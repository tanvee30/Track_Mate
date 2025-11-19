# # from django.core.mail import send_mail
# # from django.conf import settings
# #
# # def send_otp_email(email, code):
# #     send_mail(
# #         "Your Verification Code",
# #         f"Your verification code is {code}. It expires in 10 minutes.",
# #         settings.DEFAULT_FROM_EMAIL,
# #         [email],
# #         fail_silently=False,
# #     )
#
# from django.core.mail import send_mail
#
# def send_otp_email(email, otp, purpose="signup"):
#     subject = f"Your OTP for {purpose}"
#     message = f"Your OTP is: {otp}"
#     send_mail(subject, message, None, [email])

from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(email: str, otp: str, purpose: str = "signup"):
    subject = f"Your OTP for {purpose}"
    message = f"Your OTP code is: {otp}. It expires in 10 minutes."
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )