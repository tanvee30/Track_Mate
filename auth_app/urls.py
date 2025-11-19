# # # #
# # # #
# # # #
# # # # from django.urls import path
# # # # from . import views
# # # #
# # # # urlpatterns = [
# # # #     path("signup/", views.signup),
# # # #     path("verify/", views.verify_otp),
# # # #     path("login/", views.login),
# # # #     path("forgot-password/", views.forgot_password),
# # # #     path("reset-password/", views.reset_password),
# # # # ]
# # #
# # #
# # # from django.urls import path
# # # from . import views
# # #
# # # urlpatterns = [
# # #     path("signup/", views.signup),
# # #     path("verify-otp/", views.verify_otp),
# # #     path("login/", views.login),
# # #     path("refresh/", views.refresh_token),
# # #     path("forgot-password/", views.forgot_password),
# # #     path("reset-password/", views.reset_password),
# # # ]
# #
# # from django.urls import path
# # from . import views
# #
# # urlpatterns = [
# #     path("signup/", views.signup),
# #     path("verify-otp/", views.verify_otp),
# #     path("login/", views.login_view),
# #     path("refresh/", views.refresh_token),
# #     path("forgot-password/", views.forgot_password),
# #     path("reset-password/", views.reset_password),
# # ]
#
# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path("signup/", views.signup),
#     path("verify/", views.verify_otp),
#     # path("login/", views.login),
#     path("forgot-password/", views.forgot_password),
#     path("reset-password/", views.reset_password),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup),
    path("verify/", views.verify_otp),
    path("login/", views.login),
    path("refresh/", views.refresh_token),
    path("forgot-password/", views.forgot_password),
    path("reset-password/", views.reset_password),
]