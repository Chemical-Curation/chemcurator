from django.db import models
from django.utils.functional import cached_property

from indigo import Indigo, IndigoException
from polymorphic.models import PolymorphicManager, PolymorphicModel
from polymorphic.query import PolymorphicQuerySet

from chemreg.common.models import CommonInfo, ControlledVocabulary
from chemreg.common.validators import UniqueAcrossModelsValidator, validate_deprecated
from chemreg.compound.fields import StructureAliasField
from chemreg.compound.utils import build_cid
from chemreg.compound.validators import (
    validate_inchikey_computable,
    validate_molfile_v3000,
)
from chemreg.indigo.inchi import get_inchikey


class SoftDeleteCompoundQuerySet(PolymorphicQuerySet):
    """Filters out the soft deleted compounds."""

    def filter_deleted(self):
        return self.filter(replaced_by__isnull=True)

    def delete(self, force=False):
        if not force:
            raise Exception(
                "Attempted to delete a soft-delete model. "
                "Pass in `force=True` if you need to perfrom an actual deletion."
            )
        return super().delete()


class SoftDeleteCompoundManager(PolymorphicManager):
    """Filters out the soft deleted compounds."""

    def get_queryset(self):
        """The default queryset filters out deleted."""
        qs = super().get_queryset()
        return qs.filter_deleted()

    def with_deleted(self):
        """Include deleted with this call."""
        return super().get_queryset()


class BaseCompound(PolymorphicModel, CommonInfo):
    """The base class for compounds.

    This model shouldn't exist on it's own. It will always be subclassed
    by a concrete compound. The `chemreg.compound.fields.StructureAliasField`
    can be used to reference the `structure` field on subclassed models. This
    field can then have a more sensible name and varied validation logic
    applied to it.

    Attributes:
        id (str): The compound CID.
        structure (str): Definitive structure string
        replaced_by (foreign key): A user deleted the compound and specified this CID as the replacement
        qc_note (str): An explanation of why the compound was deleted and replaced
    """

    id = models.CharField(
        default=build_cid,
        primary_key=True,
        max_length=50,
        unique=True,
        validators=[UniqueAcrossModelsValidator(model_list=["substance.Substance"])],
    )
    structure = models.TextField()
    # soft delete functionality
    replaced_by = models.ForeignKey(
        "self",
        related_name="replaces",
        on_delete=models.PROTECT,
        null=True,
        default=None,
    )
    qc_note = models.TextField(blank=True, default="")
    objects = SoftDeleteCompoundManager.from_queryset(SoftDeleteCompoundQuerySet)()

    class Meta:
        ordering = ["pk"]

    @property
    def is_deleted(self):
        return self.replaced_by_id is not None

    @property
    def serializer_name(self):
        """Camel cased string of model for serializer"""
        s = self._meta.label.split(".")[-1]
        return s[0].lower() + s[1:]

    def delete(self, force=False):
        if not force:
            raise Exception(
                "Attempted to delete a soft-delete model. "
                "Pass in `force=True` if you need to perfrom an actual deletion."
            )
        return super().delete()


class DefinedCompound(BaseCompound):
    """A defined compound.

    Attributes:
        molfile_v3000 (str): A v3000 molfile. Alias to definitive structure string.
        inchikey (str): A hashed key based off of the chemical structure.

    """

    molfile_v3000 = StructureAliasField(
        validators=[validate_molfile_v3000, validate_inchikey_computable]
    )
    inchikey = models.CharField(null=True, max_length=29)

    @property
    def _inchikey(self):
        """Computes the inchikey from the molfile."""
        try:
            return get_inchikey(self.molfile_v3000)
        except IndigoException:
            return None

    @cached_property
    def indigo_structure(self):
        indigo = Indigo()
        indigo.setOption("molfile-saving-mode", "3000")
        return indigo.loadStructure(structureStr=self.molfile_v3000)


class QueryStructureType(ControlledVocabulary):
    """A controlled vocabulary

    Attributes:
    Name = String (Less than 50 character, url safe, unique, required field)
    Label = String (Less than 100 characters, unique, required field)
    Short Description = String (Less than 500 characters, required field)
    Long Description = TEXT (required field)
    """

    pass


def get_illdefined_qst():
    """Default value for `IllDefinedCompound.query_structure_type`.

    This object is created in a data migration. Calling `get_or_create` here will
    cause migrations to fail if `QueryStructureType` has been modified: the new model
    would be used to create the model prior to new columns made in the database.
    """
    return QueryStructureType.objects.get(name="ill-defined").pk


class IllDefinedCompound(BaseCompound):
    """An ill-defined compound.

    Attributes:
        mrvfile (str): Alias to definitive structure string.
        query_structure_type (foreign key): A foreign key to the "ill-defined" record in the "query structure type"
         controlled vocabulary

    """

    mrvfile = StructureAliasField()
    query_structure_type = models.ForeignKey(
        "QueryStructureType",
        on_delete=models.PROTECT,
        default=get_illdefined_qst,
        validators=[validate_deprecated],
    )

    class Meta(BaseCompound.Meta):
        verbose_name = "ill-defined compound"
