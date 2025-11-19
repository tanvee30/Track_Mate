from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q
import requests
from decimal import Decimal
from datetime import datetime

from .models import Trip, TripLocation
from .serializers import (
    TripSerializer, 
    TripStartSerializer, 
    TripEndSerializer,
    TripUpdateSerializer,
    TrackingPointSerializer,
    RoutePreviewSerializer,
    ManualTripSerializer
)


class TripViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Trip CRUD operations
    """
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return trips only for the authenticated user"""
        return Trip.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set the user when creating a trip"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'], url_path='start')
    def start_trip(self, request):
        """
        Start a new trip
        POST /api/trips/start/
        Body: {
            "start_latitude": 28.6139,
            "start_longitude": 77.2090,
            "start_location_name": "Connaught Place" (optional)
        }
        """
        serializer = TripStartSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user has any ongoing trip
        ongoing_trip = Trip.objects.filter(
            user=request.user,
            status='ongoing'
        ).first()
        
        if ongoing_trip:
            return Response(
                {
                    "error": "You already have an ongoing trip",
                    "ongoing_trip_id": ongoing_trip.id,
                    "trip_number": ongoing_trip.trip_number
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get reverse geocoded address if not provided
        start_location_name = serializer.validated_data.get('start_location_name')
        if not start_location_name:
            start_location_name = self.get_address_from_coordinates(
                serializer.validated_data['start_latitude'],
                serializer.validated_data['start_longitude']
            )
        
        # Create new trip
        trip = Trip.objects.create(
            user=request.user,
            start_latitude=serializer.validated_data['start_latitude'],
            start_longitude=serializer.validated_data['start_longitude'],
            start_location_name=start_location_name,
            start_time=serializer.validated_data.get('start_time', timezone.now()),
            status='ongoing'
        )
        
        # Create initial tracking point
        TripLocation.objects.create(
            trip=trip,
            latitude=trip.start_latitude,
            longitude=trip.start_longitude,
            accuracy=0.0,
            timestamp=trip.start_time
        )
        
        return Response(
            {
                "message": "Trip started successfully",
                "trip": TripSerializer(trip).data
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'], url_path='end')
    def end_trip(self, request, pk=None):
        """
        End an ongoing trip
        POST /api/trips/{trip_id}/end/
        Body: {
            "end_latitude": 28.6129,
            "end_longitude": 77.2295,
            "end_location_name": "India Gate" (optional),
            "mode_of_travel": "car" (optional),
            "trip_purpose": "work" (optional),
            "number_of_companions": 2 (optional)
        }
        """
        trip = self.get_object()
        
        if trip.status != 'ongoing':
            return Response(
                {"error": "This trip is not ongoing"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = TripEndSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get reverse geocoded address if not provided
        end_location_name = serializer.validated_data.get('end_location_name')
        if not end_location_name:
            end_location_name = self.get_address_from_coordinates(
                serializer.validated_data['end_latitude'],
                serializer.validated_data['end_longitude']
            )
        
        # Update trip
        trip.end_latitude = serializer.validated_data['end_latitude']
        trip.end_longitude = serializer.validated_data['end_longitude']
        trip.end_location_name = end_location_name
        trip.end_time = serializer.validated_data.get('end_time', timezone.now())
        trip.status = 'completed'
        
        # Update optional fields
        if 'mode_of_travel' in serializer.validated_data:
            trip.mode_of_travel = serializer.validated_data['mode_of_travel']
        if 'trip_purpose' in serializer.validated_data:
            trip.trip_purpose = serializer.validated_data['trip_purpose']
        if 'number_of_companions' in serializer.validated_data:
            trip.number_of_companions = serializer.validated_data['number_of_companions']
        
        # Calculate distance and duration
        trip.distance_km = trip.calculate_distance()
        trip.duration_minutes = trip.calculate_duration()
        
        # Calculate CO2 emissions if mode is set
        if trip.mode_of_travel:
            trip.co2_emission_kg = trip.calculate_co2_emission()
        
        trip.save()
        
        # Create final tracking point
        TripLocation.objects.create(
            trip=trip,
            latitude=trip.end_latitude,
            longitude=trip.end_longitude,
            accuracy=0.0,
            timestamp=trip.end_time
        )
        
        return Response(
            {
                "message": "Trip ended successfully",
                "trip": TripSerializer(trip).data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'], url_path='add-tracking-point')
    def add_tracking_point(self, request, pk=None):
        """
        Add GPS tracking point during ongoing trip
        POST /api/trips/{trip_id}/add-tracking-point/
        Body: {
            "latitude": 28.6140,
            "longitude": 77.2100,
            "accuracy": 10.5,
            "speed": 45.0 (optional)
        }
        """
        trip = self.get_object()
        
        if trip.status != 'ongoing':
            return Response(
                {"error": "Can only add tracking points to ongoing trips"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = TrackingPointSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tracking_point = TripLocation.objects.create(
            trip=trip,
            latitude=serializer.validated_data['latitude'],
            longitude=serializer.validated_data['longitude'],
            accuracy=serializer.validated_data['accuracy'],
            speed=serializer.validated_data.get('speed'),
            timestamp=serializer.validated_data.get('timestamp', timezone.now())
        )
        
        return Response(
            {
                "message": "Tracking point added successfully",
                "point_id": tracking_point.id
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['patch'], url_path='update-details')
    def update_details(self, request, pk=None):
        """
        Update trip details (mode, purpose, costs, etc.)
        PATCH /api/trips/{trip_id}/update-details/
        Body: {
            "mode_of_travel": "bus",
            "trip_purpose": "work",
            "ticket_cost": 50,
            "fuel_expense": 200
        }
        """
        trip = self.get_object()
        
        serializer = TripUpdateSerializer(trip, data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        
        # Recalculate CO2 if mode changed
        if 'mode_of_travel' in request.data and trip.distance_km:
            trip.co2_emission_kg = trip.calculate_co2_emission()
            trip.save()
        
        return Response(
            {
                "message": "Trip details updated successfully",
                "trip": TripSerializer(trip).data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'], url_path='ongoing')
    def get_ongoing_trip(self, request):
        """
        Get user's current ongoing trip
        GET /api/trips/ongoing/
        """
        ongoing_trip = Trip.objects.filter(
            user=request.user,
            status='ongoing'
        ).first()
        
        if not ongoing_trip:
            return Response(
                {"message": "No ongoing trip found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(
            TripSerializer(ongoing_trip).data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'], url_path='history')
    def trip_history(self, request):
        """
        Get user's trip history with filters
        GET /api/trips/history/?date_from=2025-01-01&date_to=2025-12-31&mode=car
        """
        trips = self.get_queryset().filter(status='completed')
        
        # Apply filters
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        mode = request.query_params.get('mode')
        purpose = request.query_params.get('purpose')
        
        if date_from:
            trips = trips.filter(start_time__date__gte=date_from)
        if date_to:
            trips = trips.filter(start_time__date__lte=date_to)
        if mode:
            trips = trips.filter(mode_of_travel=mode)
        if purpose:
            trips = trips.filter(trip_purpose=purpose)
        
        serializer = TripSerializer(trips, many=True)
        
        return Response(
            {
                "count": trips.count(),
                "trips": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    # SITUATION 2: MANUAL TRIP ENTRY
    
    @action(detail=False, methods=['post'], url_path='preview-route')
    def preview_route(self, request):
        """
        Get route preview without saving trip
        POST /api/trips/preview-route/
        """
        serializer = RoutePreviewSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = serializer.validated_data
        
        # Get coordinates
        start_lat, start_lng = self._get_coordinates(
            data.get('start_location'),
            data.get('start_latitude'),
            data.get('start_longitude')
        )
        
        end_lat, end_lng = self._get_coordinates(
            data.get('end_location'),
            data.get('end_latitude'),
            data.get('end_longitude')
        )
        
        if not all([start_lat, start_lng, end_lat, end_lng]):
            return Response(
                {"error": "Could not determine coordinates"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get route from Google
        route_data = self._get_route_from_google(
            start_lat, start_lng,
            end_lat, end_lng,
            data.get('mode_of_travel', 'car')
        )
        
        if not route_data:
            return Response(
                {"error": "Could not get route"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate estimated CO2
        distance_km = route_data.get('distance_km', 0)
        mode = data.get('mode_of_travel', 'car')
        
        emission_factors = {
            'walk': 0, 'bike': 0, 'car': 0.192, 'bus': 0.089,
            'train': 0.041, 'metro': 0.030, 'auto': 0.150,
            'bike_taxi': 0.084, 'other': 0.150,
        }
        estimated_co2 = distance_km * emission_factors.get(mode, 0)
        
        return Response(
            {
                "start_location": {
                    "latitude": start_lat,
                    "longitude": start_lng,
                    "address": self.get_address_from_coordinates(start_lat, start_lng)
                },
                "end_location": {
                    "latitude": end_lat,
                    "longitude": end_lng,
                    "address": self.get_address_from_coordinates(end_lat, end_lng)
                },
                "route": {
                    "distance_km": route_data.get('distance_km'),
                    "duration_minutes": route_data.get('duration_minutes'),
                    "polyline": route_data.get('polyline'),
                    "steps": route_data.get('steps', [])
                },
                "estimated_co2_kg": round(estimated_co2, 2),
                "mode_of_travel": mode
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'], url_path='create-manual')
    def create_manual_trip(self, request):
        """
        Create a trip by manually entering start and end locations
        POST /api/trips/create-manual/
        """
        serializer = ManualTripSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = serializer.validated_data
        
        # Step 1: Get coordinates if addresses were provided
        start_lat, start_lng = self._get_coordinates(
            data.get('start_location'),
            data.get('start_latitude'),
            data.get('start_longitude')
        )
        
        end_lat, end_lng = self._get_coordinates(
            data.get('end_location'),
            data.get('end_latitude'),
            data.get('end_longitude')
        )
        
        if not all([start_lat, start_lng, end_lat, end_lng]):
            return Response(
                {"error": "Could not determine coordinates. Please check your addresses."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Step 2: Get route from Google Directions API
        route_data = self._get_route_from_google(
            start_lat, start_lng,
            end_lat, end_lng,
            data.get('mode_of_travel', 'car')
        )
        
        if not route_data:
            return Response(
                {"error": "Could not get route from Google Maps"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Step 3: Get location names if not provided
        start_location_name = data.get('start_location')
        if not start_location_name:
            start_location_name = self.get_address_from_coordinates(start_lat, start_lng)
        
        end_location_name = data.get('end_location')
        if not end_location_name:
            end_location_name = self.get_address_from_coordinates(end_lat, end_lng)
        
        # Step 4: Create the trip
        trip_date = data.get('trip_date', timezone.now().date())
        trip_time = timezone.now().time()
        start_datetime = timezone.make_aware(datetime.combine(trip_date, trip_time))
        
        trip = Trip.objects.create(
            user=request.user,
            is_manual_entry=True,
            status='completed',
            
            # Start location
            start_latitude=start_lat,
            start_longitude=start_lng,
            start_location_name=start_location_name,
            start_time=start_datetime,
            
            # End location
            end_latitude=end_lat,
            end_longitude=end_lng,
            end_location_name=end_location_name,
            end_time=start_datetime,
            
            # Trip details
            mode_of_travel=data.get('mode_of_travel'),
            trip_purpose=data.get('trip_purpose'),
            number_of_companions=data.get('number_of_companions', 0),
            
            # Route data from Google
            route_polyline=route_data.get('polyline'),
            suggested_distance_km=route_data.get('distance_km'),
            suggested_duration_minutes=route_data.get('duration_minutes'),
            distance_km=route_data.get('distance_km'),
            duration_minutes=route_data.get('duration_minutes'),
        )
        
        # Calculate CO2 emissions
        trip.co2_emission_kg = trip.calculate_co2_emission()
        trip.save()
        
        return Response(
            {
                "message": "Manual trip created successfully",
                "trip": TripSerializer(trip).data,
                "route_info": {
                    "distance_km": route_data.get('distance_km'),
                    "duration_minutes": route_data.get('duration_minutes'),
                    "polyline": route_data.get('polyline'),
                    "steps": route_data.get('steps', [])
                }
            },
            status=status.HTTP_201_CREATED
        )
    
    # HELPER METHODS
    
    def get_address_from_coordinates(self, latitude, longitude):
        """
        Use Google Geocoding API to get address from coordinates
        """
        GEOCODING_API_KEY = "AIzaSyCIuctlZtylqWYpH8NZ_y8hdqQ0P5JhlHM"
        
        try:
            url = f"https://maps.googleapis.com/maps/api/geocode/json"
            params = {
                'latlng': f"{latitude},{longitude}",
                'key': GEOCODING_API_KEY
            }
            
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('results'):
                    return data['results'][0].get('formatted_address', 'Unknown Location')
            
            return 'Unknown Location'
        
        except Exception as e:
            print(f"Geocoding error: {str(e)}")
            return 'Unknown Location'
    
    def _get_coordinates(self, address, lat, lng):
        """Get coordinates from address or return provided coordinates"""
        
        if lat and lng:
            return float(lat), float(lng)
        
        if address:
            # Use Google Geocoding API
            GEOCODING_API_KEY = "AIzaSyCIuctlZtylqWYpH8NZ_y8hdqQ0P5JhlHM"
            
            try:
                url = "https://maps.googleapis.com/maps/api/geocode/json"
                params = {
                    'address': address,
                    'key': GEOCODING_API_KEY
                }
                
                response = requests.get(url, params=params, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('results'):
                        location = data['results'][0]['geometry']['location']
                        return location['lat'], location['lng']
            
            except Exception as e:
                print(f"Geocoding error: {str(e)}")
        
        return None, None
    
    def _get_route_from_google(self, start_lat, start_lng, end_lat, end_lng, mode):
        """Get route from Google Directions API"""
        
        DIRECTIONS_API_KEY = "AIzaSyDFTdr7PpBNjhE6yufD7mRfLu5yEoIV9SI"
        
        # Map our modes to Google's modes
        mode_mapping = {
            'car': 'driving',
            'bus': 'transit',
            'train': 'transit',
            'metro': 'transit',
            'walk': 'walking',
            'bike': 'bicycling',
            'auto': 'driving',
            'bike_taxi': 'driving',
            'other': 'driving'
        }
        
        google_mode = mode_mapping.get(mode, 'driving')
        
        try:
            url = "https://maps.googleapis.com/maps/api/directions/json"
            params = {
                'origin': f"{start_lat},{start_lng}",
                'destination': f"{end_lat},{end_lng}",
                'mode': google_mode,
                'key': DIRECTIONS_API_KEY
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'OK' and data.get('routes'):
                    route = data['routes'][0]
                    leg = route['legs'][0]
                    
                    # Extract route information
                    distance_meters = leg['distance']['value']
                    distance_km = round(distance_meters / 1000, 2)
                    
                    duration_seconds = leg['duration']['value']
                    duration_minutes = round(duration_seconds / 60)
                    
                    polyline = route['overview_polyline']['points']
                    
                    # Extract step-by-step directions
                    steps = []
                    for step in leg.get('steps', []):
                        steps.append({
                            'instruction': step.get('html_instructions', ''),
                            'distance': step['distance']['text'],
                            'duration': step['duration']['text']
                        })
                    
                    return {
                        'distance_km': distance_km,
                        'duration_minutes': duration_minutes,
                        'polyline': polyline,
                        'steps': steps
                    }
        
        except Exception as e:
            print(f"Directions API error: {str(e)}")
        
        return None
    

@action(detail=True, methods=['post'], url_path='add-note')
def add_note(self, request, pk=None):
    """
    Add notes/highlights after trip completion
    POST /api/trips/{trip_id}/add-note/
    Body: {
        "note_text": "Great trip! Traffic was smooth. Parking was easy to find."
    }
    """
    from .serializers import TripNoteSerializer
    from .models import TripNote
    
    trip = self.get_object()
    
    serializer = TripNoteSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    note = TripNote.objects.create(
        trip=trip,
        note_text=serializer.validated_data['note_text']
    )
    
    return Response(
        {
            "message": "Note added successfully",
            "note": TripNoteSerializer(note).data
        },
        status=status.HTTP_201_CREATED
    )

@action(detail=True, methods=['patch', 'delete'], url_path='note/(?P<note_id>[^/.]+)')
def manage_note(self, request, pk=None, note_id=None):
    """
    Update or delete a note
    PATCH  /api/trips/{trip_id}/note/{note_id}/  - Update note
    DELETE /api/trips/{trip_id}/note/{note_id}/  - Delete note
    """
    from .models import TripNote
    from .serializers import TripNoteSerializer
    
    trip = self.get_object()
    
    try:
        note = TripNote.objects.get(id=note_id, trip=trip)
    except TripNote.DoesNotExist:
        return Response(
            {"error": "Note not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'PATCH':
        serializer = TripNoteSerializer(note, data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        
        return Response(
            {
                "message": "Note updated successfully",
                "note": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    elif request.method == 'DELETE':
        note.delete()
        return Response(
            {"message": "Note deleted successfully"},
            status=status.HTTP_200_OK
        )
    

        