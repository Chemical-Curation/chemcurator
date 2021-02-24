from django.urls import include, path

from chemreg.jsonapi.routers import SimpleRouter
from chemreg.resolution import views

# Create a router and register our viewsets with it.
router = SimpleRouter()
router.register(views.ResolverViewSet, basename="resolution", prefix="resolution")


urlpatterns = [
    path("", include(router.urls)),
]
