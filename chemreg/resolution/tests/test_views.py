import pytest

from chemreg.jsonapi.views import ModelViewSet
from chemreg.resolution.views import ResolverViewSet


def test_resolution_view():
    """Tests that the Resolver View Set, is a sub class of the Model View Set."""
    assert issubclass(ResolverViewSet, ModelViewSet)


@pytest.mark.django_db
def test_resolution_parameter(client):
    resp = client.get("/resolution")
    assert resp.status_code == 400
    assert str(resp.data[0]["detail"]) == "'search' parameter required at this endpoint"
