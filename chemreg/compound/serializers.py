from rest_framework import serializers

from chemreg.common.validators import OneOfValidator
from chemreg.compound.fields import StructureAliasField
from chemreg.compound.models import (
    DefinedCompound,
    IllDefinedCompound,
    QueryStructureType,
)
from chemreg.compound.validators import (
    validate_inchikey_computable,
    validate_inchikey_unique,
    validate_molfile_v2000,
    validate_molfile_v3000_computable,
    validate_smiles,
)
from chemreg.indigo.molfile import get_molfile_v3000
from chemreg.jsonapi.serializers import HyperlinkedModelSerializer


class BaseCompoundSerializer(HyperlinkedModelSerializer):
    """The base serializer for compounds."""

    serializer_field_mapping = HyperlinkedModelSerializer.serializer_field_mapping
    serializer_field_mapping.update({StructureAliasField: serializers.CharField})


class DefinedCompoundSerializer(BaseCompoundSerializer):
    """The serializer for defined compounds."""

    molfile_v2000 = serializers.CharField(
        write_only=True,
        required=False,
        validators=[
            validate_molfile_v2000,
            validate_inchikey_computable,
            validate_molfile_v3000_computable,
        ],
        trim_whitespace=False,
    )
    smiles = serializers.CharField(
        write_only=True,
        required=False,
        validators=[
            validate_smiles,
            validate_inchikey_computable,
            validate_molfile_v3000_computable,
        ],
        trim_whitespace=False,
    )

    class Meta:
        model = DefinedCompound
        fields = (
            "cid",
            "inchikey",
            "molfile_v2000",
            "molfile_v3000",
            "smiles",
        )
        extra_kwargs = {"molfile_v3000": {"required": False, "trim_whitespace": False}}
        validators = [
            OneOfValidator("molfile_v2000", "molfile_v3000", "smiles", required=True)
        ]

    def __init__(self, *args, admin_override=False, **kwargs):
        if not admin_override:
            for structrue in ("molfile_v2000", "molfile_v3000", "smiles"):
                field = self.fields[structrue]
                field.validators.append(validate_inchikey_unique)
        super().__init__(*args, **kwargs)

    def validate(self, data):
        alt_structures = ("molfile_v2000", "molfile_v3000", "smiles")
        alt_structure = next(k for k in alt_structures if k in data)
        data["molfile_v3000"] = get_molfile_v3000(data.pop(alt_structure))
        return data


class QueryStructureTypeSerializer(HyperlinkedModelSerializer):
    """The serializer for query structure type."""

    class Meta:
        model = QueryStructureType
        fields = ("name", "label", "short_description", "long_description")


class IllDefinedCompoundSerializer(BaseCompoundSerializer):
    """The serializer for ill-defined compounds."""

    query_structure_type = QueryStructureTypeSerializer

    class Meta:
        model = IllDefinedCompound
        fields = ("cid", "mrvfile", "query_structure_type")
