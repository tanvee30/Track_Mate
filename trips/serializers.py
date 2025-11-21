from rest_framework import serializers
from .models import Trip, TripLocation, TripNote, PlannedTrip
from django.utils import timezone


class TripLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripLocation
        fields = ['id', 'latitude', 'longitude', 'accuracy', 'speed', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class TripNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripNote
        fields = ['id', 'note_text', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TripSerializer(serializers.ModelSerializer):
    tracking_points = TripLocationSerializer(many=True, read_only=True)
    notes = TripNoteSerializer(many=True, read_only=True)
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Trip
        fields = [
            'id',
            'trip_number',
            'username',
            'status',
            'start_latitude',
            'start_longitude',
            'start_location_name',
            'start_time',
            'end_latitude',
            'end_longitude',
            'end_location_name',
            'end_time',
            'mode_of_travel',
            'distance_km',
            'duration_minutes',
            'trip_purpose',
            'number_of_companions',
            'ticket_cost',
            'fuel_expense',
            'toll_cost',
            'parking_cost',
            'total_cost',
            'co2_emission_kg',
            'tracking_points',
            'notes',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'trip_number', 'created_at', 'updated_at', 'username']


class TripStartSerializer(serializers.Serializer):
    """Serializer for starting a trip"""
    start_latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    start_longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    start_location_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    start_time = serializers.DateTimeField(required=False)


class TripEndSerializer(serializers.Serializer):
    """Serializer for ending a trip"""
    end_latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    end_longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    end_location_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    end_time = serializers.DateTimeField(required=False)
    mode_of_travel = serializers.ChoiceField(choices=Trip.MODE_CHOICES, required=False)
    trip_purpose = serializers.ChoiceField(choices=Trip.PURPOSE_CHOICES, required=False)
    number_of_companions = serializers.IntegerField(required=False, default=0)


class TripUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating trip details"""
    class Meta:
        model = Trip
        fields = [
            'mode_of_travel',
            'trip_purpose',
            'number_of_companions',
            'ticket_cost',
            'fuel_expense',
            'toll_cost',
            'parking_cost'
        ]


class TrackingPointSerializer(serializers.Serializer):
    """Serializer for adding tracking points during ongoing trip"""
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    accuracy = serializers.FloatField()
    speed = serializers.FloatField(required=False, allow_null=True)
    timestamp = serializers.DateTimeField(required=False)


class ManualTripSerializer(serializers.Serializer):
    """Serializer for creating manual trip entries"""
    
    # Start location (can be address or coordinates)
    start_location = serializers.CharField(
        max_length=255, 
        required=False, 
        help_text="Start address (e.g., 'AKGEC College, Ghaziabad')"
    )
    start_latitude = serializers.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        required=False,
        help_text="Start latitude if known"
    )
    start_longitude = serializers.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        required=False,
        help_text="Start longitude if known"
    )
    
    # End location (can be address or coordinates)
    end_location = serializers.CharField(
        max_length=255, 
        required=False,
        help_text="End address (e.g., 'Gaur Central Mall')"
    )
    end_latitude = serializers.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        required=False,
        help_text="End latitude if known"
    )
    end_longitude = serializers.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        required=False,
        help_text="End longitude if known"
    )
    
    # Trip details
    mode_of_travel = serializers.ChoiceField(
        choices=Trip.MODE_CHOICES,
        help_text="How did you travel?"
    )
    trip_purpose = serializers.ChoiceField(
        choices=Trip.PURPOSE_CHOICES,
        required=False,
        help_text="What was the purpose?"
    )
    trip_date = serializers.DateField(
        required=False,
        help_text="When did this trip happen?"
    )
    number_of_companions = serializers.IntegerField(
        required=False, 
        default=0,
        help_text="How many people with you?"
    )
    
    def validate(self, data):
        """Ensure we have either address or coordinates for both start and end"""
        
        # Check start location
        has_start_address = data.get('start_location')
        has_start_coords = data.get('start_latitude') and data.get('start_longitude')
        
        if not (has_start_address or has_start_coords):
            raise serializers.ValidationError(
                "Please provide either start_location OR both start_latitude and start_longitude"
            )
        
        # Check end location
        has_end_address = data.get('end_location')
        has_end_coords = data.get('end_latitude') and data.get('end_longitude')
        
        if not (has_end_address or has_end_coords):
            raise serializers.ValidationError(
                "Please provide either end_location OR both end_latitude and end_longitude"
            )
        
        return data


class RoutePreviewSerializer(serializers.Serializer):
    """Serializer for getting route preview before saving trip"""
    
    start_location = serializers.CharField(max_length=255, required=False)
    start_latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False)
    start_longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False)
    
    end_location = serializers.CharField(max_length=255, required=False)
    end_latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False)
    end_longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False)
    
    mode_of_travel = serializers.ChoiceField(
        choices=Trip.MODE_CHOICES,
        default='car'
    )


class WaypointSerializer(serializers.Serializer):
    """Serializer for waypoints in planned trips"""
    name = serializers.CharField(max_length=255)
    address = serializers.CharField()
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    order = serializers.IntegerField(min_value=1)


class PlannedTripSerializer(serializers.ModelSerializer):
    """Main serializer for PlannedTrip"""
    is_upcoming = serializers.ReadOnlyField()
    is_past = serializers.ReadOnlyField()
    estimated_co2_kg = serializers.ReadOnlyField()
    actual_trip_id = serializers.IntegerField(source='actual_trip.id', read_only=True)
    actual_trip_number = serializers.CharField(source='actual_trip.trip_number', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = PlannedTrip
        fields = [
            'id', 'username', 'trip_name', 'description', 'status',
            'planned_start_date', 'planned_end_date',
            'start_location_name', 'start_location_address',
            'start_latitude', 'start_longitude',
            'destination_name', 'destination_address',
            'destination_latitude', 'destination_longitude',
            'estimated_distance_km', 'estimated_duration_minutes',
            'waypoints', 'mode_of_travel', 'trip_purpose',
            'number_of_companions', 'estimated_budget',
            'estimated_co2_kg', 'notes', 'route_polyline',
            'actual_trip_id', 'actual_trip_number',
            'is_upcoming', 'is_past',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'username', 'created_at', 'updated_at', 
                           'status', 'actual_trip_id', 'actual_trip_number']
    
    def validate_planned_start_date(self, value):
        """Validate that planned start date is not too far in the past"""
        if value and value < timezone.now() - timezone.timedelta(days=1):
            raise serializers.ValidationError(
                "Planned start date cannot be more than 1 day in the past."
            )
        return value
    
    def validate(self, data):
        """Validate that end date is after start date"""
        if 'planned_end_date' in data and data.get('planned_end_date'):
            planned_start = data.get('planned_start_date')
            if planned_start and data['planned_end_date'] <= planned_start:
                raise serializers.ValidationError({
                    'planned_end_date': 'End date must be after start date.'
                })
        return data


class PlannedTripListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    is_upcoming = serializers.ReadOnlyField()
    estimated_co2_kg = serializers.ReadOnlyField()
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = PlannedTrip
        fields = [
            'id', 'username', 'trip_name', 'status',
            'planned_start_date', 'planned_end_date',
            'start_location_name', 'destination_name',
            'estimated_distance_km', 'estimated_duration_minutes',
            'mode_of_travel', 'trip_purpose',
            'estimated_co2_kg', 'is_upcoming', 'created_at'
        ]


class PlannedTripUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating planned trips"""
    
    class Meta:
        model = PlannedTrip
        fields = [
            'trip_name', 'description',
            'planned_start_date', 'planned_end_date',
            'start_location_name', 'start_location_address',
            'start_latitude', 'start_longitude',
            'destination_name', 'destination_address',
            'destination_latitude', 'destination_longitude',
            'estimated_distance_km', 'estimated_duration_minutes',
            'waypoints', 'mode_of_travel', 'trip_purpose',
            'number_of_companions', 'estimated_budget',
            'notes', 'route_polyline'
        ]
    
    def validate(self, data):
        instance = self.instance
        if instance and instance.status != 'planned':
            raise serializers.ValidationError(
                "Cannot update trip that has been started or completed."
            )
        return data


class StartPlannedTripSerializer(serializers.Serializer):
    """Serializer for starting a planned trip"""
    start_latitude = serializers.DecimalField(
        max_digits=9, 
        decimal_places=6,
        required=False,
        help_text="Current GPS latitude (overrides planned start location)"
    )
    start_longitude = serializers.DecimalField(
        max_digits=9, 
        decimal_places=6,
        required=False,
        help_text="Current GPS longitude (overrides planned start location)"
    )
    start_location_name = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Override start location name"
    )
    notes = serializers.CharField(
        required=False, 
        allow_blank=True,
        help_text="Additional notes for the actual trip"
    )


class PlannedTripCreateSerializer(serializers.Serializer):
    """Serializer for creating planned trip with route preview"""
    
    # Basic info
    trip_name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    
    # Start location (can be address or coordinates)
    start_location_name = serializers.CharField(max_length=255)
    start_location_address = serializers.CharField(required=False, allow_blank=True)
    start_latitude = serializers.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        required=False
    )
    start_longitude = serializers.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        required=False
    )
    
    # Destination (can be address or coordinates)
    destination_name = serializers.CharField(max_length=255)
    destination_address = serializers.CharField(required=False, allow_blank=True)
    destination_latitude = serializers.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        required=False
    )
    destination_longitude = serializers.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        required=False
    )
    
    # Date and time
    planned_start_date = serializers.DateTimeField()
    planned_end_date = serializers.DateTimeField(required=False)
    
    # Trip details
    mode_of_travel = serializers.ChoiceField(
        choices=Trip.MODE_CHOICES,
        required=False
    )
    trip_purpose = serializers.ChoiceField(
        choices=Trip.PURPOSE_CHOICES,
        required=False
    )
    number_of_companions = serializers.IntegerField(required=False, default=0)
    estimated_budget = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=False
    )
    
    # Optional
    waypoints = serializers.JSONField(required=False)
    notes = serializers.CharField(required=False, allow_blank=True)
    
    # Auto-calculate route
    auto_calculate_route = serializers.BooleanField(
        default=True,
        help_text="Automatically get route from Google Maps"
    )
    
    def validate(self, data):
        """Ensure we have location data"""
        # Check start location
        has_start_coords = data.get('start_latitude') and data.get('start_longitude')
        has_start_address = data.get('start_location_address')
        
        if not (has_start_coords or has_start_address):
            raise serializers.ValidationError(
                "Provide either start coordinates OR start address"
            )
        
        # Check destination
        has_dest_coords = data.get('destination_latitude') and data.get('destination_longitude')
        has_dest_address = data.get('destination_address')
        
        if not (has_dest_coords or has_dest_address):
            raise serializers.ValidationError(
                "Provide either destination coordinates OR destination address"
            )
        
        return data