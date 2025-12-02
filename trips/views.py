from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q
import requests
from datetime import datetime

from .models import Trip, TripLocation, TripNote, PlannedTrip
from .serializers import (
    TripSerializer, TripStartSerializer, TripEndSerializer,
    TripUpdateSerializer, TrackingPointSerializer, TripNoteSerializer,
    RoutePreviewSerializer, ManualTripSerializer, PlannedTripSerializer,
    PlannedTripListSerializer, PlannedTripUpdateSerializer,
    StartPlannedTripSerializer, PlannedTripCreateSerializer,
)


class TripViewSet(viewsets.ModelViewSet):
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Trip.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'], url_path='start')
    def start_trip(self, request):
        serializer = TripStartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        ongoing_trip = Trip.objects.filter(user=request.user, status='ongoing').first()
        if ongoing_trip:
            return Response({
                "error": "You already have an ongoing trip",
                "ongoing_trip_id": ongoing_trip.id,
                "trip_number": ongoing_trip.trip_number
            }, status=status.HTTP_400_BAD_REQUEST)
        
        start_location_name = serializer.validated_data.get('start_location_name')
        if not start_location_name:
            start_location_name = self.get_address_from_coordinates(
                serializer.validated_data['start_latitude'],
                serializer.validated_data['start_longitude']
            )
        
        trip = Trip.objects.create(
            user=request.user,
            start_latitude=serializer.validated_data['start_latitude'],
            start_longitude=serializer.validated_data['start_longitude'],
            start_location_name=start_location_name,
            start_time=serializer.validated_data.get('start_time', timezone.now()),
            status='ongoing'
        )
        
        TripLocation.objects.create(
            trip=trip, latitude=trip.start_latitude, longitude=trip.start_longitude,
            accuracy=0.0, timestamp=trip.start_time
        )
        
        return Response({
            "message": "Trip started successfully",
            "trip": TripSerializer(trip).data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], url_path='end')
    def end_trip(self, request, pk=None):
        trip = self.get_object()
        if trip.status != 'ongoing':
            return Response({"error": "This trip is not ongoing"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = TripEndSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        end_location_name = serializer.validated_data.get('end_location_name')
        if not end_location_name:
            end_location_name = self.get_address_from_coordinates(
                serializer.validated_data['end_latitude'],
                serializer.validated_data['end_longitude']
            )
        
        trip.end_latitude = serializer.validated_data['end_latitude']
        trip.end_longitude = serializer.validated_data['end_longitude']
        trip.end_location_name = end_location_name
        trip.end_time = serializer.validated_data.get('end_time', timezone.now())
        trip.status = 'completed'
        
        if 'mode_of_travel' in serializer.validated_data:
            trip.mode_of_travel = serializer.validated_data['mode_of_travel']
        if 'trip_purpose' in serializer.validated_data:
            trip.trip_purpose = serializer.validated_data['trip_purpose']
        if 'number_of_companions' in serializer.validated_data:
            trip.number_of_companions = serializer.validated_data['number_of_companions']

        if 'fuel_expense' in serializer.validated_data:
             trip.fuel_expense = serializer.validated_data['fuel_expense']

        if 'parking_cost' in serializer.validated_data:
            trip.parking_cost = serializer.validated_data['parking_cost']
        if 'toll_cost' in serializer.validated_data:
            trip.toll_cost = serializer.validated_data['toll_cost']
        if 'ticket_cost' in serializer.validated_data:
            trip.ticket_cost = serializer.validated_data['ticket_cost']
    
        
        trip.distance_km = trip.calculate_distance()
        trip.duration_minutes = trip.calculate_duration()
        if trip.mode_of_travel:
            trip.co2_emission_kg = trip.calculate_co2_emission()
        trip.save()
        
        TripLocation.objects.create(
            trip=trip, latitude=trip.end_latitude, longitude=trip.end_longitude,
            accuracy=0.0, timestamp=trip.end_time
        )
        
        return Response({
            "message": "Trip ended successfully",
            "trip": TripSerializer(trip).data
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], url_path='add-tracking-point')
    def add_tracking_point(self, request, pk=None):
        trip = self.get_object()
        if trip.status != 'ongoing':
            return Response({"error": "Can only add tracking points to ongoing trips"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = TrackingPointSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        tracking_point = TripLocation.objects.create(
            trip=trip,
            latitude=serializer.validated_data['latitude'],
            longitude=serializer.validated_data['longitude'],
            accuracy=serializer.validated_data['accuracy'],
            speed=serializer.validated_data.get('speed'),
            timestamp=serializer.validated_data.get('timestamp', timezone.now())
        )
        
        return Response({
            "message": "Tracking point added successfully",
            "point_id": tracking_point.id
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['patch'], url_path='update-details')
    def update_details(self, request, pk=None):
        trip = self.get_object()
        serializer = TripUpdateSerializer(trip, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        if 'mode_of_travel' in request.data and trip.distance_km:
            trip.co2_emission_kg = trip.calculate_co2_emission()
            trip.save()
        
        return Response({
            "message": "Trip details updated successfully",
            "trip": TripSerializer(trip).data
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='ongoing')
    def get_ongoing_trip(self, request):
        ongoing_trip = Trip.objects.filter(user=request.user, status='ongoing').first()
        if not ongoing_trip:
            return Response({"message": "No ongoing trip found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(TripSerializer(ongoing_trip).data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='history')
    def trip_history(self, request):
        trips = self.get_queryset().filter(status='completed')
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
        return Response({"count": trips.count(), "trips": serializer.data}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='preview-route')
    def preview_route(self, request):
        serializer = RoutePreviewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        start_lat, start_lng = self._get_coordinates(data.get('start_location'), data.get('start_latitude'), data.get('start_longitude'))
        end_lat, end_lng = self._get_coordinates(data.get('end_location'), data.get('end_latitude'), data.get('end_longitude'))
        
        if not all([start_lat, start_lng, end_lat, end_lng]):
            return Response({"error": "Could not determine coordinates"}, status=status.HTTP_400_BAD_REQUEST)
        
        route_data = self._get_route_from_google(start_lat, start_lng, end_lat, end_lng, data.get('mode_of_travel', 'car'))
        if not route_data:
            return Response({"error": "Could not get route"}, status=status.HTTP_400_BAD_REQUEST)
        
        distance_km = route_data.get('distance_km', 0)
        mode = data.get('mode_of_travel', 'car')
        emission_factors = {'walk': 0, 'bike': 0, 'car': 0.192, 'bus': 0.089, 'train': 0.041, 'metro': 0.030, 'auto': 0.150, 'bike_taxi': 0.084, 'other': 0.150}
        estimated_co2 = distance_km * emission_factors.get(mode, 0)
        
        return Response({
            "start_location": {"latitude": start_lat, "longitude": start_lng, "address": self.get_address_from_coordinates(start_lat, start_lng)},
            "end_location": {"latitude": end_lat, "longitude": end_lng, "address": self.get_address_from_coordinates(end_lat, end_lng)},
            "route": {"distance_km": route_data.get('distance_km'), "duration_minutes": route_data.get('duration_minutes'), "polyline": route_data.get('polyline'), "steps": route_data.get('steps', [])},
            "estimated_co2_kg": round(estimated_co2, 2),
            "mode_of_travel": mode
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='create-manual')
    def create_manual_trip(self, request):
        serializer = ManualTripSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        start_lat, start_lng = self._get_coordinates(data.get('start_location'), data.get('start_latitude'), data.get('start_longitude'))
        end_lat, end_lng = self._get_coordinates(data.get('end_location'), data.get('end_latitude'), data.get('end_longitude'))
        
        if not all([start_lat, start_lng, end_lat, end_lng]):
            return Response({"error": "Could not determine coordinates. Please check your addresses."}, status=status.HTTP_400_BAD_REQUEST)
        
        route_data = self._get_route_from_google(start_lat, start_lng, end_lat, end_lng, data.get('mode_of_travel', 'car'))
        if not route_data:
            return Response({"error": "Could not get route from Google Maps"}, status=status.HTTP_400_BAD_REQUEST)
        
        start_location_name = data.get('start_location') or self.get_address_from_coordinates(start_lat, start_lng)
        end_location_name = data.get('end_location') or self.get_address_from_coordinates(end_lat, end_lng)
        
        trip_date = data.get('trip_date', timezone.now().date())
        trip_time = timezone.now().time()
        start_datetime = timezone.make_aware(datetime.combine(trip_date, trip_time))
        
        trip = Trip.objects.create(
            user=request.user, is_manual_entry=True, status='completed',
            start_latitude=start_lat, start_longitude=start_lng, start_location_name=start_location_name, start_time=start_datetime,
            end_latitude=end_lat, end_longitude=end_lng, end_location_name=end_location_name, end_time=start_datetime,
            mode_of_travel=data.get('mode_of_travel'), trip_purpose=data.get('trip_purpose'), number_of_companions=data.get('number_of_companions', 0),
            route_polyline=route_data.get('polyline'), suggested_distance_km=route_data.get('distance_km'), suggested_duration_minutes=route_data.get('duration_minutes'),
            distance_km=route_data.get('distance_km'), duration_minutes=route_data.get('duration_minutes'),
            toll_cost=data.get('toll_cost'),
            parking_cost=data.get('parking_cost'),
            fuel_expense=data.get('fuel_expense'),
            ticket_cost=data.get('ticket_cost'),
        )
        
        trip.co2_emission_kg = trip.calculate_co2_emission()
        trip.save()
        
        return Response({
            "message": "Manual trip created successfully",
            "trip": TripSerializer(trip).data,
            "route_info": {"distance_km": route_data.get('distance_km'), "duration_minutes": route_data.get('duration_minutes'), "polyline": route_data.get('polyline'), "steps": route_data.get('steps', [])}
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], url_path='add-note')
    def add_note(self, request, pk=None):
        trip = self.get_object()
        serializer = TripNoteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        note = TripNote.objects.create(trip=trip, note_text=serializer.validated_data['note_text'])
        return Response({"message": "Note added successfully", "note": TripNoteSerializer(note).data}, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['patch', 'delete'], url_path='note/(?P<note_id>[^/.]+)')
    def manage_note(self, request, pk=None, note_id=None):
        trip = self.get_object()
        try:
            note = TripNote.objects.get(id=note_id, trip=trip)
        except TripNote.DoesNotExist:
            return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'PATCH':
            serializer = TripNoteSerializer(note, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"message": "Note updated successfully", "note": serializer.data}, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            note.delete()
            return Response({"message": "Note deleted successfully"}, status=status.HTTP_200_OK)
    
    def get_address_from_coordinates(self, latitude, longitude):
        GEOCODING_API_KEY = "AIzaSyCIuctlZtylqWYpH8NZ_y8hdqQ0P5JhlHM"
        try:
            url = "https://maps.googleapis.com/maps/api/geocode/json"
            params = {'latlng': f"{latitude},{longitude}", 'key': GEOCODING_API_KEY}
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
        if lat and lng:
            return float(lat), float(lng)
        if address:
            GEOCODING_API_KEY = "AIzaSyCIuctlZtylqWYpH8NZ_y8hdqQ0P5JhlHM"
            try:
                url = "https://maps.googleapis.com/maps/api/geocode/json"
                params = {'address': address, 'key': GEOCODING_API_KEY}
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
        DIRECTIONS_API_KEY = "AIzaSyDFTdr7PpBNjhE6yufD7mRfLu5yEoIV9SI"
        mode_mapping = {'car': 'driving', 'bus': 'transit', 'train': 'transit', 'metro': 'transit', 'walk': 'walking', 'bike': 'bicycling', 'auto': 'driving', 'bike_taxi': 'driving', 'other': 'driving'}
        google_mode = mode_mapping.get(mode, 'driving')
        
        try:
            url = "https://maps.googleapis.com/maps/api/directions/json"
            params = {'origin': f"{start_lat},{start_lng}", 'destination': f"{end_lat},{end_lng}", 'mode': google_mode, 'key': DIRECTIONS_API_KEY}
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'OK' and data.get('routes'):
                    route = data['routes'][0]
                    leg = route['legs'][0]
                    distance_km = round(leg['distance']['value'] / 1000, 2)
                    duration_minutes = round(leg['duration']['value'] / 60)
                    polyline = route['overview_polyline']['points']
                    steps = [{'instruction': step.get('html_instructions', ''), 'distance': step['distance']['text'], 'duration': step['duration']['text']} for step in leg.get('steps', [])]
                    return {'distance_km': distance_km, 'duration_minutes': duration_minutes, 'polyline': polyline, 'steps': steps}
        except Exception as e:
            print(f"Directions API error: {str(e)}")
        return None


class PlannedTripViewSet(viewsets.ModelViewSet):
    serializer_class = PlannedTripSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PlannedTrip.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PlannedTripListSerializer
        elif self.action in ['update', 'partial_update']:
            return PlannedTripUpdateSerializer
        elif self.action == 'start_trip':
            return StartPlannedTripSerializer
        elif self.action == 'create':
            return PlannedTripCreateSerializer
        return PlannedTripSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = PlannedTripCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        start_lat, start_lng = self._get_coordinates(data.get('start_location_address'), data.get('start_latitude'), data.get('start_longitude'))
        dest_lat, dest_lng = self._get_coordinates(data.get('destination_address'), data.get('destination_latitude'), data.get('destination_longitude'))
        
        if not all([start_lat, start_lng, dest_lat, dest_lng]):
            return Response({"error": "Could not determine coordinates from provided addresses"}, status=status.HTTP_400_BAD_REQUEST)
        
        start_address = data.get('start_location_address') or self._get_address_from_coordinates(start_lat, start_lng)
        dest_address = data.get('destination_address') or self._get_address_from_coordinates(dest_lat, dest_lng)
        
        route_data = None
        if data.get('auto_calculate_route', True):
            route_data = self._get_route_from_google(start_lat, start_lng, dest_lat, dest_lng, data.get('mode_of_travel', 'car'))
        
        planned_trip = PlannedTrip.objects.create(
            user=request.user, trip_name=data['trip_name'], description=data.get('description', ''),
            planned_start_date=data['planned_start_date'], planned_end_date=data.get('planned_end_date'),
            start_location_name=data['start_location_name'], start_location_address=start_address,
            start_latitude=start_lat, start_longitude=start_lng,
            destination_name=data['destination_name'], destination_address=dest_address,
            destination_latitude=dest_lat, destination_longitude=dest_lng,
            mode_of_travel=data.get('mode_of_travel'), trip_purpose=data.get('trip_purpose'),
            number_of_companions=data.get('number_of_companions', 0), estimated_budget=data.get('estimated_budget'),
            waypoints=data.get('waypoints'), notes=data.get('notes', ''),
            estimated_distance_km=route_data.get('distance_km') if route_data else None,
            estimated_duration_minutes=route_data.get('duration_minutes') if route_data else None,
            route_polyline=route_data.get('polyline') if route_data else None,
        )
        
        response_data = PlannedTripSerializer(planned_trip).data
        if route_data:
            response_data['route_preview'] = {'distance_km': route_data.get('distance_km'), 'duration_minutes': route_data.get('duration_minutes'), 'polyline': route_data.get('polyline'), 'steps': route_data.get('steps', [])}
        
        return Response({"message": "Planned trip created successfully", "trip": response_data}, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        if request.query_params.get('upcoming', '').lower() == 'true':
            queryset = queryset.filter(planned_start_date__gt=timezone.now(), status='planned')
        
        if request.query_params.get('past', '').lower() == 'true':
            queryset = queryset.filter(planned_start_date__lt=timezone.now(), status='planned')
        
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(Q(trip_name__icontains=search) | Q(description__icontains=search) | Q(start_location_name__icontains=search) | Q(destination_name__icontains=search))
        
        start_from = request.query_params.get('start_from')
        start_to = request.query_params.get('start_to')
        if start_from:
            queryset = queryset.filter(planned_start_date__gte=start_from)
        if start_to:
            queryset = queryset.filter(planned_start_date__lte=start_to)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'planned':
            return Response({'error': 'Cannot delete trip that has been started or completed.'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response({"message": "Planned trip deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        queryset = self.get_queryset().filter(planned_start_date__gt=timezone.now(), status='planned').order_by('planned_start_date')
        serializer = PlannedTripListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    # @action(detail=False, methods=['get'])
    # def summary(self, request):
    #     queryset = self.get_queryset()
    #     now = timezone.now()
    #     summary = {
    #         'total_planned': queryset.filter(status='planned').count(),
    #         'upcoming': queryset.filter(planned_start_date__gt=now, status='planned').count(),
    #         'past_planned': queryset.filter(planned_start_date__lt=now, status='planned').count(),
    #         'started': queryset.filter(status='started').count(),
    #         'completed': queryset.filter(status='completed').count(),
    #         'cancelled': queryset.filter(status='cancelled').count(),
    #     }
    #     return Response(summary)
    
    @action(detail=True, methods=['post'])
    def start_trip(self, request, pk=None):
        planned_trip = self.get_object()
        if planned_trip.status != 'planned':
            return Response({'error': 'This trip has already been started or is not in planned status.'}, status=status.HTTP_400_BAD_REQUEST)
        
        ongoing_trip = Trip.objects.filter(user=request.user, status='ongoing').first()
        if ongoing_trip:
            return Response({"error": "You already have an ongoing trip. End it before starting a new one.", "ongoing_trip_id": ongoing_trip.id, "trip_number": ongoing_trip.trip_number}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = StartPlannedTripSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        start_lat = serializer.validated_data.get('start_latitude', planned_trip.start_latitude)
        start_lon = serializer.validated_data.get('start_longitude', planned_trip.start_longitude)
        start_location_name = serializer.validated_data.get('start_location_name', planned_trip.start_location_name)
        
        try:
            actual_trip = Trip.objects.create(
                user=request.user, start_latitude=start_lat, start_longitude=start_lon,
                start_location_name=start_location_name, start_time=timezone.now(), status='ongoing',
                mode_of_travel=planned_trip.mode_of_travel, trip_purpose=planned_trip.trip_purpose,
                number_of_companions=planned_trip.number_of_companions,
            )
            
            TripLocation.objects.create(trip=actual_trip, latitude=start_lat, longitude=start_lon, accuracy=0.0, timestamp=actual_trip.start_time)
            
            planned_trip.status = 'started'
            planned_trip.actual_trip = actual_trip
            planned_trip.save()
            
            return Response({'message': 'Trip started successfully! GPS tracking is now active.', 'planned_trip_id': planned_trip.id, 'trip': TripSerializer(actual_trip).data, 'instructions': {'next_step': 'Use POST /api/trips/{id}/add-tracking-point/ to add GPS points', 'end_trip': 'Use POST /api/trips/{id}/end/ when trip is complete'}}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Failed to start trip: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        planned_trip = self.get_object()
        if planned_trip.status != 'planned':
            return Response({'error': 'Can only cancel trips in planned status.'}, status=status.HTTP_400_BAD_REQUEST)
        planned_trip.status = 'cancelled'
        planned_trip.save()
        return Response({'message': 'Trip cancelled successfully', 'trip': PlannedTripSerializer(planned_trip).data})
    
    # @action(detail=True, methods=['post'])
    # def duplicate(self, request, pk=None):
        
    #     original_trip = self.get_object()
    #     new_start_date = request.data.get('planned_start_date')
    #     if not new_start_date:
    #         return Response({'error': 'planned_start_date is required'}, status=status.HTTP_400_BAD_REQUEST)
        
    #     duplicate = PlannedTrip.objects.create(
    #         user=request.user,
    #         trip_name=f"{original_trip.trip_name} (Copy)",
    #         description=original_trip.description,
    #         planned_start_date=new_start_date,
    #         planned_end_date=request.data.get('planned_end_date'),
    #         start_location_name=original_trip.start_location_name,
    #         start_location_address=original_trip.start_location_address,
    #         start_latitude=original_trip.start_latitude,
    #         start_longitude=original_trip.start_longitude,
    #         destination_name=original_trip.destination_name,
    #         destination_address=original_trip.destination_address,
    #         destination_latitude=original_trip.destination_latitude,
    #         destination_longitude=original_trip.destination_longitude,
    #         estimated_distance_km=original_trip.estimated_distance_km,
    #         estimated_duration_minutes=original_trip.estimated_duration_minutes,
    #         waypoints=original_trip.waypoints,
    #         route_polyline=original_trip.route_polyline,
    #         mode_of_travel=original_trip.mode_of_travel,
    #         trip_purpose=original_trip.trip_purpose,
    #         number_of_companions=original_trip.number_of_companions,
    #         estimated_budget=original_trip.estimated_budget,
    #         notes=original_trip.notes
    #     )
        
        
    #     serializer = PlannedTripSerializer(duplicate)
    #     return Response({"message": "Trip duplicated successfully", "trip": serializer.data}, status=status.HTTP_201_CREATED)
    
    def _get_coordinates(self, address, lat, lng):
        if lat and lng:
            return float(lat), float(lng)
        if address:
            GEOCODING_API_KEY = "AIzaSyCIuctlZtylqWYpH8NZ_y8hdqQ0P5JhlHM"
            try:
                url = "https://maps.googleapis.com/maps/api/geocode/json"
                params = {'address': address, 'key': GEOCODING_API_KEY}
                response = requests.get(url, params=params, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('results'):
                        location = data['results'][0]['geometry']['location']
                        return location['lat'], location['lng']
            except Exception as e:
                print(f"Geocoding error: {str(e)}")
        return None, None
    
    def _get_address_from_coordinates(self, latitude, longitude):
        GEOCODING_API_KEY = "AIzaSyCIuctlZtylqWYpH8NZ_y8hdqQ0P5JhlHM"
        try:
            url = "https://maps.googleapis.com/maps/api/geocode/json"
            params = {'latlng': f"{latitude},{longitude}", 'key': GEOCODING_API_KEY}
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('results'):
                    return data['results'][0].get('formatted_address', 'Unknown Location')
            return 'Unknown Location'
        except Exception as e:
            print(f"Geocoding error: {str(e)}")
            return 'Unknown Location'
    
    def _get_route_from_google(self, start_lat, start_lng, end_lat, end_lng, mode):
        DIRECTIONS_API_KEY = "AIzaSyDFTdr7PpBNjhE6yufD7mRfLu5yEoIV9SI"
        mode_mapping = {'car': 'driving', 'bus': 'transit', 'train': 'transit', 'metro': 'transit', 'walk': 'walking', 'bike': 'bicycling', 'auto': 'driving', 'bike_taxi': 'driving', 'other': 'driving'}
        google_mode = mode_mapping.get(mode, 'driving')
        
        try:
            url = "https://maps.googleapis.com/maps/api/directions/json"
            params = {'origin': f"{start_lat},{start_lng}", 'destination': f"{end_lat},{end_lng}", 'mode': google_mode, 'key': DIRECTIONS_API_KEY}
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'OK' and data.get('routes'):
                    route = data['routes'][0]
                    leg = route['legs'][0]
                    distance_km = round(leg['distance']['value'] / 1000, 2)
                    duration_minutes = round(leg['duration']['value'] / 60)
                    polyline = route['overview_polyline']['points']
                    steps = [{'instruction': step.get('html_instructions', ''), 'distance': step['distance']['text'], 'duration': step['duration']['text']} for step in leg.get('steps', [])]
                    return {'distance_km': distance_km, 'duration_minutes': duration_minutes, 'polyline': polyline, 'steps': steps}
        except Exception as e:
            print(f"Directions API error: {str(e)}")
        return None
    


# ==================== views.py ====================
# Add this ViewSet to your existing views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
import calendar
from decimal import Decimal

from .models import Trip, DailyStats, Vehicle
from .serializers import (
    DailyScoreSerializer, CalendarStatsSerializer, 
    MonthlyChartSerializer, VehicleSerializer
)


class DailyStatsViewSet(viewsets.ViewSet):
    """ViewSet for daily statistics and analytics"""
    permission_classes = [IsAuthenticated]
    
    def _calculate_score(self, distance, co2, fuel_cost, trips_count):
        """
        Calculate daily score (0-100) based on multiple factors
        Lower emissions and cost = higher score
        More trips = more engagement bonus
        """
        if distance == 0:
            return 0
        
        # Normalize metrics (adjust these thresholds based on your app's typical usage)
        # Example thresholds for a "good" day:
        # - Distance: 20-50 km is typical
        # - CO2: < 2000g per day is good
        # - Cost: < 200 per day is good
        
        # Efficiency score (40 points max)
        # Lower CO2 per km = higher score
        co2_per_km = (co2 / distance) if distance > 0 else 0
        if co2_per_km < 50:  # Very efficient (walk, bike, public transport)
            efficiency_score = 40
        elif co2_per_km < 100:  # Good
            efficiency_score = 30
        elif co2_per_km < 150:  # Average
            efficiency_score = 20
        else:  # Needs improvement
            efficiency_score = 10
        
        # Cost efficiency score (30 points max)
        cost_per_km = (fuel_cost / distance) if distance > 0 else 0
        if cost_per_km < 5:  # Very economical
            cost_score = 30
        elif cost_per_km < 10:  # Good
            cost_score = 20
        elif cost_per_km < 15:  # Average
            cost_score = 15
        else:  # Expensive
            cost_score = 5
        
        # Activity bonus (30 points max)
        # More trips tracked = more engagement
        activity_score = min(30, trips_count * 10)
        
        total_score = int(efficiency_score + cost_score + activity_score)
        return min(100, max(0, total_score))
    
    def _calculate_emissions_from_trip(self, trip):
        """Calculate CO2 emissions for a trip in grams"""
        if not trip.distance_km:
            return 0
        
        distance = float(trip.distance_km)
        
        # Check if user has a vehicle configured
        vehicle = Vehicle.objects.filter(user=trip.user, is_active=True).first()
        
        # If vehicle exists and trip mode matches vehicle type, use vehicle's emissions
        if vehicle and trip.mode_of_travel in ['car', 'bike', 'scooter']:
            return distance * vehicle.emissions_factor
        
        # Otherwise use the trip's calculated CO2 or standard factors
        if trip.co2_emission_kg:
            return float(trip.co2_emission_kg) * 1000  # Convert kg to grams
        
        # Fallback to mode-based calculation
        emission_factors = {
            'walk': 0, 'bike': 0, 'car': 120, 'bus': 89,
            'train': 41, 'metro': 30, 'auto': 150,
            'bike_taxi': 84, 'other': 150,
        }
        factor = emission_factors.get(trip.mode_of_travel, 120)
        return distance * factor
    
    def _calculate_fuel_cost_from_trip(self, trip):
        """Calculate fuel cost for a trip"""
        # If trip already has fuel_expense, use that
        if trip.fuel_expense:
            return float(trip.fuel_expense)
        
        if not trip.distance_km:
            return 0
        
        distance = float(trip.distance_km)
        
        # Check if user has a vehicle configured
        vehicle = Vehicle.objects.filter(user=trip.user, is_active=True).first()
        
        if vehicle and trip.mode_of_travel in ['car', 'bike', 'scooter']:
            # Calculate based on vehicle's fuel efficiency
            liters_used = distance / vehicle.fuel_efficiency
            return liters_used * float(vehicle.fuel_price_per_liter)
        
        # Fallback: estimate based on mode
        cost_per_km = {
            'walk': 0, 'bike': 0, 'car': 8, 'bus': 3,
            'train': 2, 'metro': 2.5, 'auto': 12,
            'bike_taxi': 10, 'other': 8,
        }
        rate = cost_per_km.get(trip.mode_of_travel, 8)
        return distance * rate
    
    def _get_or_calculate_daily_stats(self, user, date):
        """Get cached stats or calculate fresh from trips"""
        try:
            stats = DailyStats.objects.get(user=user, date=date)
            return {
                'score': stats.score,
                'date': stats.date,
                'distance_travelled': stats.total_distance,
                'co2_emissions': stats.total_co2,
                'fuel_cost': stats.total_fuel_cost,
                'trips_count': stats.trips_count
            }
        except DailyStats.DoesNotExist:
            # Calculate from trips
            trips = Trip.objects.filter(
                user=user,
                start_time__date=date,
                status='completed'  # Only count completed trips
            )
            
            total_distance = 0
            total_co2 = 0
            total_fuel_cost = 0
            trips_count = trips.count()
            
            # Calculate totals from all trips
            for trip in trips:
                if trip.distance_km:
                    total_distance += float(trip.distance_km)
                
                total_co2 += self._calculate_emissions_from_trip(trip)
                total_fuel_cost += self._calculate_fuel_cost_from_trip(trip)
            
            # Calculate score
            score = self._calculate_score(
                total_distance, 
                total_co2, 
                total_fuel_cost, 
                trips_count
            )
            
            # Cache the result only if there were trips
            if trips_count > 0:
                DailyStats.objects.update_or_create(
                    user=user,
                    date=date,
                    defaults={
                        'score': score,
                        'total_distance': total_distance,
                        'total_co2': total_co2,
                        'total_fuel_cost': total_fuel_cost,
                        'trips_count': trips_count
                    }
                )
            
            return {
                'score': score,
                'date': date,
                'distance_travelled': total_distance,
                'co2_emissions': total_co2,
                'fuel_cost': total_fuel_cost,
                'trips_count': trips_count
            }
    
    @action(detail=False, methods=['get'], url_path='daily-score')
    def daily_score(self, request):
        """
        GET /api/trips/daily-score/
        Query params: 
            - date (optional, format: YYYY-MM-DD, defaults to today)
        
        Returns today's/specified day's score and stats for the Daily Score screen
        """
        date_param = request.query_params.get('date')
        
        if date_param:
            try:
                target_date = datetime.strptime(date_param, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {'error': 'Invalid date format. Use YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            target_date = timezone.now().date()
        
        stats = self._get_or_calculate_daily_stats(request.user, target_date)
        serializer = DailyScoreSerializer(stats)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='calendar-stats')
    def calendar_stats(self, request):
        """
        GET /api/trips/calendar-stats/
        Query params: 
            - month (1-12, defaults to current month)
            - year (YYYY, defaults to current year)
        
        Returns calendar view with scores for each day in the month
        For the calendar widget showing November 2025
        """
        try:
            month = int(request.query_params.get('month', timezone.now().month))
            year = int(request.query_params.get('year', timezone.now().year))
            
            if month < 1 or month > 12:
                return Response(
                    {'error': 'Month must be between 1 and 12'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid month or year'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get all days in the month
        num_days = calendar.monthrange(year, month)[1]
        days_data = []
        
        for day in range(1, num_days + 1):
            date = datetime(year, month, day).date()
            
            # Check if there are any completed trips on this day
            trips_count = Trip.objects.filter(
                user=request.user,
                start_time__date=date,
                status='completed'
            ).count()
            
            has_trips = trips_count > 0
            
            if has_trips:
                stats = self._get_or_calculate_daily_stats(request.user, date)
                score = stats['score']
            else:
                score = 0
            
            days_data.append({
                'date': date,
                'score': score,
                'has_trips': has_trips,
                'trips_count': trips_count
            })
        
        response_data = {
            'month': calendar.month_name[month],
            'year': year,
            'days': days_data
        }
        
        serializer = CalendarStatsSerializer(response_data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='monthly-chart')
    def monthly_chart(self, request):
        """
        GET /api/trips/monthly-chart/
        Query params: 
            - month (1-12, defaults to current month)
            - year (YYYY, defaults to current year)
        
        Returns chart data for distance/CO2/cost for the bottom section charts
        """
        try:
            month = int(request.query_params.get('month', timezone.now().month))
            year = int(request.query_params.get('year', timezone.now().year))
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid month or year'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get stats for the entire month
        start_date = datetime(year, month, 1).date()
        if month == 12:
            end_date = datetime(year + 1, 1, 1).date()
        else:
            end_date = datetime(year, month + 1, 1).date()
        
        # Get all stats for the month
        stats_qs = DailyStats.objects.filter(
            user=request.user,
            date__gte=start_date,
            date__lt=end_date
        ).order_by('date')
        
        distance_data = []
        co2_data = []
        cost_data = []
        
        # If no cached stats, calculate on the fly
        if not stats_qs.exists():
            current_date = start_date
            while current_date < end_date:
                stats = self._get_or_calculate_daily_stats(request.user, current_date)
                
                if stats['trips_count'] > 0:  # Only include days with trips
                    distance_data.append({
                        'date': current_date,
                        'value': stats['distance_travelled']
                    })
                    co2_data.append({
                        'date': current_date,
                        'value': stats['co2_emissions']
                    })
                    cost_data.append({
                        'date': current_date,
                        'value': stats['fuel_cost']
                    })
                
                current_date += timedelta(days=1)
        else:
            for stat in stats_qs:
                distance_data.append({
                    'date': stat.date,
                    'value': stat.total_distance
                })
                co2_data.append({
                    'date': stat.date,
                    'value': stat.total_co2
                })
                cost_data.append({
                    'date': stat.date,
                    'value': stat.total_fuel_cost
                })
        
        response_data = {
            'distance': distance_data,
            'co2_emissions': co2_data,
            'fuel_cost': cost_data
        }
        
        serializer = MonthlyChartSerializer(response_data)
        return Response(serializer.data)


class VehicleViewSet(viewsets.ModelViewSet):
    """CRUD operations for user vehicles"""
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # If this is set as active, deactivate other vehicles
        if serializer.validated_data.get('is_active', False):
            Vehicle.objects.filter(
                user=self.request.user, 
                is_active=True
            ).update(is_active=False)
        
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        # If this is set as active, deactivate other vehicles
        if serializer.validated_data.get('is_active', False):
            Vehicle.objects.filter(
                user=self.request.user, 
                is_active=True
            ).exclude(id=self.get_object().id).update(is_active=False)
        
        serializer.save()


import math
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Haversine formula to calculate distance in KM
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon/2)**2)
    c = 2 * math.asin(math.sqrt(a))
    return R * c


# Fuel type costs per km (in ₹)
FUEL_COSTS = {
    "petrol": 9.5,      # ₹9.5/km (assuming 12 km/l, ₹105/l)
    "diesel": 7.0,      # ₹7/km (assuming 18 km/l, ₹95/l)
    "cng": 4.5,         # ₹4.5/km (assuming 25 km/kg, ₹85/kg)
    "electric": 2.5,    # ₹2.5/km (assuming 5 km/kWh, ₹8/kWh)
}

# CO2 emissions per km (in kg)
FUEL_EMISSIONS = {
    "petrol": 0.12,
    "diesel": 0.10,
    "cng": 0.08,
    "electric": 0.05,
}


@api_view(['POST'])
def compare_routes(request):

    start_lat = request.data.get("start_latitude")
    start_lon = request.data.get("start_longitude")
    dest_lat = request.data.get("destination_latitude")
    dest_lon = request.data.get("destination_longitude")

    if not all([start_lat, start_lon, dest_lat, dest_lon]):
        return Response({"error": "Missing coordinates"}, status=400)

    # Distance Calculation
    distance_km = round(calculate_distance(start_lat, start_lon, dest_lat, dest_lon), 2)

    # Car options for all fuel types
    car_options = []
    for fuel_type, cost_per_km in FUEL_COSTS.items():
        car_cost = round(distance_km * cost_per_km)
        car_time = round(distance_km / 55, 1)  # 55 km/hr avg
        car_co2 = round(distance_km * FUEL_EMISSIONS[fuel_type], 1)
        
        car_options.append({
            "fuel_type": fuel_type,
            "estimated_cost": car_cost,
            "cost_per_km": cost_per_km,
            "time_hours": car_time,
            "co2_kg": car_co2,
            "comfort_rating": 5,
            "pros": ["Most comfortable", "Flexible timing", "Door-to-door"],
            "cons": ["Long drive", "Tiring for driver"]
        })

    # Other transport options
    flight_cost_min = 4500
    flight_cost_max = 8000
    flight_time = 2
    flight_co2 = round(distance_km * 0.15, 1)

    train_cost_min = 800
    train_cost_max = 2500
    train_time = round(distance_km / 45, 1)
    train_co2 = round(distance_km * 0.04, 1)

    bus_cost_min = 1200
    bus_cost_max = 1800
    bus_time = round(distance_km / 40, 1)
    bus_co2 = round(distance_km * 0.09, 1)

    # All Options Summary
    options = [
        {
            "mode": "car",
            "fuel_options": car_options  # All fuel types shown here
        },
        {
            "mode": "flight",
            "estimated_cost_min": flight_cost_min,
            "estimated_cost_max": flight_cost_max,
            "time_hours": flight_time,
            "co2_kg": flight_co2,
            "comfort_rating": 5,
            "pros": ["Fastest", "Time-saving"],
            "cons": ["Expensive", "Airport travel"],
        },
        {
            "mode": "train",
            "estimated_cost_min": train_cost_min,
            "estimated_cost_max": train_cost_max,
            "time_hours": train_time,
            "co2_kg": train_co2,
            "comfort_rating": 4,
            "pros": ["Cheapest", "Comfortable", "Eco-friendly"],
            "cons": ["Longer travel time"],
        },
        {
            "mode": "bus",
            "estimated_cost_min": bus_cost_min,
            "estimated_cost_max": bus_cost_max,
            "time_hours": bus_time,
            "co2_kg": bus_co2,
            "comfort_rating": 3,
            "pros": ["Affordable", "Easily available"],
            "cons": ["Less comfort", "Longer time"],
        }
    ]

    # Find cheapest car option
    cheapest_car = min(car_options, key=lambda x: x['estimated_cost'])
    cheapest_car_cost = cheapest_car['estimated_cost']

    # Recommendation Logic
    cheapest_overall = min([cheapest_car_cost, train_cost_min, bus_cost_min, flight_cost_min])

    if cheapest_overall == train_cost_min:
        recommendation = {
            "mode": "train",
            "reason": "Best balance of cost & comfort",
            "savings": cheapest_car_cost - train_cost_min
        }
    elif cheapest_overall == bus_cost_min:
        recommendation = {
            "mode": "bus",
            "reason": "Cheapest option",
            "savings": cheapest_car_cost - bus_cost_min
        }
    elif cheapest_overall == cheapest_car_cost:
        recommendation = {
            "mode": "car",
            "fuel_type": cheapest_car['fuel_type'],
            "reason": f"Most economical with {cheapest_car['fuel_type']} vehicle",
            "cost": cheapest_car_cost,
            "savings": 0
        }
    else:
        recommendation = {
            "mode": "flight",
            "reason": "Fastest option available",
            "savings": 0
        }

    return Response({
        "distance_km": distance_km,
        "options": options,
        "recommendation": recommendation
    })

