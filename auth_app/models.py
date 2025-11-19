# # # # # #
# # # # # #
# # # # # # from django.db import models
# # # # # # from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# # # # # # from django.utils import timezone
# # # # # # from datetime import timedelta
# # # # # #
# # # # # #
# # # # # # # --------------------------
# # # # # # # USER MANAGER
# # # # # # # --------------------------
# # # # # # class UserManager(BaseUserManager):
# # # # # #     def create_user(self, email, password=None, **extra_fields):
# # # # # #         if not email:
# # # # # #             raise ValueError("Email is required")
# # # # # #
# # # # # #         email = self.normalize_email(email)
# # # # # #         user = self.model(email=email, **extra_fields)
# # # # # #
# # # # # #         if password:
# # # # # #             user.set_password(password)
# # # # # #
# # # # # #         user.save(using=self._db)
# # # # # #         return user
# # # # # #
# # # # # #     def create_superuser(self, email, password=None, **extra_fields):
# # # # # #         extra_fields.setdefault("is_staff", True)
# # # # # #         extra_fields.setdefault("is_superuser", True)
# # # # # #         extra_fields.setdefault("is_active", True)
# # # # # #         extra_fields.setdefault("is_verified", True)
# # # # # #
# # # # # #         return self.create_user(email, password, **extra_fields)
# # # # # #
# # # # # #
# # # # # # # --------------------------
# # # # # # # USER MODEL
# # # # # # # --------------------------
# # # # # # class User(AbstractBaseUser, PermissionsMixin):
# # # # # #     email = models.EmailField(unique=True)
# # # # # #     is_verified = models.BooleanField(default=False)
# # # # # #     is_staff = models.BooleanField(default=False)
# # # # # #     is_active = models.BooleanField(default=True)
# # # # # #
# # # # # #     USERNAME_FIELD = "email"
# # # # # #     REQUIRED_FIELDS = []
# # # # # #
# # # # # #     objects = UserManager()
# # # # # #
# # # # # #     def __str__(self):
# # # # # #         return self.email
# # # # # #
# # # # # #
# # # # # # # --------------------------
# # # # # # # HELPER FOR OTP EXPIRY
# # # # # # # --------------------------
# # # # # # def otp_expiry():
# # # # # #     return timezone.now() + timedelta(minutes=10)
# # # # # #
# # # # # #
# # # # # # # --------------------------
# # # # # # # EMAIL OTP MODEL
# # # # # # # --------------------------
# # # # # # class EmailOTP(models.Model):
# # # # # #     PURPOSE_CHOICES = [
# # # # # #         ("signup", "Signup"),
# # # # # #         ("reset", "Password Reset"),
# # # # # #     ]
# # # # # #
# # # # # #     user = models.ForeignKey(User, on_delete=models.CASCADE)
# # # # # #     code = models.CharField(max_length=6)
# # # # # #     purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICES)
# # # # # #     used = models.BooleanField(default=False)
# # # # # #
# # # # # #     created_at = models.DateTimeField(auto_now_add=True)
# # # # # #     expires_at = models.DateTimeField(default=otp_expiry)
# # # # # #
# # # # # #     def __str__(self):
# # # # # #         return f"{self.user.email} - {self.purpose}"
# # # # # #
# # # # #
# # # # #
# # # # # from django.db import models
# # # # # from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# # # # # from django.utils import timezone
# # # # # import random
# # # # #
# # # # #
# # # # # # ---------------------------
# # # # # # USER MANAGER
# # # # # # ---------------------------
# # # # # class UserManager(BaseUserManager):
# # # # #     def create_user(self, email, username, password=None, **extra_fields):
# # # # #         if not email:
# # # # #             raise ValueError("Email required")
# # # # #         if not username:
# # # # #             raise ValueError("Username required")
# # # # #
# # # # #         email = self.normalize_email(email)
# # # # #         user = self.model(email=email, username=username, **extra_fields)
# # # # #         user.set_password(password)
# # # # #         user.save()
# # # # #         return user
# # # # #
# # # # #     def create_superuser(self, email, username, password=None, **extra_fields):
# # # # #         extra_fields.setdefault("is_staff", True)
# # # # #         extra_fields.setdefault("is_superuser", True)
# # # # #
# # # # #         return self.create_user(email, username, password, **extra_fields)
# # # # #
# # # # #
# # # # # # ---------------------------
# # # # # # USER MODEL
# # # # # # ---------------------------
# # # # # class User(AbstractBaseUser, PermissionsMixin):
# # # # #     email = models.EmailField(unique=True)
# # # # #     username = models.CharField(max_length=150, unique=True)
# # # # #
# # # # #     is_active = models.BooleanField(default=True)
# # # # #     is_staff = models.BooleanField(default=False)
# # # # #     is_verified = models.BooleanField(default=False)
# # # # #
# # # # #     created_at = models.DateTimeField(auto_now_add=True)
# # # # #
# # # # #     USERNAME_FIELD = "email"
# # # # #     REQUIRED_FIELDS = ["username"]
# # # # #
# # # # #     objects = UserManager()
# # # # #
# # # # #     def __str__(self):
# # # # #         return self.email
# # # # #
# # # # #
# # # # # # ---------------------------
# # # # # # EMAIL OTP
# # # # # # ---------------------------
# # # # # class EmailOTP(models.Model):
# # # # #     PURPOSE_CHOICES = (
# # # # #         ("signup", "Signup Verification"),
# # # # #         ("forgot", "Forgot Password"),
# # # # #     )
# # # # #
# # # # #     user = models.ForeignKey(User, on_delete=models.CASCADE)
# # # # #     code = models.CharField(max_length=6)
# # # # #     purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICES)
# # # # #     used = models.BooleanField(default=False)
# # # # #     created_at = models.DateTimeField(auto_now_add=True)
# # # # #     expires_at = models.DateTimeField()
# # # # #
# # # # #     def is_expired(self):
# # # # #         return timezone.now() > self.expires_at
# # # # #
# # # # #     @staticmethod
# # # # #     def generate_code():
# # # # #         return str(random.randint(100000, 999999))
# # # # #
# # # # #     def __str__(self):
# # # # #         return f"{self.user.email} - {self.code}"
# # # #
# # # # from django.db import models
# # # # from django.contrib.auth.models import AbstractUser
# # # #
# # # # class User(AbstractUser):
# # # #     username = models.CharField(max_length=150)
# # # #     email = models.EmailField(unique=True)
# # # #
# # # #     USERNAME_FIELD = "email"
# # # #     REQUIRED_FIELDS = ["username"]
# # # #
# # # #     is_verified = models.BooleanField(default=False)
# # # #
# # # #     def __str__(self):
# # # #         return self.email
# # # #
# # # #
# # # # class EmailOTP(models.Model):
# # # #     email = models.EmailField()
# # # #     code = models.CharField(max_length=6)
# # # #     purpose = models.CharField(max_length=10)  # signup / reset
# # # #     used = models.BooleanField(default=False)
# # # #     created_at = models.DateTimeField(auto_now_add=True)
# # # #
# # # #     def is_expired(self):
# # # #         return (self.created_at + timedelta(minutes=10)) < timezone.now()
# # # #
# # # #     def __str__(self):
# # # #         return f"{self.email} - {self.code}"
# # #
# # #
# # # from django.db import models
# # # from django.utils import timezone
# # #
# # # class EmailOTP(models.Model):
# # #     email = models.EmailField()           # stores the user's email
# # #     code = models.CharField(max_length=6)
# # #     purpose = models.CharField(max_length=20, default="signup")
# # #     created_at = models.DateTimeField(auto_now_add=True)
# # #     expires_at = models.DateTimeField(default=timezone.now)  # MUST EXIST
# # #     used = models.BooleanField(default=False)
# # #
# # #     def __str__(self):
# # #         return f"{self.email} - {self.code}"
# #
# #
# # from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# # from django.db import models
# #
# # class User(AbstractBaseUser, PermissionsMixin):
# #     email = models.EmailField(unique=True)
# #     username = models.CharField(max_length=150, unique=True)
# #     is_verified = models.BooleanField(default=False)
# #     is_active = models.BooleanField(default=True)
# #     is_staff = models.BooleanField(default=False)
# #
# #     USERNAME_FIELD = "email"
# #     REQUIRED_FIELDS = ["username"]
# #
# #     objects = models.Manager()
# #
# #     def __str__(self):
# #         return self.email
# #
# # from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# # from django.db import models
# #
# #
# # class User(AbstractBaseUser, PermissionsMixin):
# #     email = models.EmailField(unique=True)
# #     username = models.CharField(max_length=150, unique=True)
# #     is_verified = models.BooleanField(default=False)
# #     is_active = models.BooleanField(default=True)
# #     is_staff = models.BooleanField(default=False)
# #
# #     USERNAME_FIELD = "email"
# #     REQUIRED_FIELDS = ["username"]
# #
# #     objects = models.Manager()
# #
# #     def __str__(self):
# #         return self.email
# #
# #
# # class EmailOTP(models.Model):
# #     email = models.EmailField()
# #     code = models.CharField(max_length=6)
# #     purpose = models.CharField(max_length=20)  # e.g. signup, login, reset
# #     used = models.BooleanField(default=False)
# #     created_at = models.DateTimeField(auto_now_add=True)
# #
# #     def __str__(self):
# #         return f"{self.email} - {self.code}"
#
#
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from django.db import models
# from django.utils import timezone
#
# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     username = models.CharField(max_length=150, unique=True)
#     is_verified = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["username"]
#
#     objects = models.Manager()
#
#     def __str__(self):
#         return self.email
#
#
# class EmailOTP(models.Model):
#     """
#     Simple OTP model that stores OTPs by email.
#     expires_at used to check expiry.
#     """
#     email = models.EmailField()
#     code = models.CharField(max_length=6)
#     purpose = models.CharField(max_length=20)  # e.g. signup, reset
#     used = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     expires_at = models.DateTimeField(default=timezone.now)
#
#     def is_expired(self):
#         return timezone.now() > self.expires_at
#
#     def __str__(self):
#         return f"{self.email} - {self.code}"

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        return self.create_user(email, username, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.email


class EmailOTP(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=20)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.email} - {self.code}"