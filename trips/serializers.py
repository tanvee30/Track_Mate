from rest_framework import serializers
from .models import Trip, TripLocation, TripNote
from django.contrib.auth.models import User

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


from rest_framework import serializers
from .models import Trip

# ADD this new serializer at the end of your file:

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


class TripNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripNote
        fields = ['id', 'note_text', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']