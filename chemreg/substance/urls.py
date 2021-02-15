from django.urls import include, path

from chemreg.jsonapi.routers import SimpleRouter
from chemreg.substance import views

# Create a router and register our viewsets with it.
router = SimpleRouter()
router.register(views.QCLevelsTypeViewSet, "qcLevels")
router.register(views.RelationshipTypeViewSet)
router.register(views.SynonymViewSet)
router.register(views.SynonymTypeViewSet)
router.register(views.SourceViewSet)
router.register(views.SubstanceViewSet)
router.register(views.SubstanceTypeViewSet)
router.register(views.SynonymQualityViewSet, prefix="synonymQualities")
router.register(views.SubstanceRelationshipViewSet)
router.register(views.ResolverViewSet, basename="substances", prefix="bologna")


urlpatterns = [
    path("", include(router.urls)),
]
