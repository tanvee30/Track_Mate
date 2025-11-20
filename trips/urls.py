from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TripViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'', TripViewSet, basename='trip')  # ← Changed 'trips' to ''

urlpatterns = [
    path('', include(router.urls)),
]

# Available endpoints will now be:
# POST   /api/trips/start/                    - Start a new trip
# POST   /api/trips/{id}/end/                 - End a trip
# POST   /api/trips/{id}/add-tracking-point/  - Add GPS tracking point
# PATCH  /api/trips/{id}/update-details/      - Update trip details
# GET    /api/trips/ongoing/                  - Get current ongoing trip
# GET    /api/trips/history/                  - Get trip history with filters
# GET    /api/trips/                          - List all trips
# GET    /api/trips/{id}/                     - Get specific trip
# POST   /api/trips/create-manual/            - Create trip manually
# POST   /api/trips/preview-route/            - Preview route before saving
