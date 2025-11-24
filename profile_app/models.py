# from django.db import models
# from django.conf import settings
#
# User = settings.AUTH_USER_MODEL
#
#
# # ----------------------- USER PROFILE -----------------------
# class Profile(models.Model):
#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         related_name="profile"
#     )
#     full_name = models.CharField(max_length=100, blank=True, null=True)
#     profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
#     bio = models.TextField(blank=True, null=True)
#     home_location = models.CharField(max_length=255, blank=True, null=True)
#     work_location = models.CharField(max_length=255, blank=True, null=True)
#
#     def __str__(self):
#         return f"Profile - {self.user.email}"
#
#
# # ----------------------- TRUSTED CONTACTS -----------------------
# class TrustedContact(models.Model):
#     profile = models.ForeignKey(
#         Profile,
#         on_delete=models.CASCADE,
#         related_name="trusted_contacts",
#         null=True,        # allow migration on existing DB
#         blank=True
#     )
#     name = models.CharField(max_length=100)
#     phone_number = models.CharField(max_length=15)
#     relation = models.CharField(max_length=50, blank=True, null=True)
#
#     def __str__(self):
#         return f"{self.name} ({self.phone_number})"
#
#
# # ----------------------- AADHAAR -----------------------
# # class AadhaarVerification(models.Model):
# #     profile = models.ForeignKey(
# #         Profile,
# #         on_delete=models.CASCADE,
# #         related_name="aadhaar_verification",
# #         null=True,        # allow old rows to migrate
# #         blank=True
# #     )
# #     front_image = models.ImageField(upload_to="aadhaar/", null=True, blank=True)
# #     back_image = models.ImageField(upload_to="aadhaar/", null=True, blank=True)
# #     is_verified = models.BooleanField(default=False)
# #
# #     def __str__(self):
# #         if self.profile:
# #             return f"Aadhaar - {self.profile.user.email}"
# #         return "Aadhaar (No Profile)"
#
# class AadhaarVerification(models.Model):
#     profile = models.OneToOneField(
#         Profile,
#         on_delete=models.CASCADE,
#         related_name="aadhaar_verification",
#         null=True,
#         blank=True
#     )
#     front_image = models.ImageField(upload_to="aadhaar/", null=True, blank=True)
#     back_image = models.ImageField(upload_to="aadhaar/", null=True, blank=True)
#     is_verified = models.BooleanField(default=False)
#
#
# # ----------------------- VEHICLES -----------------------
# class VehicleDetails(models.Model):
#     profile = models.ForeignKey(
#         Profile,
#         on_delete=models.CASCADE,
#         related_name="vehicles",
#         null=True,       # <-- THIS FIXES YOUR MIGRATION ERROR
#         blank=True
#     )
#     vehicle_number = models.CharField(max_length=20)
#     vehicle_model = models.CharField(max_length=50)
#     rc_image = models.ImageField(upload_to="vehicles/")
#     is_verified = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.vehicle_number

from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


# ----------------------- USER PROFILE -----------------------
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    full_name = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    home_location = models.CharField(max_length=255, blank=True, null=True)
    work_location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Profile - {self.user.email}"


# ----------------------- TRUSTED CONTACTS -----------------------
class TrustedContact(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="trusted_contacts",
        null=True,        # allow migration on existing DB
        blank=True
    )
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    relation = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.phone_number})"


# ----------------------- AADHAAR -----------------------
# class AadhaarVerification(models.Model):
#     profile = models.ForeignKey(
#         Profile,
#         on_delete=models.CASCADE,
#         related_name="aadhaar_verification",
#         null=True,        # allow old rows to migrate
#         blank=True
#     )
#     front_image = models.ImageField(upload_to="aadhaar/", null=True, blank=True)
#     back_image = models.ImageField(upload_to="aadhaar/", null=True, blank=True)
#     is_verified = models.BooleanField(default=False)
#
#     def __str__(self):
#         if self.profile:
#             return f"Aadhaar - {self.profile.user.email}"
#         return "Aadhaar (No Profile)"

class AadhaarVerification(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name="aadhaar_verification",
        null=True,
        blank=True
    )
    front_image = models.ImageField(upload_to="aadhaar/", null=True, blank=True)
    back_image = models.ImageField(upload_to="aadhaar/", null=True, blank=True)
    is_verified = models.BooleanField(default=False)


# ----------------------- VEHICLES -----------------------
class VehicleDetails(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="vehicles",
        null=True,       # <-- THIS FIXES YOUR MIGRATION ERROR
        blank=True
    )
    vehicle_number = models.CharField(max_length=20)
    vehicle_model = models.CharField(max_length=50)
    rc_image = models.ImageField(upload_to="vehicles/")
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.vehicle_number