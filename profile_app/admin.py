
from django.contrib import admin
from .models import Profile, TrustedContact, AadhaarVerification, VehicleDetails, InviteFriend

# Registering models to appear in Django admin
admin.site.register(Profile)
admin.site.register(TrustedContact)
admin.site.register(AadhaarVerification)
admin.site.register(VehicleDetails)
admin.site.register(InviteFriend)  # InviteFriend will now appear under profile_app