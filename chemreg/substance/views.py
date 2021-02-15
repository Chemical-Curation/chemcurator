from itertools import chain

from rest_framework.response import Response

from chemreg.common.mixins import DeprecateDeleteMixin
from chemreg.compound.models import BaseCompound
from chemreg.jsonapi.views import ModelViewSet
from chemreg.substance.filters import SubstanceFilter, SubstanceRelationshipFilter
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
from chemreg.substance.serializers import (  # SearchResolutionSerializer,
    QCLevelsTypeSerializer,
    RelationshipTypeSerializer,
    SearchResolutionSerializer,
    SourceSerializer,
    SubstanceRelationshipSerializer,
    SubstanceSerializer,
    SubstanceTypeSerializer,
    SynonymQualitySerializer,
    SynonymSerializer,
    SynonymTypeSerializer,
)


class QCLevelsTypeViewSet(DeprecateDeleteMixin, ModelViewSet):

    queryset = QCLevelsType.objects.all()
    serializer_class = QCLevelsTypeSerializer


class SynonymTypeViewSet(DeprecateDeleteMixin, ModelViewSet):

    queryset = SynonymType.objects.all()
    serializer_class = SynonymTypeSerializer


class SourceViewSet(DeprecateDeleteMixin, ModelViewSet):

    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class SubstanceViewSet(ModelViewSet):

    queryset = Substance.objects.all()
    serializer_class = SubstanceSerializer
    filterset_class = SubstanceFilter


class SubstanceTypeViewSet(DeprecateDeleteMixin, ModelViewSet):

    queryset = SubstanceType.objects.all()
    serializer_class = SubstanceTypeSerializer


class RelationshipTypeViewSet(DeprecateDeleteMixin, ModelViewSet):

    queryset = RelationshipType.objects.all()
    serializer_class = RelationshipTypeSerializer


class SynonymQualityViewSet(DeprecateDeleteMixin, ModelViewSet):

    queryset = SynonymQuality.objects.all()
    serializer_class = SynonymQualitySerializer


class SynonymViewSet(ModelViewSet):

    queryset = Synonym.objects.all()
    serializer_class = SynonymSerializer
    filterset_fields = ["substance__id"]


class SubstanceRelationshipViewSet(ModelViewSet):

    queryset = SubstanceRelationship.objects.all()
    serializer_class = SubstanceRelationshipSerializer
    filterset_class = SubstanceRelationshipFilter


class ResolverViewSet(ModelViewSet):
    """
    A simple ViewSet for listing the Tweets and Articles in your Timeline.
    """

    serializer_class = SearchResolutionSerializer

    def get_queryset(self):
        return None

    def list(self, request, *args, **kwargs):
        big_qs = list(chain(Substance.objects.all(), BaseCompound.objects.all()))

        big = self.get_serializer(big_qs, many=True)

        return Response(big.data)
