from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse as drf_reverse

from rest_framework_json_api.utils import format_value

from chemreg.common.serializers import CommonInfoSerializer, ControlledVocabSerializer
from chemreg.compound.fields import StructureAliasField
from chemreg.compound.models import (
    BaseCompound,
    DefinedCompound,
    IllDefinedCompound,
    QueryStructureType,
)
from chemreg.compound.validators import (
    validate_inchikey_computable,
    validate_molfile_v2000,
    validate_molfile_v3000_computable,
    validate_smiles,
)
from chemreg.indigo.errors import catch_compound_calc_error
from chemreg.indigo.inchi import get_inchikey
from chemreg.indigo.molfile import get_molfile_v3000
from chemreg.jsonapi.serializers import PolymorphicModelSerializer


class BaseCompoundSerializer(CommonInfoSerializer):
    """The base serializer for compounds."""

    included_serializers = {
        **CommonInfoSerializer.included_serializers,
        **{"substance": "chemreg.substance.serializers.SubstanceSerializer"},
    }

    serializer_field_mapping = CommonInfoSerializer.serializer_field_mapping
    serializer_field_mapping.update({StructureAliasField: serializers.CharField})
    replaced_by = "chemreg.compound.serializers.CompoundSerializer"
    substance = "chemreg.substance.serializers.SubstanceSerializer"

    class Meta(CommonInfoSerializer.Meta):
        fields = CommonInfoSerializer.Meta.fields + ["id", "qc_note", "replaced_by"]
        model = BaseCompound

    def __init__(self, *args, is_admin=False, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove admin-only fields
        if not is_admin:
            self.fields.pop("qc_note")
            self.fields.pop("replaced_by")


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
    alt_structures = ("molfile_v2000", "molfile_v3000", "smiles")

    class Meta(BaseCompoundSerializer.Meta):
        model = DefinedCompound
        fields = BaseCompoundSerializer.Meta.fields + [
            "inchikey",
            "molfile_v2000",
            "molfile_v3000",
            "smiles",
            "substance",
        ]
        extra_kwargs = {
            "molfile_v3000": {"required": False, "trim_whitespace": False},
            "substance": {"required": False},
        }

    def __init__(self, *args, admin_override=False, **kwargs):
        self.admin_override = admin_override
        super().__init__(*args, **kwargs)

    def validate_id(self, value):
        # if there is no inchikey on POST (patch id's are not editable)
        if "inchikey" not in self.initial_data and not self.instance:
            raise ValidationError("InchIKey must be included when CID is defined.")
        return value

    def validate_inchikey(self, value):
        if "id" not in self.initial_data:
            raise ValidationError("CID must be included when InchIKey is defined.")
        return value

    def validate(self, data):
        qs = self.Meta.model.objects.filter(inchikey=data["inchikey"])
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists() and not self.admin_override:
            matched = []
            req = self.context.get("request", None)
            for obj in qs:
                matched.append(
                    drf_reverse(
                        "definedcompound-detail", request=req, kwargs={"pk": obj.pk}
                    )
                )
            raise ValidationError(
                {
                    "detail": {
                        "detail": f"Inchikey conflicts with {[x.id for x in qs]}",
                        "links": matched,
                        "status": "400",
                        "source": {"pointer": "/data/attributes/inchikey"},
                        "code": "invalid",
                    },
                },
            )
        return data

    def to_internal_value(self, data):
        matched_fields = set(self.alt_structures) & set(self.initial_data.keys())
        formatted_fields = [format_value(f) for f in sorted(self.alt_structures)]
        formatted_matched_fields = [format_value(f) for f in sorted(matched_fields)]
        if not matched_fields:
            raise ValidationError(
                {"non_field_errors": f"One of {sorted(formatted_fields)} required."}
            )
        if len(matched_fields) > 1:
            raise ValidationError(
                {
                    "non_field_errors": (
                        f"Only one of {formatted_fields} allowed. "
                        f"Recieved {formatted_matched_fields}."
                    )
                }
            )
        data = super().to_internal_value(data)  # calls field validators
        structure = next(k for k in self.alt_structures if k in data)
        data["molfile_v3000"] = get_molfile_v3000(data.pop(structure))
        if "inchikey" not in data:
            data["inchikey"] = get_inchikey(data["molfile_v3000"])
        return data


class DefinedCompoundDetailSerializer(DefinedCompoundSerializer):
    molecular_weight = serializers.SerializerMethodField()
    molecular_formula = serializers.SerializerMethodField()
    smiles = serializers.SerializerMethodField()
    calculated_inchikey = serializers.SerializerMethodField()

    class Meta(DefinedCompoundSerializer.Meta):
        fields = DefinedCompoundSerializer.Meta.fields + [
            "molecular_weight",
            "molecular_formula",
            "smiles",
            "calculated_inchikey",
        ]

    @catch_compound_calc_error
    def get_molecular_weight(self, obj):
        return obj.indigo_structure.molecularWeight()

    @catch_compound_calc_error
    def get_molecular_formula(self, obj):
        return obj.indigo_structure.grossFormula()

    @catch_compound_calc_error
    def get_smiles(self, obj):
        return obj.indigo_structure.smiles()

    @catch_compound_calc_error
    def get_calculated_inchikey(self, obj):
        return get_inchikey(obj.molfile_v3000)


class QueryStructureTypeSerializer(ControlledVocabSerializer):
    """The serializer for query structure type."""

    class Meta(ControlledVocabSerializer.Meta):
        model = QueryStructureType


class IllDefinedCompoundSerializer(BaseCompoundSerializer):
    """The serializer for ill-defined compounds."""

    query_structure_type = QueryStructureTypeSerializer

    class Meta(BaseCompoundSerializer.Meta):
        model = IllDefinedCompound
        fields = BaseCompoundSerializer.Meta.fields + [
            "mrvfile",
            "query_structure_type",
            "substance",
        ]
        extra_kwargs = {
            "substance": {"required": False},
        }


class CompoundSerializer(PolymorphicModelSerializer):
    """The serializer for both ill-defined and defined compounds."""

    polymorphic_serializers = [DefinedCompoundSerializer, IllDefinedCompoundSerializer]
    serializer_kwargs = {
        DefinedCompoundSerializer: ["override", "is_admin"],
        IllDefinedCompoundSerializer: ["is_admin"],
    }

    class Meta:
        model = BaseCompound


class CompoundDetailSerializer(PolymorphicModelSerializer):
    """The serializer for both ill-defined and defined compounds."""

    polymorphic_serializers = [
        DefinedCompoundDetailSerializer,
        IllDefinedCompoundSerializer,
    ]
    serializer_kwargs = {
        DefinedCompoundDetailSerializer: ["override", "is_admin"],
        IllDefinedCompoundSerializer: ["is_admin"],
    }

    class Meta:
        model = BaseCompound


class CompoundDeleteSerializer(serializers.Serializer):
    """Serializes data required for the soft delete of compounds."""

    replacement_cid = serializers.SlugRelatedField(
        slug_field="id", queryset=BaseCompound.objects.all()
    )
    qc_note = serializers.CharField()

    def update(self, instance, validated_data):
        """
        This method is called when "deleting" the instance.

        We're using a QuerySet update to avoid any weirdness while updating the
        instance that the Model.object manager will then see as deleted.
        """
        BaseCompound.objects.with_deleted().filter(pk=instance.pk).update(
            replaced_by=validated_data["replacement_cid"],
            qc_note=validated_data["qc_note"],
        )
        # Django REST Framework wants this function to return an
        # updated instance, so let's give it one.
        instance.replaced_by = validated_data["replacement_cid"]
        instance.qc_note = validated_data["qc_note"]
        return instance
