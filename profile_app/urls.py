from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProfileView,
    TrustedContactViewSet,
    AadhaarVerificationView,
    VehicleDetailsView,
    FullProfileView,
)

router = DefaultRouter()
router.register("contacts", TrustedContactViewSet, basename="contacts")

urlpatterns = [
    path("", ProfileView.as_view()),
    path("", include(router.urls)),
    path("aadhaar/", AadhaarVerificationView.as_view()),
    path("vehicle/", VehicleDetailsView.as_view()),
    path("full/", FullProfileView.as_view()),
]
