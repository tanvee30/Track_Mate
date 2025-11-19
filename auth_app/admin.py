# # #
# # # from django.contrib import admin
# # # from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# # # from .models import User, EmailOTP
# # #
# # #
# # # @admin.register(User)
# # # class UserAdmin(BaseUserAdmin):
# # #     model = User
# # #
# # #     list_display = ("email", "is_verified", "is_staff", "is_superuser")
# # #     list_filter = ("is_staff", "is_superuser", "is_verified")
# # #
# # #     ordering = ("email",)
# # #     search_fields = ("email",)
# # #
# # #     fieldsets = (
# # #         (None, {"fields": ("email", "password")}),
# # #         ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "is_verified")}),
# # #         ("Important dates", {"fields": ("last_login",)}),
# # #     )
# # #
# # #     add_fieldsets = (
# # #         (None, {
# # #             "classes": ("wide",),
# # #             "fields": ("email", "password1", "password2"),
# # #         }),
# # #     )
# # #
# # #
# # # @admin.register(EmailOTP)
# # # class OTPAdmin(admin.ModelAdmin):
# # #     list_display = ("user", "code", "purpose", "used", "expires_at", "created_at")
# # #     search_fields = ("user__email", "code")
# # #     list_filter = ("purpose", "used")
# #
# #
# # from django.contrib import admin
# # from .models import User, EmailOTP
# #
# #
# # @admin.register(User)
# # class UserAdmin(admin.ModelAdmin):
# #     list_display = ("email", "username", "is_verified", "is_staff")
# #     search_fields = ("email", "username")
# #
# #
# # @admin.register(EmailOTP)
# # class EmailOTPAdmin(admin.ModelAdmin):
# #     list_display = ("user", "code", "purpose", "used", "expires_at")
#
# from django.contrib import admin
# from .models import User, EmailOTP
# from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
#
#
# @admin.register(User)
# class UserAdmin(DjangoUserAdmin):
#     list_display = ("email", "username", "is_verified", "is_staff", "is_superuser")
#     search_fields = ("email",)
#     ordering = ("email",)
#
#
# @admin.register(EmailOTP)
# class EmailOTPAdmin(admin.ModelAdmin):
#     list_display = ("email", "code", "purpose", "used", "created_at")
#     search_fields = ("email", "code")
#     list_filter = ("purpose", "used")


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, EmailOTP

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("email", "username", "is_verified", "is_staff", "is_superuser")
    search_fields = ("email", "username")
    ordering = ("email",)

@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ("email", "code", "purpose", "used", "created_at", "expires_at")
    search_fields = ("email", "code")
    list_filter = ("purpose", "used")