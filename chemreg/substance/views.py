from collections import namedtuple

from rest_framework import viewsets
from rest_framework.response import Response

from chemreg.common.mixins import DeprecateDeleteMixin
from chemreg.compound.models import DefinedCompound
from chemreg.compound.serializers import DefinedCompoundSerializer
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


ResolverResponse = namedtuple("ResolverResponse", ("substances", "compounds"))


class ResolverViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing the Tweets and Articles in your Timeline.
    """

    def list(self, request):
        print("yay")
        # timeline = ResolverResponse (
        #     substances=Substance.objects.all(),
        #     compounds=DefinedCompound.objects.all(),
        # )
        # serializer = SearchResolutionSerializer(timeline)

        subs = SubstanceSerializer(
            Substance.objects.all(), context={"request": request}, many=True
        )
        comps = DefinedCompoundSerializer(
            DefinedCompound.objects.all(), context={"request": request}, many=True
        )

        # return Response(serializer.data)
        return Response({"substances": subs.data, "compounds": comps.data})
