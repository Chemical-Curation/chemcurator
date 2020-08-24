from itertools import chain

from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import RegexValidator
from rest_framework.exceptions import ValidationError

from chemreg.common.serializers import ControlledVocabSerializer
from chemreg.common.validators import validate_casrn_checksum
from chemreg.compound.models import BaseCompound
from chemreg.compound.serializers import CompoundSerializer
from chemreg.jsonapi.relations import PolymorphicResourceRelatedField
from chemreg.jsonapi.serializers import HyperlinkedModelSerializer
from chemreg.substance.models import (
    QCLevelsType,
    RelationshipType,
    Source,
    Substance,
    SubstanceRelationship,
    SubstanceType,
    Synonym,
    SynonymQuality,
    SynonymType,
)


class QCLevelsTypeSerializer(ControlledVocabSerializer):
    """The serializer for QCLevelsType Types."""

    class Meta(ControlledVocabSerializer.Meta):
        fields = ControlledVocabSerializer.Meta.fields + [
            "rank",
        ]
        model = QCLevelsType


class SynonymTypeSerializer(ControlledVocabSerializer):
    """The serializer for Synonym Types."""

    class Meta(ControlledVocabSerializer.Meta):
        fields = ControlledVocabSerializer.Meta.fields + [
            "validation_regular_expression",
            "score_modifier",
            "is_casrn",
        ]
        model = SynonymType

    def validate(self, data):
        """Validates non-field related errors.

        Args:
            data (dict): The dictionary of the newly updated or created SynonymType

        Returns:
            Validated data dictionary.
        """
        if self.instance:
            self.validate_synonym_set(data)
        return data

    def validate_synonym_set(self, data):
        """This validates that all Synonyms belonging to this SynonymType are valid

        Note:
            This test only needs to be run on updates.  On creates it will fail as
            there is no instance to validate against.

        Args:
            data (dict): The dictionary of the newly updated SynonymType

        Raises:
            ValidationError:  Raises an error that contains an error message with
                all synonym identifiers that fail to meet the updated type.
        """
        failed_checksum_synonyms = []
        failed_format_synonyms = []
        for synonym in self.instance.synonym_set.all():
            # Verify synonym.identifier matches the validation_regular_expression
            try:
                RegexValidator(
                    data.get("validation_regular_expression"), code="format",
                )(synonym.identifier)
            except DjangoValidationError:
                failed_format_synonyms.append(synonym)

            # If the synonym is a casrn, verify it has the correct checksum
            try:
                if data.get("is_casrn"):
                    validate_casrn_checksum(synonym.identifier)
            except ValidationError:
                failed_checksum_synonyms.append(synonym)

        if failed_checksum_synonyms or failed_format_synonyms:
            error_message = self._construct_error_message(
                failed_checksum_synonyms, failed_format_synonyms
            )
            raise ValidationError(
                error_message, "invalid_data",
            )

    def _construct_error_message(self, failed_checksums, failed_formats):
        """Accepts lists of synonyms and constructs an error message containing their
        identifiers.

        Args:
            failed_checksums (list): Synonyms that failed an update due to incorrect
                checksums
            failed_formats (list): Synonyms that failed an update due to failing to
                meet the regex formatting

        Returns:
            String containing the failing synonyms organized by how they failed
        """
        checksum_string = (
            (
                "Synonyms with invalid CAS-RN checksums: ["
                f"{', '.join(syn.identifier for syn in failed_checksums)}]"
            )
            if failed_checksums
            else None
        )
        format_string = (
            (
                "Synonyms associated with this Synonym Type do not match "
                "the proposed regular expression: ["
                f"{', '.join(syn.identifier for syn in failed_formats)}]"
            )
            if failed_formats
            else None
        )
        return "\n".join(filter(None, [checksum_string, format_string]))


class SourceSerializer(ControlledVocabSerializer):
    """The serializer for Sources."""

    class Meta(ControlledVocabSerializer.Meta):
        model = Source


class SubstanceTypeSerializer(ControlledVocabSerializer):
    """The serializer for Substance Types."""

    class Meta(ControlledVocabSerializer.Meta):
        model = SubstanceType


class SubstanceSerializer(HyperlinkedModelSerializer):
    """The serializer for Substances."""

    included_serializers = {
        "source": "chemreg.substance.serializers.SourceSerializer",
        "substance_type": "chemreg.substance.serializers.SubstanceTypeSerializer",
        "qc_level": "chemreg.substance.serializers.QCLevelsTypeSerializer",
        "associated_compound": "chemreg.compound.serializers.CompoundSerializer",
    }

    source = SourceSerializer
    substance_type = SubstanceTypeSerializer
    qc_level = QCLevelsTypeSerializer
    associated_compound = PolymorphicResourceRelatedField(
        polymorphic_serializer=CompoundSerializer,
        queryset=BaseCompound.objects,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Substance
        fields = [
            "sid",
            "preferred_name",
            "display_name",
            "description",
            "public_qc_note",
            "private_qc_note",
            "casrn",
            "source",
            "substance_type",
            "qc_level",
            "associated_compound",
        ]

    def validate(self, data):
        fields = ["preferred_name", "display_name", "casrn"]
        field_data = [
            data.get(f)  # get values in the serializer
            for f in fields
            if f in data.keys()
        ]
        if (duplicated := set([x for x in field_data if field_data.count(x) > 1])) :
            raise ValidationError(f"{duplicated.pop()} is not unique in {fields}")
        errors = []
        for field in field_data:
            restricted_identifiers = Synonym.objects.restricted().filter(
                identifier=field
            )
            restricted_substance_fields = Substance.objects.restrictive_fields(field)
            if set(chain(restricted_substance_fields, restricted_identifiers)):
                errors.append(field)
        if errors:
            raise ValidationError(
                f"The identifier/s {[e for e in errors]} is not unique in restrictive name fields."
            )
        return data


class RelationshipTypeSerializer(ControlledVocabSerializer):
    """The serializer for Substance Types."""

    class Meta(ControlledVocabSerializer.Meta):
        model = RelationshipType
        fields = ControlledVocabSerializer.Meta.fields + [
            "corrolary_label",
            "corrolary_short_description",
        ]


class SynonymQualitySerializer(ControlledVocabSerializer):
    """The serializer for Synonym Qualities."""

    class Meta(ControlledVocabSerializer.Meta):
        model = SynonymQuality
        fields = ControlledVocabSerializer.Meta.fields + [
            "score_weight",
            "is_restrictive",
        ]

    def validate_score_weight(self, value):
        if not value > 0:
            raise ValidationError("Score Weight must be greater than zero.")
        return value

    def validate_is_restrictive(self, value):
        if value and self.instance:
            # get list of unique identifiers
            qs = self.instance.synonym_set.order_by("identifier").values_list(
                "identifier", flat=True
            )
            if qs.distinct().count() != qs.count():
                # find equivalent values
                equiv = qs.intersection(qs.distinct())
                raise ValidationError(
                    (
                        "Synonyms associated with this SynonymQuality do not "
                        f"meet uniqueness constraints. {[e for e in equiv]}"
                    )
                )
        return value


class SynonymSerializer(HyperlinkedModelSerializer):
    """The serializer for Synonyms."""

    source = SourceSerializer
    substance = SubstanceSerializer
    synonym_quality = SynonymQualitySerializer
    synonym_type = SynonymTypeSerializer

    class Meta:
        model = Synonym
        fields = [
            "identifier",
            "qc_notes",
            "source",
            "substance",
            "synonym_quality",
            "synonym_type",
        ]

    def validate(self, data):
        """Validates non-field related errors.

        Args:
            data (dict): The dictionary of the newly updated or created Synonym

        Returns:
            Validated data dictionary.
        """
        synonym_type = data.get("synonym_type", None) or self.instance.synonym_type

        # Validate data.identifier is a valid synonym_type.validation_regular_expression
        RegexValidator(
            synonym_type.validation_regular_expression,
            "The proposed Synonym identifier does not conform to "
            "the regexp for the associated Synonym Type",
            "format",
        )(data.get("identifier"))

        if synonym_type.is_casrn:
            validate_casrn_checksum(data["identifier"])

        identifier = data.get("identifier", None) or self.instance.identifier
        restricted_identifiers = Synonym.objects.restricted().filter(
            identifier=identifier
        )
        restricted_substance_fields = Substance.objects.restrictive_fields(identifier)
        if set(chain(restricted_identifiers, restricted_substance_fields)):
            raise ValidationError(
                f"The identifier '{identifier}' is not unique in restrictive name fields."
            )
        return data


class SubstanceRelationshipSerializer(HyperlinkedModelSerializer):
    """The serializer for Substance Relationships."""

    from_substance = SubstanceSerializer
    to_substance = SubstanceSerializer
    source = SourceSerializer
    relationship_type = RelationshipTypeSerializer

    class Meta:
        model = SubstanceRelationship
        fields = [
            "from_substance",
            "to_substance",
            "source",
            "relationship_type",
            "qc_notes",
        ]
