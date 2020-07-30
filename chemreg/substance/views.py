from chemreg.common.mixins import DeprecateDeleteMixin
from chemreg.jsonapi.views import ModelViewSet
from chemreg.substance.models import (
    QCLevelsType,
    RelationshipType,
    Source,
    Substance,
    SubstanceType,
    Synonym,
    SynonymQuality,
    SynonymType,
)
from chemreg.substance.serializers import (
    QCLevelsTypeSerializer,
    RelationshipTypeSerializer,
    SourceSerializer,
    SubstanceSerializer,
    SubstanceTypeSerializer,
    SynonymQualitySerializer,
    SynonymSerializer,
    SynonymTypeSerializer,
)


class QCLevelsTypeViewSet(ModelViewSet):

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


class SubstanceTypeViewSet(ModelViewSet):

    queryset = SubstanceType.objects.all()
    serializer_class = SubstanceTypeSerializer


class RelationshipTypeViewSet(ModelViewSet):

    queryset = RelationshipType.objects.all()
    serializer_class = RelationshipTypeSerializer


class SynonymQualityViewSet(ModelViewSet):

    queryset = SynonymQuality.objects.all()
    serializer_class = SynonymQualitySerializer


class SynonymViewSet(ModelViewSet):

    queryset = Synonym.objects.all()
    serializer_class = SynonymSerializer
