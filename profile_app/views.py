# from rest_framework import viewsets, permissions, generics
# from rest_framework.response import Response
#
# from .models import Profile, TrustedContact, AadhaarVerification, VehicleDetails
# from .serializers import (
#     ProfileSerializer,            # <-- FIXED
#     TrustedContactSerializer,
#     AadhaarVerificationSerializer,
#     VehicleDetailsSerializer,
#     FullProfileSerializer,
# )
#
# # --------------------------
# # USER PROFILE VIEW
# # --------------------------
# class ProfileView(generics.RetrieveUpdateAPIView):
#     serializer_class = ProfileSerializer   # <-- FIXED
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_object(self):
#         return self.request.user.profile   # this is correct
#
#
# # --------------------------
# # TRUSTED CONTACTS CRUD
# # --------------------------
# class TrustedContactViewSet(viewsets.ModelViewSet):
#     serializer_class = TrustedContactSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         return TrustedContact.objects.filter(profile__user=self.request.user)
#
#     def perform_create(self, serializer):
#         serializer.save(profile=self.request.user.profile)
#
#
# # --------------------------
# # AADHAAR VERIFY
# # --------------------------
# class AadhaarVerificationView(generics.RetrieveUpdateAPIView):
#     serializer_class = AadhaarVerificationSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_object(self):
#         profile = self.request.user.profile
#         obj, _ = AadhaarVerification.objects.get_or_create(profile=profile)
#         return obj
#
#
# # --------------------------
# # VEHICLE DETAILS
# # --------------------------
# class VehicleDetailsView(generics.RetrieveUpdateAPIView):
#     serializer_class = VehicleDetailsSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_object(self):
#         profile = self.request.user.profile
#         obj, _ = VehicleDetails.objects.get_or_create(profile=profile)
#         return obj
#
#
# # --------------------------
# # FULL PROFILE
# # --------------------------
# class FullProfileView(generics.RetrieveAPIView):
#     serializer_class = FullProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_object(self):
#         return self.request.user.profile
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response

from .models import Profile, TrustedContact, AadhaarVerification, VehicleDetails
from .serializers import (
    ProfileSerializer,            # <-- FIXED
    TrustedContactSerializer,
    AadhaarVerificationSerializer,
    VehicleDetailsSerializer,
    FullProfileSerializer,
)

# --------------------------
# USER PROFILE VIEW
# --------------------------
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer   # <-- FIXED
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile   # this is correct


# --------------------------
# TRUSTED CONTACTS CRUD
# --------------------------
class TrustedContactViewSet(viewsets.ModelViewSet):
    serializer_class = TrustedContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TrustedContact.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


# --------------------------
# AADHAAR VERIFY
# --------------------------
class AadhaarVerificationView(generics.RetrieveUpdateAPIView):
    serializer_class = AadhaarVerificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile = self.request.user.profile
        obj, _ = AadhaarVerification.objects.get_or_create(profile=profile)
        return obj


# --------------------------
# VEHICLE DETAILS
# --------------------------
class VehicleDetailsView(generics.RetrieveUpdateAPIView):
    serializer_class = VehicleDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile = self.request.user.profile
        obj, _ = VehicleDetails.objects.get_or_create(profile=profile)
        return obj


# --------------------------
# FULL PROFILE
# --------------------------
class FullProfileView(generics.RetrieveAPIView):
    serializer_class = FullProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
