from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import MyProviderProfileView, MyServicesViewSet, ProviderBrowseViewSet

router = DefaultRouter()
router.register("providers", ProviderBrowseViewSet, basename="provider")
router.register("provider/services", MyServicesViewSet, basename="my-service")

urlpatterns = [
    path("provider/profile/", MyProviderProfileView.as_view(), name="my-provider-profile"),
] + router.urls
