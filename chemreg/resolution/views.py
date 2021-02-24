from itertools import chain

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from chemreg.compound.models import BaseCompound
from chemreg.jsonapi.views import ModelViewSet
from chemreg.resolution.indices import SubstanceIndex
from chemreg.resolution.serializers import SearchResolutionSerializer
from chemreg.substance.models import Substance


class ResolverViewSet(ModelViewSet):
    """
    A view set to return both compound and substance from resolver
    """

    http_method_names = ["get"]
    permission_classes = []
    serializer_class = SearchResolutionSerializer

    def get_queryset(self, *args, **kwargs):
        return None

    def list(self, request, *args, **kwargs):

        value = request.query_params.get("search")
        if not value:
            raise ValidationError("'search' parameter required at this endpoint")

        resp_json = SubstanceIndex().search(value)

        sub_ids = [row["id"] for row in resp_json["data"] if "DTXSID" in row["id"]]
        comp_ids = [row["id"] for row in resp_json["data"] if "DTXCID" in row["id"]]

        substances = Substance.objects.filter(id__in=sub_ids)
        compounds = BaseCompound.objects.filter(id__in=comp_ids)

        big_qs = list(chain(substances, compounds))

        big = self.get_serializer(big_qs, many=True)

        return Response(big.data)
