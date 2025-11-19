# # # # # # from rest_framework.response import Response
# # # # # # from rest_framework.decorators import api_view
# # # # # # from django.contrib.auth import authenticate
# # # # # # from rest_framework_simplejwt.tokens import RefreshToken
# # # # # #
# # # # # # from .models import User, EmailOTP
# # # # # # from .serializers import *
# # # # # # from .utils import send_otp_email
# # # # # #
# # # # # # # ----------------------
# # # # # # # Signup → Send OTP
# # # # # # # ----------------------
# # # # # # @api_view(["POST"])
# # # # # # def signup(request):
# # # # # #     serializer = SignupSerializer(data=request.data)
# # # # # #     serializer.is_valid(raise_exception=True)
# # # # # #
# # # # # #     email = serializer.validated_data["email"]
# # # # # #
# # # # # #     user, created = User.objects.get_or_create(email=email)
# # # # # #
# # # # # #     otp = EmailOTP.create_otp(user, "signup")
# # # # # #     send_otp_email(user.email, otp.code)
# # # # # #
# # # # # #     return Response({"message": "OTP sent"})
# # # # # #
# # # # # #
# # # # # # # ----------------------
# # # # # # # Verify OTP
# # # # # # # ----------------------
# # # # # # @api_view(["POST"])
# # # # # # def verify_otp(request):
# # # # # #     serializer = VerifyOTPSerializer(data=request.data)
# # # # # #     serializer.is_valid(raise_exception=True)
# # # # # #
# # # # # #     email = serializer.validated_data["email"]
# # # # # #     code = serializer.validated_data["code"]
# # # # # #
# # # # # #     user = User.objects.get(email=email)
# # # # # #     otp = EmailOTP.objects.filter(user=user, code=code, purpose="signup").last()
# # # # # #
# # # # # #     if not otp or otp.expires_at < timezone.now():
# # # # # #         return Response({"error": "Invalid or expired OTP"}, status=400)
# # # # # #
# # # # # #     user.is_verified = True
# # # # # #     user.save()
# # # # # #     otp.delete()
# # # # # #
# # # # # #     return Response({"message": "OTP verified"})
# # # # # #
# # # # # #
# # # # # # # ----------------------
# # # # # # # Login
# # # # # # # ----------------------
# # # # # # @api_view(["POST"])
# # # # # # def login(request):
# # # # # #     serializer = LoginSerializer(data=request.data)
# # # # # #     serializer.is_valid(raise_exception=True)
# # # # # #
# # # # # #     email = serializer.validated_data["email"]
# # # # # #     password = serializer.validated_data["password"]
# # # # # #
# # # # # #     user = authenticate(email=email, password=password)
# # # # # #
# # # # # #     if not user:
# # # # # #         return Response({"error": "Invalid credentials"}, status=400)
# # # # # #
# # # # # #     if not user.is_verified:
# # # # # #         return Response({"error": "Verify your email first"}, status=400)
# # # # # #
# # # # # #     tokens = RefreshToken.for_user(user)
# # # # # #
# # # # # #     return Response({
# # # # # #         "access": str(tokens.access_token),
# # # # # #         "refresh": str(tokens),
# # # # # #     })
# # # # # #
# # # # # #
# # # # # # # ----------------------
# # # # # # # Forgot Password
# # # # # # # ----------------------
# # # # # # @api_view(["POST"])
# # # # # # def forgot_password(request):
# # # # # #     serializer = ForgotPasswordSerializer(data=request.data)
# # # # # #     serializer.is_valid(raise_exception=True)
# # # # # #
# # # # # #     email = serializer.validated_data["email"]
# # # # # #     user = User.objects.get(email=email)
# # # # # #
# # # # # #     otp = EmailOTP.create_otp(user, "reset")
# # # # # #     send_otp_email(user.email, otp.code)
# # # # # #
# # # # # #     return Response({"message": "OTP sent"})
# # # # # #
# # # # # #
# # # # # # # ----------------------
# # # # # # # Reset Password
# # # # # # # ----------------------
# # # # # # @api_view(["POST"])
# # # # # # def reset_password(request):
# # # # # #     serializer = ResetPasswordSerializer(data=request.data)
# # # # # #     serializer.is_valid(raise_exception=True)
# # # # # #
# # # # # #     email = serializer.validated_data["email"]
# # # # # #     code = serializer.validated_data["code"]
# # # # # #     new_password = serializer.validated_data["new_password"]
# # # # # #
# # # # # #     user = User.objects.get(email=email)
# # # # # #     otp = EmailOTP.objects.filter(user=user, code=code, purpose="reset").last()
# # # # # #
# # # # # #     if not otp or otp.expires_at < timezone.now():
# # # # # #         return Response({"error": "Invalid or expired OTP"}, status=400)
# # # # # #
# # # # # #     user.set_password(new_password)
# # # # # #     user.save()
# # # # # #     otp.delete()
# # # # # #
# # # # # #     return Response({"message": "Password reset successful"})
# # # # #
# # # # #
# # # # # from rest_framework.decorators import api_view
# # # # # from rest_framework.response import Response
# # # # # from rest_framework import status
# # # # # from django.utils import timezone
# # # # # from django.contrib.auth import authenticate
# # # # # from django.core.mail import send_mail
# # # # # from django.conf import settings
# # # # # from rest_framework_simplejwt.tokens import RefreshToken
# # # # #
# # # # # from .models import User, EmailOTP
# # # # # from datetime import timedelta
# # # # #
# # # # #
# # # # # # ---------------------------
# # # # # # SEND OTP HELPER
# # # # # # ---------------------------
# # # # # def send_otp_email(email, otp):
# # # # #     send_mail(
# # # # #         subject="Your OTP Code",
# # # # #         message=f"Your OTP is {otp}",
# # # # #         from_email=settings.DEFAULT_FROM_EMAIL,
# # # # #         recipient_list=[email],
# # # # #     )
# # # # #
# # # # #
# # # # # # ---------------------------
# # # # # # SIGNUP
# # # # # # ---------------------------
# # # # # @api_view(["POST"])
# # # # # def signup(request):
# # # # #     email = request.data.get("email")
# # # # #     username = request.data.get("username")
# # # # #     password = request.data.get("password")
# # # # #
# # # # #     if User.objects.filter(email=email).exists():
# # # # #         return Response({"error": "Email already exists"}, status=400)
# # # # #
# # # # #     user = User.objects.create_user(email=email, username=username, password=password)
# # # # #
# # # # #     otp = EmailOTP.generate_code()
# # # # #     EmailOTP.objects.create(
# # # # #         user=user,
# # # # #         code=otp,
# # # # #         purpose="signup",
# # # # #         expires_at=timezone.now() + timedelta(minutes=10)
# # # # #     )
# # # # #
# # # # #     send_otp_email(email, otp)
# # # # #
# # # # #     return Response({"message": "Signup successful. OTP sent to email"})
# # # # #
# # # # #
# # # # # # ---------------------------
# # # # # # VERIFY OTP
# # # # # # ---------------------------
# # # # # @api_view(["POST"])
# # # # # def verify_otp(request):
# # # # #     email = request.data.get("email")
# # # # #     otp = request.data.get("otp")
# # # # #
# # # # #     try:
# # # # #         user = User.objects.get(email=email)
# # # # #         otp_obj = EmailOTP.objects.filter(user=user, code=otp, used=False).latest("created_at")
# # # # #     except:
# # # # #         return Response({"error": "Invalid OTP"}, status=400)
# # # # #
# # # # #     if otp_obj.is_expired():
# # # # #         return Response({"error": "OTP expired"}, status=400)
# # # # #
# # # # #     otp_obj.used = True
# # # # #     otp_obj.save()
# # # # #
# # # # #     user.is_verified = True
# # # # #     user.save()
# # # # #
# # # # #     return Response({"message": "OTP verified successfully"})
# # # # #
# # # # #
# # # # # # ---------------------------
# # # # # # LOGIN
# # # # # # ---------------------------
# # # # # @api_view(["POST"])
# # # # # def login(request):
# # # # #     email = request.data.get("email")
# # # # #     password = request.data.get("password")
# # # # #
# # # # #     user = authenticate(email=email, password=password)
# # # # #
# # # # #     if not user:
# # # # #         return Response({"error": "Invalid credentials"}, status=400)
# # # # #
# # # # #     if not user.is_verified:
# # # # #         return Response({"error": "Email not verified"}, status=403)
# # # # #
# # # # #     refresh = RefreshToken.for_user(user)
# # # # #
# # # # #     return Response({
# # # # #         "access": str(refresh.access_token),
# # # # #         "refresh": str(refresh)
# # # # #     })
# # # # #
# # # # #
# # # # # # ---------------------------
# # # # # # REFRESH TOKEN
# # # # # # ---------------------------
# # # # # @api_view(["POST"])
# # # # # def refresh_token(request):
# # # # #     try:
# # # # #         refresh = RefreshToken(request.data.get("refresh"))
# # # # #         return Response({
# # # # #             "access": str(refresh.access_token)
# # # # #         })
# # # # #     except:
# # # # #         return Response({"error": "Invalid refresh token"}, status=400)
# # # # #
# # # # #
# # # # # # ---------------------------
# # # # # # FORGOT PASSWORD
# # # # # # ---------------------------
# # # # # @api_view(["POST"])
# # # # # def forgot_password(request):
# # # # #     email = request.data.get("email")
# # # # #
# # # # #     try:
# # # # #         user = User.objects.get(email=email)
# # # # #     except:
# # # # #         return Response({"error": "Email not found"}, status=404)
# # # # #
# # # # #     otp = EmailOTP.generate_code()
# # # # #
# # # # #     EmailOTP.objects.create(
# # # # #         user=user,
# # # # #         code=otp,
# # # # #         purpose="forgot",
# # # # #         expires_at=timezone.now() + timedelta(minutes=10)
# # # # #     )
# # # # #
# # # # #     send_otp_email(email, otp)
# # # # #
# # # # #     return Response({"message": "OTP sent for password reset"})
# # # # #
# # # # #
# # # # # # ---------------------------
# # # # # # RESET PASSWORD
# # # # # # ---------------------------
# # # # # @api_view(["POST"])
# # # # # def reset_password(request):
# # # # #     email = request.data.get("email")
# # # # #     otp = request.data.get("otp")
# # # # #     new_password = request.data.get("new_password")
# # # # #
# # # # #     try:
# # # # #         user = User.objects.get(email=email)
# # # # #         otp_obj = EmailOTP.objects.filter(
# # # # #             user=user,
# # # # #             code=otp,
# # # # #             purpose="forgot",
# # # # #             used=False
# # # # #         ).latest("created_at")
# # # # #     except:
# # # # #         return Response({"error": "Invalid OTP"}, status=400)
# # # # #
# # # # #     if otp_obj.is_expired():
# # # # #         return Response({"error": "OTP expired"}, status=400)
# # # # #
# # # # #     otp_obj.used = True
# # # # #     otp_obj.save()
# # # # #
# # # # #     user.set_password(new_password)
# # # # #     user.save()
# # # # #
# # # # #     return Response({"message": "Password reset successful"})
# # # #
# # # # import random
# # # # from datetime import timedelta
# # # # from django.utils import timezone
# # # # from django.contrib.auth import authenticate
# # # # from rest_framework.response import Response
# # # # from rest_framework.decorators import api_view
# # # #
# # # # from rest_framework_simplejwt.tokens import RefreshToken
# # # #
# # # # from .models import User, EmailOTP
# # # # from .utils import send_otp_email
# # # #
# # # #
# # # # # ------------------------------
# # # # # SIGNUP
# # # # # ------------------------------
# # # # @api_view(["POST"])
# # # # def signup(request):
# # # #     email = request.data.get("email")
# # # #     password = request.data.get("password")
# # # #     username = request.data.get("username")
# # # #
# # # #     if User.objects.filter(email=email).exists():
# # # #         return Response({"error": "Email already exists"}, status=400)
# # # #
# # # #     otp_code = str(random.randint(100000, 999999))
# # # #     EmailOTP.objects.create(email=email, code=otp_code, purpose="signup")
# # # #
# # # #     send_otp_email(email, otp_code, "signup")
# # # #
# # # #     return Response({"message": "OTP sent to email"})
# # # #
# # # #
# # # # # ------------------------------
# # # # # VERIFY OTP
# # # # # ------------------------------
# # # # @api_view(["POST"])
# # # # def verify_otp(request):
# # # #     email = request.data.get("email")
# # # #     code = request.data.get("code")
# # # #     password = request.data.get("password")
# # # #     username = request.data.get("username")
# # # #
# # # #     otp = EmailOTP.objects.filter(email=email, code=code, purpose="signup", used=False).first()
# # # #
# # # #     if not otp:
# # # #         return Response({"error": "Invalid or used OTP"}, status=400)
# # # #
# # # #     if otp.is_expired():
# # # #         return Response({"error": "OTP expired"}, status=400)
# # # #
# # # #     otp.used = True
# # # #     otp.save()
# # # #
# # # #     user = User.objects.create_user(email=email, username=username, password=password)
# # # #     user.is_verified = True
# # # #     user.save()
# # # #
# # # #     return Response({"message": "Signup successful"})
# # # #
# # # #
# # # # # ------------------------------
# # # # # LOGIN
# # # # # ------------------------------
# # # # @api_view(["POST"])
# # # # def login_view(request):
# # # #     email = request.data.get("email")
# # # #     password = request.data.get("password")
# # # #
# # # #     user = authenticate(email=email, password=password)
# # # #     if not user:
# # # #         return Response({"error": "Invalid credentials"}, status=400)
# # # #
# # # #     if not user.is_verified:
# # # #         return Response({"error": "Email not verified"}, status=400)
# # # #
# # # #     refresh = RefreshToken.for_user(user)
# # # #
# # # #     return Response({
# # # #         "access": str(refresh.access_token),
# # # #         "refresh": str(refresh),
# # # #     })
# # # #
# # # #
# # # # # ------------------------------
# # # # # REFRESH TOKEN
# # # # # ------------------------------
# # # # @api_view(["POST"])
# # # # def refresh_token(request):
# # # #     token = request.data.get("refresh")
# # # #     try:
# # # #         refresh = RefreshToken(token)
# # # #         return Response({"access": str(refresh.access_token)})
# # # #     except:
# # # #         return Response({"error": "Invalid refresh token"}, status=400)
# # # #
# # # #
# # # # # ------------------------------
# # # # # FORGOT PASSWORD
# # # # # ------------------------------
# # # # @api_view(["POST"])
# # # # def forgot_password(request):
# # # #     email = request.data.get("email")
# # # #
# # # #     if not User.objects.filter(email=email).exists():
# # # #         return Response({"error": "No account found"}, status=400)
# # # #
# # # #     otp_code = str(random.randint(100000, 999999))
# # # #     EmailOTP.objects.create(email=email, code=otp_code, purpose="reset")
# # # #
# # # #     send_otp_email(email, otp_code, "reset")
# # # #
# # # #     return Response({"message": "Reset OTP sent"})
# # # #
# # # #
# # # # # ------------------------------
# # # # # RESET PASSWORD
# # # # # ------------------------------
# # # # @api_view(["POST"])
# # # # def reset_password(request):
# # # #     email = request.data.get("email")
# # # #     code = request.data.get("code")
# # # #     new_password = request.data.get("new_password")
# # # #
# # # #     otp = EmailOTP.objects.filter(email=email, code=code, purpose="reset", used=False).first()
# # # #
# # # #     if not otp:
# # # #         return Response({"error": "Invalid OTP"}, status=400)
# # # #
# # # #     if otp.is_expired():
# # # #         return Response({"error": "OTP expired"}, status=400)
# # # #
# # # #     otp.used = True
# # # #     otp.save()
# # # #
# # # #     user = User.objects.get(email=email)
# # # #     user.set_password(new_password)
# # # #     user.save()
# # # #
# # # #     return Response({"message": "Password updated"})
# # #
# # #
# # # from rest_framework.decorators import api_view
# # # from rest_framework.response import Response
# # # from rest_framework_simplejwt.tokens import RefreshToken
# # # from .models import User
# # #
# # #
# # # @api_view(["POST"])
# # # def login(request):
# # #     email = request.data.get("email")
# # #     password = request.data.get("password")
# # #
# # #     if not email or not password:
# # #         return Response({"error": "Email and password required"}, status=400)
# # #
# # #     try:
# # #         user = User.objects.get(email=email)
# # #     except User.DoesNotExist:
# # #         return Response({"error": "User does not exist"}, status=404)
# # #
# # #     if not user.check_password(password):
# # #         return Response({"error": "Incorrect password"}, status=400)
# # #
# # #     if not user.is_verified:
# # #         return Response({"error": "Email not verified"}, status=403)
# # #
# # #     refresh = RefreshToken.for_user(user)
# # #
# # #     return Response({
# # #         "message": "Login successful",
# # #         "access": str(refresh.access_token),
# # #         "refresh": str(refresh)
# # #     })
# #
# # from rest_framework.decorators import api_view
# # from rest_framework.response import Response
# # from rest_framework import status
# # from django.utils import timezone
# # from django.contrib.auth import authenticate
# # from rest_framework_simplejwt.tokens import RefreshToken
# # from django.core.mail import send_mail
# # from .models import User, EmailOTP
# # import random
# #
# #
# # # -----------------------------
# # # Helper: Send OTP Email
# # # -----------------------------
# # def send_otp_email(email, code):
# #     send_mail(
# #         subject="Your OTP Code",
# #         message=f"Your OTP is {code}",
# #         from_email=None,
# #         recipient_list=[email],
# #         fail_silently=False
# #     )
# #
# #
# # # -----------------------------
# # # SIGNUP → Send OTP
# # # -----------------------------
# # @api_view(["POST"])
# # def signup(request):
# #     email = request.data.get("email")
# #     username = request.data.get("username")
# #     password = request.data.get("password")
# #
# #     if not email or not username or not password:
# #         return Response({"error": "Email, username, and password required"}, status=400)
# #
# #     if User.objects.filter(email=email).exists():
# #         return Response({"error": "Email already registered"}, status=400)
# #
# #     user = User.objects.create_user(
# #         email=email,
# #         username=username,
# #         password=password,
# #         is_verified=False
# #     )
# #
# #     # Create OTP
# #     otp_code = str(random.randint(100000, 999999))
# #     EmailOTP.objects.create(
# #         user=user,
# #         code=otp_code,
# #         purpose="signup",
# #         expires_at=timezone.now() + timezone.timedelta(minutes=5)
# #     )
# #
# #     send_otp_email(email, otp_code)
# #
# #     return Response({"message": "Signup successful. OTP sent to email."})
# #
# #
# # # -----------------------------
# # # VERIFY OTP
# # # -----------------------------
# # @api_view(["POST"])
# # def verify_otp(request):
# #     email = request.data.get("email")
# #     code = request.data.get("otp")
# #
# #     if not email or not code:
# #         return Response({"error": "Email and OTP required"}, status=400)
# #
# #     try:
# #         user = User.objects.get(email=email)
# #     except User.DoesNotExist:
# #         return Response({"error": "User not found"}, status=404)
# #
# #     try:
# #         otp = EmailOTP.objects.filter(user=user, purpose="signup").latest("created_at")
# #     except EmailOTP.DoesNotExist:
# #         return Response({"error": "OTP not found"}, status=404)
# #
# #     if otp.code != code:
# #         return Response({"error": "Incorrect OTP"}, status=400)
# #
# #     if otp.is_expired():
# #         return Response({"error": "OTP expired"}, status=400)
# #
# #     user.is_verified = True
# #     user.save()
# #
# #     return Response({"message": "Email verified successfully"})
# #
# #
# # # -----------------------------
# # # LOGIN
# # # -----------------------------
# # @api_view(["POST"])
# # def login(request):
# #     email = request.data.get("email")
# #     password = request.data.get("password")
# #
# #     if not email or not password:
# #         return Response({"error": "Email and password required"}, status=400)
# #
# #     try:
# #         user = User.objects.get(email=email)
# #     except User.DoesNotExist:
# #         return Response({"error": "User not found"}, status=404)
# #
# #     if not user.check_password(password):
# #         return Response({"error": "Incorrect password"}, status=400)
# #
# #     if not user.is_verified:
# #         return Response({"error": "Email not verified"}, status=403)
# #
# #     refresh = RefreshToken.for_user(user)
# #
# #     return Response({
# #         "message": "Login successful",
# #         "access": str(refresh.access_token),
# #         "refresh": str(refresh)
# #     })
# #
# #
# # # -----------------------------
# # # REFRESH TOKEN
# # # -----------------------------
# # @api_view(["POST"])
# # def refresh_token(request):
# #     token = request.data.get("refresh")
# #     if not token:
# #         return Response({"error": "Refresh token required"}, status=400)
# #
# #     try:
# #         refresh = RefreshToken(token)
# #         access = refresh.access_token
# #         return Response({"access": str(access)})
# #     except:
# #         return Response({"error": "Invalid refresh token"}, status=400)
# #
# #
# # # -----------------------------
# # # FORGOT PASSWORD
# # # -----------------------------
# # @api_view(["POST"])
# # def forgot_password(request):
# #     email = request.data.get("email")
# #
# #     if not email:
# #         return Response({"error": "Email required"}, status=400)
# #
# #     try:
# #         user = User.objects.get(email=email)
# #     except User.DoesNotExist:
# #         return Response({"error": "User not found"}, status=404)
# #
# #     otp_code = str(random.randint(100000, 999999))
# #     EmailOTP.objects.create(
# #         user=user,
# #         code=otp_code,
# #         purpose="reset",
# #         expires_at=timezone.now() + timezone.timedelta(minutes=5)
# #     )
# #
# #     send_otp_email(email, otp_code)
# #
# #     return Response({"message": "OTP sent for password reset"})
# #
# #
# # # -----------------------------
# # # RESET PASSWORD
# # # -----------------------------
# # @api_view(["POST"])
# # def reset_password(request):
# #     email = request.data.get("email")
# #     otp = request.data.get("otp")
# #     new_password = request.data.get("new_password")
# #
# #     if not email or not otp or not new_password:
# #         return Response({"error": "Email, OTP, and new password required"}, status=400)
# #
# #     try:
# #         user = User.objects.get(email=email)
# #     except User.DoesNotExist:
# #         return Response({"error": "User not found"}, status=404)
# #
# #     try:
# #         otp_obj = EmailOTP.objects.filter(user=user, purpose="reset").latest("created_at")
# #     except EmailOTP.DoesNotExist:
# #         return Response({"error": "OTP not found"}, status=404)
# #
# #     if otp_obj.code != otp:
# #         return Response({"error": "Incorrect OTP"}, status=400)
# #
# #     if otp_obj.is_expired():
# #         return Response({"error": "OTP expired"}, status=400)
# #
# #     user.set_password(new_password)
# #     user.save()
# #
# #     return Response({"message": "Password reset successful"})
#
#
# @api_view(["POST"])
# def signup(request):
#     email = request.data.get("email")
#     username = request.data.get("username")
#     password = request.data.get("password")
#
#     if not email or not username or not password:
#         return Response({"error": "email, username, and password required"}, status=400)
#
#     if User.objects.filter(email=email).exists():
#         return Response({"error": "Email already registered"}, status=400)
#
#     user = User.objects.create_user(
#         email=email,
#         username=username,
#         password=password,
#         is_verified=False
#     )
#
#     otp_code = str(random.randint(100000, 999999))
#
#     EmailOTP.objects.create(
#         email=email,
#         code=otp_code,
#         purpose="signup",
#         expires_at=timezone.now() + timezone.timedelta(minutes=5)
#     )
#
#     send_otp_email(email, otp_code)
#
#     return Response({"message": "Signup successful! OTP sent to email."})


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