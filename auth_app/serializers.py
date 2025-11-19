#
#
#
# from rest_framework import serializers
# from .models import User
#
# class SignupSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#
# class VerifyOTPSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     code = serializers.CharField()
#
# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()
#
# class ForgotPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#
# class ResetPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     code = serializers.CharField()
#     new_password = serializers.CharField()

from rest_framework import serializers

class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
    new_password = serializers.CharField(write_only=True)