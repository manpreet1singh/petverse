from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PetViewSet, VaccinationViewSet

router = DefaultRouter()
router.register("pets", PetViewSet, basename="pet")

vaccination_list = VaccinationViewSet.as_view({"get": "list", "post": "create"})
vaccination_detail = VaccinationViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = router.urls + [
    path("pets/<int:pet_pk>/vaccinations/", vaccination_list, name="vaccination-list"),
    path("pets/<int:pet_pk>/vaccinations/<int:pk>/", vaccination_detail, name="vaccination-detail"),
]
