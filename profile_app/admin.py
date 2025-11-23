from django.contrib import admin
from .models import Profile, TrustedContact, AadhaarVerification, VehicleDetails

admin.site.register(Profile)
admin.site.register(TrustedContact)
admin.site.register(AadhaarVerification)
admin.site.register(VehicleDetails)
