from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q

from chemreg.common.models import CommonInfo, ControlledVocabulary
from chemreg.common.validators import (
    UniqueAcrossModelsValidator,
    validate_casrn_checksum,
    validate_deprecated,
    validate_is_regex,
)
from chemreg.substance.utils import build_sid


class QCLevelsType(ControlledVocabulary):
    """Controlled vocabulary for qc_levels

    Attributes:
        Name = String (Less than 50 character, url safe, unique, required field)
        Label = String (Less than 100 characters, unique, required field)
        Short Description = String (Less than 500 characters, required field)
        Long Description = TEXT (required field)
        rank = integer unique
    """

    rank = models.IntegerField(unique=True)

    class JSONAPIMeta:
        resource_name = "qcLevel"


class Source(ControlledVocabulary):
    """Controlled vocabulary for Sources

    Attributes:
        Name = String (Less than 50 character, url safe, unique, required field)
        Label = String (Less than 100 characters, unique, required field)
        Short Description = String (Less than 500 characters, required field)
        Long Description = TEXT (required field)
    """

    pass


class SubstanceQuerySet(models.QuerySet):
    def restrictive_fields(self, value):
        qs = self.filter(
            Q(preferred_name=value) | Q(display_name=value) | Q(casrn=value)
        )
        return qs


class Substance(CommonInfo):
    """Substances document chemical concepts

    Attributes:
        id (str): Generated SID for external use
        preferred_name (str): Name of the substance
        display_name (str): User friendly name of the substance
        source (foreign key): Controlled vocabulary for Sources
        substance_type (foreign key): Controlled vocabulary for Substances
        qc_level (foreign key): Controlled vocabulary for QCLevels
        description (str, optional): A description of the substance
        public_qc_note (str, optional): Note from Quality Control.  Visible to everyone
        private_qc_note (str, optional): Note from Quality Control.
        associated_compound (foreign key): Polymorphic relationship to Compounds.Compounds.
            Can either be either a DefinedCompound or an IllDefinedCompound
        casrn (str): CAS registry number. It is an identifier from the CAS Registry
            (https://www.cas.org/support/documentation/chemical-substances) for a chemical substance.
        synonyms (QuerySet): One to Many Synonym resources
        substance_histories (QuerySet): One to Many Substance history resources (not implemented yet)
    """

    preferred_name_regex = r"^[a-zA-Z0-9 =<>\-\*_':.,^%&\/{}[\]?()+]{3,}$"
    display_name_regex = r"^[a-zA-Z0-9 =<>\-\*_':.,^%&\/{}[\]?()+]{3,}$"
    casrn_regex = r"^[0-9]{2,7}-[0-9]{2}-[0-9]$"

    id = models.CharField(
        default=build_sid,
        primary_key=True,
        max_length=50,
        unique=True,
        validators=[UniqueAcrossModelsValidator(model_list=["compound.BaseCompound"])],
    )
    preferred_name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        validators=[
            RegexValidator(
                preferred_name_regex,
                message="The proposed Preferred Name does not conform "
                f"to the regular expression {preferred_name_regex}",
            )
        ],
    )
    display_name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        null=True,
        validators=[
            RegexValidator(
                display_name_regex,
                message="The proposed display name does not conform "
                f"to the regular expression {display_name_regex}",
            )
        ],
    )
    source = models.ForeignKey(
        "Source", on_delete=models.PROTECT, null=False, validators=[validate_deprecated]
    )
    substance_type = models.ForeignKey(
        "SubstanceType",
        on_delete=models.PROTECT,
        null=False,
        validators=[validate_deprecated],
    )
    qc_level = models.ForeignKey(
        "QCLevelsType",
        on_delete=models.PROTECT,
        null=False,
        validators=[validate_deprecated],
    )
    description = models.CharField(max_length=1024, blank=True)
    public_qc_note = models.CharField(max_length=1024, blank=True)
    private_qc_note = models.CharField(max_length=1024, blank=True)
    associated_compound = models.OneToOneField(
        "compound.BaseCompound",
        on_delete=models.PROTECT,
        null=True,
        related_name="substance",
    )
    casrn = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        validators=[
            RegexValidator(
                casrn_regex,
                message="The proposed CASRN does not conform "
                f"to the regular expression {casrn_regex}",
            ),
            validate_casrn_checksum,
        ],
    )

    def __init__(self, *args, **kwargs):
        super(Substance, self).__init__(*args, **kwargs)
        # this is needed to determine whether a compound is becoming "orphaned"
        self.original_compound = self.associated_compound

    objects = SubstanceQuerySet.as_manager()


class SubstanceRelationship(CommonInfo):
    """ Through table linking Substances to each other. This is a self referential relationship.

    Attributes:
        from_substance (foreign key): The primary member in the relationship
        to_substance (foreign key): The secondary member in the relationship
        relationship_type (foreign key): the type of relationship between the
            two substances (required)
        source (foreign key): A source controlled vocabulary for the source type
            from which this data was derived (required)
        qc_notes (str): Quality Control Notes (optional)
    """

    from_substance = models.ForeignKey(
        "Substance", related_name="relationships", on_delete=models.PROTECT
    )
    to_substance = models.ForeignKey(
        "Substance", related_name="related_to", on_delete=models.PROTECT
    )
    source = models.ForeignKey("Source", on_delete=models.PROTECT)
    relationship_type = models.ForeignKey("RelationshipType", on_delete=models.PROTECT)
    qc_notes = models.CharField(max_length=1024, blank=True)

    class Meta:
        unique_together = (
            "from_substance",
            "to_substance",
            "source",
            "relationship_type",
        )
        ordering = ["pk"]
        base_manager_name = "objects"


class SubstanceType(ControlledVocabulary):
    """Controlled vocabulary for Substances

    Attributes:
        Name = String (Less than 50 character, url safe, unique, required field)
        Label = String (Less than 100 characters, unique, required field)
        Short Description = String (Less than 500 characters, required field)
        Long Description = TEXT (required field)
    """

    pass


class SynonymType(ControlledVocabulary):
    """Controlled vocabulary for SynonymTypes

    Attributes:
        name (str): Slug field of the synonym type (Less than 50 character, url safe, unique, required field)
        label (str): Readable string field of the synonym type (Less than 100 characters, unique, required field)
        short_description (str): Short description of the synonym type (Less than 500 characters, required field)
        long_description (str): Long description of the synonym type (required field)
        validation_regular_expression (str): (optional)
        score_modifier (float): (default 0)
        is_casrn (bool): Whether the synonyms related to this type have identifiers that are valid CAS_RNs (required)
    """

    validation_regular_expression = models.TextField(
        blank=True, validators=[validate_is_regex]
    )
    score_modifier = models.FloatField(default=0)
    is_casrn = models.BooleanField()


class SynonymQuality(ControlledVocabulary):
    """Controlled vocabulary for SynonymQuality

    Attributes:
        Name = String (Less than 50 character, url safe, unique, required field)
        Label = String (Less than 100 characters, unique, required field)
        Short Description = String (Less than 500 characters, required field)
        Long Description = TEXT (required field)
        score_weight = Float (default 1.0) greater than 0
        is_restrictive = Boolean
    """

    score_weight = models.FloatField(default=1.0)
    is_restrictive = models.BooleanField(default=False)


class RestrictiveQuerySet(models.QuerySet):
    def restricted(self):
        return self.filter(synonym_quality__is_restrictive=True)


class Synonym(CommonInfo):
    """Information to be shared across Synonyms

    Attributes:
        identifier (str): Identifier for synonym. 1024 character limit (required)
        qc_notes (str): Quality Control note.  1024 character limit (optional)
        substance (foreign key) : Link to a Substance (optional)
        source (foreign key): Link to a Source (required)
        synonym_quality (foreign key): Link to a Synonym Quality (required)
        synonym_type (foreign key): Link to a Synonym Type (optional)
    """

    identifier = models.TextField(max_length=1024)
    qc_notes = models.TextField(max_length=1024, blank=True)
    substance = models.ForeignKey("Substance", on_delete=models.PROTECT)
    source = models.ForeignKey("Source", on_delete=models.PROTECT)
    synonym_quality = models.ForeignKey("SynonymQuality", on_delete=models.PROTECT)
    synonym_type = models.ForeignKey("SynonymType", null=True, on_delete=models.PROTECT)

    objects = RestrictiveQuerySet.as_manager()


class RelationshipType(ControlledVocabulary):
    """Controlled vocabulary for Substances

    Attributes:
        name (str): Slug field of the relationship type (Less than 50 character, url safe, unique, required field)
        label (str): Readable string field of the relationship type (Less than 100 characters, unique, required field)
        short_description (str): Short description of the relationship type (Less than 500 characters, required field)
        long_description (str): Long description of the relationship type (required field)
        corrolary_label (str): (Less than 100 characters, unique, required field)
        corrolary_short_description (str): (Less than 500 characters, required field)
    """

    corrolary_label = models.CharField(max_length=99)
    corrolary_short_description = models.CharField(max_length=499)
