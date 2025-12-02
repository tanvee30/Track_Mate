from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TripViewSet, PlannedTripViewSet,DailyStatsViewSet, VehicleViewSet,compare_routes

# Create router
router = DefaultRouter()

# Register viewsets
router.register(r'trips', TripViewSet, basename='trip')
router.register(r'planned-trips', PlannedTripViewSet, basename='planned-trip')
router.register(r'trips/stats', DailyStatsViewSet, basename='daily-stats')
router.register(r'vehicles', VehicleViewSet, basename='vehicles')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
    path("compare-routes/", compare_routes, name="compare-routes"),
]

# Available endpoints 
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
# GET /api/planned-trips/                     - List all planned trips
# POST /api/planned-trips/                    - Create new planned trip
# GET /api/planned-trips/{id}/                - Get specific planned trip details
# PUT/PATCH /api/planned-trips/{id}/          - Update planned trip
# DELETE /api/planned-trips/{id}/             - Delete planned trip
# GET /api/planned-trips/upcoming/            - Get upcoming trips
# POST /api/planned-trips/{id}/start_trip/    - Start the trip
# POST /api/planned-trips/{id}/cancel/        - Cancel the trip
# Daily Stats:
# - GET /api/trips/stats/daily-score/?date=2025-11-21
# - GET /api/trips/stats/calendar-stats/?month=11&year=2025
# - GET /api/trips/stats/monthly-chart/?month=11&year=2025

# Vehicle Management:
# - GET    /api/vehicles/          - List user's vehicles
# - POST   /api/vehicles/          - Create new vehicle
# - GET    /api/vehicles/{id}/     - Get vehicle details
# - PUT    /api/vehicles/{id}/     - Update vehicle
# - DELETE /api/vehicles/{id}/     - Delete vehicle


#/api/compare-routes/