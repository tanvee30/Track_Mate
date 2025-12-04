

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
import random

from .models import EmailOTP
from .utils import send_otp_email

User = get_user_model()


def _generate_otp():
    return f"{random.randint(100000, 999999)}"


# -----------------------------
# SIGNUP -> create user (is_verified=False) and send OTP
# -----------------------------
@api_view(["POST"])
def signup(request):
    data = request.data
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not email or not username or not password:
        return Response({"error": "email, username, and password required"}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered"}, status=400)

    # create user but leave is_verified False
    user = User.objects.create_user(email=email, username=username, password=password)
    user.is_verified = False
    user.save()

    otp_code = _generate_otp()
    expires_at = timezone.now() + timedelta(minutes=10)

    EmailOTP.objects.create(
        email=email,
        code=otp_code,
        purpose="signup",
        used=False,
        expires_at=expires_at
    )

    send_otp_email(email, otp_code, "signup")
    return Response({"message": "Signup successful. OTP sent to email."}, status=201)


# -----------------------------
# VERIFY OTP
# -----------------------------
@api_view(["POST"])
def verify_otp(request):
    email = request.data.get("email")
    code = request.data.get("code") or request.data.get("otp")

    if not email or not code:
        return Response({"error": "email and code required"}, status=400)

    otp_obj = EmailOTP.objects.filter(email=email, code=code, purpose="signup", used=False).order_by("-created_at").first()
    if not otp_obj:
        return Response({"error": "Invalid or used OTP"}, status=400)

    if otp_obj.is_expired():
        return Response({"error": "OTP expired"}, status=400)

    otp_obj.used = True
    otp_obj.save()

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    user.is_verified = True
    user.save()
    return Response({"message": "Email verified successfully"})


# -----------------------------
# LOGIN
# -----------------------------
@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"error": "Email and password required"}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=400)

    if not user.check_password(password):
        return Response({"error": "Invalid credentials"}, status=400)

    if not user.is_verified:
        return Response({"error": "Email not verified"}, status=403)

    refresh = RefreshToken.for_user(user)
    return Response({"access": str(refresh.access_token), "refresh": str(refresh)})


# -----------------------------
# REFRESH TOKEN
# -----------------------------
@api_view(["POST"])
def refresh_token(request):
    token = request.data.get("refresh")
    if not token:
        return Response({"error": "Refresh token required"}, status=400)
    try:
        refresh = RefreshToken(token)
        return Response({"access": str(refresh.access_token)})
    except Exception:
        return Response({"error": "Invalid refresh token"}, status=400)


# -----------------------------
# FORGOT PASSWORD (send OTP)
# -----------------------------
@api_view(["POST"])
def forgot_password(request):
    email = request.data.get("email")
    if not email:
        return Response({"error": "Email required"}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Email not found"}, status=404)

    otp_code = _generate_otp()
    expires_at = timezone.now() + timedelta(minutes=10)

    EmailOTP.objects.create(
        email=email,
        code=otp_code,
        purpose="reset",
        used=False,
        expires_at=expires_at
    )

    send_otp_email(email, otp_code, "password reset")
    return Response({"message": "OTP sent for password reset"})


# -----------------------------
# RESET PASSWORD
# -----------------------------
@api_view(["POST"])
def reset_password(request):
    email = request.data.get("email")
    code = request.data.get("code")
    new_password = request.data.get("new_password")

    if not email or not code or not new_password:
        return Response({"error": "email, code and new_password required"}, status=400)

    otp_obj = EmailOTP.objects.filter(email=email, code=code, purpose="reset", used=False).order_by("-created_at").first()
    if not otp_obj:
        return Response({"error": "Invalid OTP"}, status=400)

    if otp_obj.is_expired():
        return Response({"error": "OTP expired"}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    user.set_password(new_password)
    user.save()

    otp_obj.used = True
    otp_obj.save()
    return Response({"message": "Password reset successful"})


# -----------------------------
# LOGOUT (Blacklist Refresh Token)
# -----------------------------
@api_view(["POST"])
def logout_view(request):
    refresh_token = request.data.get("refresh")

    if not refresh_token:
        return Response({"error": "Refresh token required"}, status=400)

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logged out successfully"}, status=200)
    except Exception:
        return Response({"error": "Invalid token"}, status=400)
