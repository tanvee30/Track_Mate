from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    # add other fields as needed

    def __str__(self):
        return self.user.email


class TrustedContact(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class AadhaarVerification(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    aadhaar_number = models.CharField(max_length=12)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.profile.user.email} - {self.aadhaar_number}"


class VehicleDetails(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=50)

    def __str__(self):
        return self.vehicle_number


# ✅ Invite Friend Model
class InviteFriend(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="invites")
    friend_email = models.EmailField()
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.profile.user.email} invited {self.friend_email}"


# ✅ Signal to auto-create profile when user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()