from django.urls import include, path

urlpatterns = [
    path("", include("chemreg.openapi.urls")),
    path("", include("chemreg.auth.urls")),
    path("", include("chemreg.compound.urls")),
    path("", include("chemreg.substance.urls")),
    path("", include("chemreg.resolution.urls")),
    path("", include("chemreg.lists.urls")),
    path("", include("django_prometheus.urls")),
]
