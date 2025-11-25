# # # # from django.contrib import admin
# # # # from django.urls import path, include
# # # # from django.http import JsonResponse
# # # #
# # # # def home(request):
# # # #     return JsonResponse({"message": "TrackMate API running"})
# # # #
# # # # urlpatterns = [
# # # #     path("", home),
# # # #     path("admin/", admin.site.urls),
# # # #     path("api/auth/", include("auth_app.urls")),
# # # # ]
# # #
# # #
# # # from django.contrib import admin
# # # from django.urls import path, include
# # # from django.http import JsonResponse
# # #
# # #
# # # def home(request):
# # #     return JsonResponse({"message": "TrackMate API is running"})
# # #
# # #
# # # urlpatterns = [
# # #     path("", home),                           # Home URL
# # #     path("api/auth/", include("auth_app.urls")),  # Auth routes
# # #     path("admin/", admin.site.urls),          # Admin panel
# # # ]
# #
# #
# # from django.urls import path, include
# # from django.http import JsonResponse
# #
# # def home(request):
# #     return JsonResponse({"message": "TrackMate API running"})
# #
# # urlpatterns = [
# #     path("", home),
# #     path("api/auth/", include("auth_app.urls")),
# # ]
#
# from django.contrib import admin
# from django.urls import path, include
# from django.http import JsonResponse
#
# def home(request):
#     return JsonResponse({"message": "TrackMate API running"})
#
# urlpatterns = [
#     path("", home),
#
#     # ADMIN PANEL (You missed this!)
#     path("admin/", admin.site.urls),
#
#     # AUTH APIs
#     path("api/auth/", include("auth_app.urls")),
# ]

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    return JsonResponse({"message": "TrackMate API running"})

urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("api/auth/", include("auth_app.urls")),
    path("api/profile/", include("profile_app.urls")),
    path('api/', include('trips.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)