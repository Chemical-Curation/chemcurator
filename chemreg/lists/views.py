from chemreg.common.mixins import DeprecateDeleteMixin
from chemreg.jsonapi.views import ModelViewSet
from chemreg.lists.models import (
    AccessibilityType,
    ExternalContact,
    IdentifierType,
    List,
    ListType,
    Record,
    RecordIdentifier,
)
from chemreg.lists.serializers import (
    AccessibilityTypeSerializer,
    ExternalContactSerializer,
    IdentifierTypeSerializer,
    ListSerializer,
    ListTypeSerializer,
    RecordIdentifierSerializer,
    RecordSerializer,
)


class AccessibilityTypeViewSet(DeprecateDeleteMixin, ModelViewSet):

    queryset = AccessibilityType.objects.all()
    serializer_class = AccessibilityTypeSerializer


class ExternalContactViewSet(ModelViewSet):

    queryset = ExternalContact.objects.all()
    serializer_class = ExternalContactSerializer


class IdentifierTypeViewSet(DeprecateDeleteMixin, ModelViewSet):

    queryset = IdentifierType.objects.all()
    serializer_class = IdentifierTypeSerializer


class ListViewSet(ModelViewSet):

    queryset = List.objects.all()
    serializer_class = ListSerializer


class ListTypeViewSet(DeprecateDeleteMixin, ModelViewSet):

    queryset = ListType.objects.all()
    serializer_class = ListTypeSerializer


class RecordViewSet(ModelViewSet):

    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    filterset_fields = ["substance__id"]


class RecordIdentifierViewSet(ModelViewSet):

    queryset = RecordIdentifier.objects.all()
    serializer_class = RecordIdentifierSerializer
