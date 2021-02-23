from chemreg.compound.models import BaseCompound
from chemreg.compound.serializers import (
    DefinedCompoundSerializer,
    IllDefinedCompoundSerializer,
)
from chemreg.jsonapi.serializers import PolymorphicModelSerializer
from chemreg.substance.serializers import SubstanceSerializer


class SearchResolutionSerializer(PolymorphicModelSerializer):
    """Serializer to return Substances and Compounds"""

    polymorphic_serializers = [
        SubstanceSerializer,
        DefinedCompoundSerializer,
        IllDefinedCompoundSerializer,
    ]
    serializer_kwargs = {
        DefinedCompoundSerializer: ["override", "is_admin"],
        IllDefinedCompoundSerializer: ["is_admin"],
    }

    class Meta:
        model = BaseCompound
