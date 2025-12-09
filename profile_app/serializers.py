from rest_framework import serializers
from .models import Profile, TrustedContact, AadhaarVerification, VehicleDetails
from .models import InviteFriend


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "full_name",
            "profile_image",
            "bio",
            "home_location",
            "work_location",
            "last_shared_trip_link",   # ✅ NEW FIELD
        ]


class TrustedContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrustedContact
        fields = ["id", "name", "phone_number", "relation"]


class AadhaarVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AadhaarVerification
        fields = ["front_image", "back_image", "is_verified"]


class VehicleDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleDetails
        fields = ["id", "vehicle_number", "vehicle_model", "rc_image", "is_verified"]


class FullProfileSerializer(serializers.ModelSerializer):
    trusted_contacts = TrustedContactSerializer(many=True)
    aadhaar_verification = AadhaarVerificationSerializer()
    vehicles = VehicleDetailsSerializer(many=True)

    class Meta:
        model = Profile
        fields = [
            "full_name",
            "profile_image",
            "bio",
            "home_location",
            "work_location",
            "last_shared_trip_link",    # ✅ NEW FIELD
            "trusted_contacts",
            "aadhaar_verification",
            "vehicles",
        ]


class InviteFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteFriend
        fields = ['id', 'friend_email', 'message', 'created_at', 'accepted']
        read_only_fields = ['id', 'created_at', 'accepted']