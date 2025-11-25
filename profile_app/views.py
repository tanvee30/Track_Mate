# # # from rest_framework import viewsets, permissions, generics
# # # from rest_framework.response import Response
# # #
# # # from .models import Profile, TrustedContact, AadhaarVerification, VehicleDetails
# # # from .serializers import (
# # #     ProfileSerializer,            # <-- FIXED
# # #     TrustedContactSerializer,
# # #     AadhaarVerificationSerializer,
# # #     VehicleDetailsSerializer,
# # #     FullProfileSerializer,
# # # )
# # #
# # # # --------------------------
# # # # USER PROFILE VIEW
# # # # --------------------------
# # # class ProfileView(generics.RetrieveUpdateAPIView):
# # #     serializer_class = ProfileSerializer   # <-- FIXED
# # #     permission_classes = [permissions.IsAuthenticated]
# # #
# # #     def get_object(self):
# # #         return self.request.user.profile   # this is correct
# # #
# # #
# # # # --------------------------
# # # # TRUSTED CONTACTS CRUD
# # # # --------------------------
# # # class TrustedContactViewSet(viewsets.ModelViewSet):
# # #     serializer_class = TrustedContactSerializer
# # #     permission_classes = [permissions.IsAuthenticated]
# # #
# # #     def get_queryset(self):
# # #         return TrustedContact.objects.filter(profile__user=self.request.user)
# # #
# # #     def perform_create(self, serializer):
# # #         serializer.save(profile=self.request.user.profile)
# # #
# # #
# # # # --------------------------
# # # # AADHAAR VERIFY
# # # # --------------------------
# # # class AadhaarVerificationView(generics.RetrieveUpdateAPIView):
# # #     serializer_class = AadhaarVerificationSerializer
# # #     permission_classes = [permissions.IsAuthenticated]
# # #
# # #     def get_object(self):
# # #         profile = self.request.user.profile
# # #         obj, _ = AadhaarVerification.objects.get_or_create(profile=profile)
# # #         return obj
# # #
# # #
# # # # --------------------------
# # # # VEHICLE DETAILS
# # # # --------------------------
# # # class VehicleDetailsView(generics.RetrieveUpdateAPIView):
# # #     serializer_class = VehicleDetailsSerializer
# # #     permission_classes = [permissions.IsAuthenticated]
# # #
# # #     def get_object(self):
# # #         profile = self.request.user.profile
# # #         obj, _ = VehicleDetails.objects.get_or_create(profile=profile)
# # #         return obj
# # #
# # #
# # # # --------------------------
# # # # FULL PROFILE
# # # # --------------------------
# # # class FullProfileView(generics.RetrieveAPIView):
# # #     serializer_class = FullProfileSerializer
# # #     permission_classes = [permissions.IsAuthenticated]
# # #
# # #     def get_object(self):
# # #         return self.request.user.profile
# # from rest_framework import viewsets, permissions, generics
# # from rest_framework.response import Response
# #
# # from .models import Profile, TrustedContact, AadhaarVerification, VehicleDetails
# # from .serializers import (
# #     ProfileSerializer,            # <-- FIXED
# #     TrustedContactSerializer,
# #     AadhaarVerificationSerializer,
# #     VehicleDetailsSerializer,
# #     FullProfileSerializer,
# # )
# #
# # # --------------------------
# # # USER PROFILE VIEW
# # # --------------------------
# # class ProfileView(generics.RetrieveUpdateAPIView):
# #     serializer_class = ProfileSerializer   # <-- FIXED
# #     permission_classes = [permissions.IsAuthenticated]
# #
# #     def get_object(self):
# #         return self.request.user.profile   # this is correct
# #
# #
# # # --------------------------
# # # TRUSTED CONTACTS CRUD
# # # --------------------------
# # class TrustedContactViewSet(viewsets.ModelViewSet):
# #     serializer_class = TrustedContactSerializer
# #     permission_classes = [permissions.IsAuthenticated]
# #
# #     def get_queryset(self):
# #         return TrustedContact.objects.filter(profile__user=self.request.user)
# #
# #     def perform_create(self, serializer):
# #         serializer.save(profile=self.request.user.profile)
# #
# #
# # # --------------------------
# # # AADHAAR VERIFY
# # # --------------------------
# # class AadhaarVerificationView(generics.RetrieveUpdateAPIView):
# #     serializer_class = AadhaarVerificationSerializer
# #     permission_classes = [permissions.IsAuthenticated]
# #
# #     def get_object(self):
# #         profile = self.request.user.profile
# #         obj, _ = AadhaarVerification.objects.get_or_create(profile=profile)
# #         return obj
# #
# #
# # # --------------------------
# # # VEHICLE DETAILS
# # # --------------------------
# # class VehicleDetailsView(generics.RetrieveUpdateAPIView):
# #     serializer_class = VehicleDetailsSerializer
# #     permission_classes = [permissions.IsAuthenticated]
# #
# #     def get_object(self):
# #         profile = self.request.user.profile
# #         obj, _ = VehicleDetails.objects.get_or_create(profile=profile)
# #         return obj
# #
# #
# # # --------------------------
# # # FULL PROFILE
# # # --------------------------
# # class FullProfileView(generics.RetrieveAPIView):
# #     serializer_class = FullProfileSerializer
# #     permission_classes = [permissions.IsAuthenticated]
# #
# #     def get_object(self):
# #         return self.request.user.profile
#
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from .models import Profile, TrustedContact, AadhaarVerification, VehicleDetails
# from .serializers import (
#     ProfileSerializer,
#     TrustedContactSerializer,
#     AadhaarSerializer,
#     VehicleSerializer,
# )
#
#
# # --------------------------- PROFILE ---------------------------
# class ProfileView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         """Get logged-in user's profile"""
#         profile, created = Profile.objects.get_or_create(user=request.user)
#         serializer = ProfileSerializer(profile)
#         return Response(serializer.data)
#
#     def put(self, request):
#         """Update logged-in user's profile"""
#         profile, created = Profile.objects.get_or_create(user=request.user)
#         serializer = ProfileSerializer(profile, data=request.data, partial=True)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# # ----------------------- TRUSTED CONTACTS -----------------------
# class TrustedContactView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         profile, created = Profile.objects.get_or_create(user=request.user)
#         serializer = TrustedContactSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save(profile=profile)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=400)
#
#
# # ----------------------- AADHAAR UPLOAD -------------------------
# class AadhaarView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         profile, created = Profile.objects.get_or_create(user=request.user)
#         aadhaar, _ = AadhaarVerification.objects.get_or_create(profile=profile)
#
#         serializer = AadhaarSerializer(aadhaar, data=request.data, partial=True)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#
#         return Response(serializer.errors, status=400)
#
#
# # ----------------------- VEHICLE REGISTRATION -------------------
# class VehicleView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         profile, created = Profile.objects.get_or_create(user=request.user)
#         serializer = VehicleSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save(profile=profile)
#             return Response(serializer.data, status=201)
#
#         return Response(serializer.errors, status=400)
#
#
# class ProfileSummaryView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         user = request.user
#
#         profile = Profile.objects.get(user=user)
#
#         data = {
#             "user": UserSerializer(user).data,
#             "profile": ProfileSerializer(profile).data,
#             "trusted_contacts": TrustedContactSerializer(
#                 profile.trusted_contacts.all(), many=True
#             ).data,
#             "aadhaar": AadhaarSerializer(
#                 getattr(profile, "aadhaar_verification", None)
#             ).data if hasattr(profile, "aadhaar_verification") else None,
#             "vehicles": VehicleSerializer(
#                 profile.vehicles.all(), many=True
#             ).data,
#         }
#
#         return Response(data, status=200)
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
