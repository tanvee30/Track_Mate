from django.db import models
from django.conf import settings  # ← Use this instead
from django.utils import timezone
import math

class Trip(models.Model):
    """Model to store trip information"""
    
    MODE_CHOICES = [
        ('walk', 'Walking'),
        ('bike', 'Bicycle'),
        ('car', 'Car'),
        ('bus', 'Bus'),
        ('train', 'Train'),
        ('metro', 'Metro'),
        ('auto', 'Auto Rickshaw'),
        ('bike_taxi', 'Bike Taxi'),
        ('other', 'Other'),
    ]
    
    TRIP_STATUS = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PURPOSE_CHOICES = [
        ('work', 'Work/Office'),
        ('education', 'Education'),
        ('shopping', 'Shopping'),
        ('social', 'Social/Recreation'),
        ('medical', 'Medical'),
        ('personal', 'Personal Business'),
        ('other', 'Other'),
    ]
    
    # User reference
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Trip identification
    trip_number = models.CharField(max_length=50, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=TRIP_STATUS, default='ongoing')
    
    # Start location details
    start_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    start_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    start_location_name = models.CharField(max_length=255, blank=True, null=True)
    start_time = models.DateTimeField(default=timezone.now)
    
    # End location details
    end_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    end_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    end_location_name = models.CharField(max_length=255, blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    
    # Trip details
    mode_of_travel = models.CharField(max_length=20, choices=MODE_CHOICES, blank=True, null=True)
    distance_km = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    duration_minutes = models.IntegerField(blank=True, null=True)
    
    # Additional information
    trip_purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES, blank=True, null=True)
    number_of_companions = models.IntegerField(default=0)
    
    # Cost details
    ticket_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fuel_expense = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    toll_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    parking_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Environmental impact
    co2_emission_kg = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Manual entry and route data
    is_manual_entry = models.BooleanField(default=False, help_text="True if trip was manually entered")
    route_polyline = models.TextField(blank=True, null=True, help_text="Encoded polyline from Google Directions API")
    suggested_distance_km = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True,
        help_text="Distance from Google Directions API"
    )
    suggested_duration_minutes = models.IntegerField(
        blank=True, 
        null=True,
        help_text="Duration from Google Directions API"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['user', '-start_time']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Trip {self.trip_number} - {self.user.username} ({self.status})"
    
    def save(self, *args, **kwargs):
        # Auto-generate trip number if not exists
        if not self.trip_number:
            self.trip_number = f"TRIP-{self.user.id}-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)
    
    def calculate_distance(self):
        """Calculate distance between start and end coordinates using Haversine formula"""
        if not all([self.start_latitude, self.start_longitude, 
                   self.end_latitude, self.end_longitude]):
            return None
        
        # Radius of Earth in kilometers
        R = 6371.0
        
        # Convert coordinates to radians
        lat1 = math.radians(float(self.start_latitude))
        lon1 = math.radians(float(self.start_longitude))
        lat2 = math.radians(float(self.end_latitude))
        lon2 = math.radians(float(self.end_longitude))
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        return round(distance, 2)
    
    def calculate_duration(self):
        """Calculate trip duration in minutes"""
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            return int(duration.total_seconds() / 60)
        return None
    
    def calculate_co2_emission(self):
        """Calculate CO2 emissions based on mode and distance"""
        if not self.distance_km or not self.mode_of_travel:
            return None
        
        # CO2 emission factors (kg per km)
        emission_factors = {
            'walk': 0,
            'bike': 0,
            'car': 0.192,
            'bus': 0.089,
            'train': 0.041,
            'metro': 0.030,
            'auto': 0.150,
            'bike_taxi': 0.084,
            'other': 0.150,
        }
        
        factor = emission_factors.get(self.mode_of_travel, 0)
        emission = float(self.distance_km) * factor
        return round(emission, 2)
    
    @property
    def total_cost(self):
        """Calculate total cost of trip"""
        costs = [
            self.ticket_cost or 0,
            self.fuel_expense or 0,
            self.toll_cost or 0,
            self.parking_cost or 0
        ]
        return sum(costs)


class TripLocation(models.Model):
    """Model to store intermediate GPS tracking points during trip"""
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='tracking_points')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    accuracy = models.FloatField(help_text="GPS accuracy in meters")
    speed = models.FloatField(blank=True, null=True, help_text="Speed in km/h")
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['trip', 'timestamp']),
        ]
    
    def __str__(self):
        return f"Location for {self.trip.trip_number} at {self.timestamp}"
    

class TripNote(models.Model):
    """Model to store user notes/highlights after trip completion"""
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='notes')
    note_text = models.TextField(help_text="User's notes about the trip")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Note for {self.trip.trip_number}"