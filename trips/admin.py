from django.contrib import admin
from .models import Trip, TripLocation


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = [
        'trip_number',
        'user',
        'status',
        'mode_of_travel',
        'distance_km',
        'duration_minutes',
        'total_cost',
        'start_time',
    ]
    
    list_filter = [
        'status',
        'mode_of_travel',
        'trip_purpose',
        'start_time',
    ]
    
    search_fields = [
        'trip_number',
        'user__username',
        'start_location_name',
        'end_location_name',
    ]
    
    readonly_fields = [
        'trip_number',
        'distance_km',
        'duration_minutes',
        'co2_emission_kg',
        'created_at',
        'updated_at',
    ]
    
    fieldsets = (
        ('Trip Information', {
            'fields': ('trip_number', 'user', 'status')
        }),
        ('Start Location', {
            'fields': (
                'start_latitude',
                'start_longitude',
                'start_location_name',
                'start_time'
            )
        }),
        ('End Location', {
            'fields': (
                'end_latitude',
                'end_longitude',
                'end_location_name',
                'end_time'
            )
        }),
        ('Trip Details', {
            'fields': (
                'mode_of_travel',
                'distance_km',
                'duration_minutes',
                'trip_purpose',
                'number_of_companions'
            )
        }),
        ('Cost Details', {
            'fields': (
                'ticket_cost',
                'fuel_expense',
                'toll_cost',
                'parking_cost'
            )
        }),
        ('Environmental Impact', {
            'fields': ('co2_emission_kg',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    date_hierarchy = 'start_time'
    
    actions = ['calculate_emissions']
    
    def calculate_emissions(self, request, queryset):
        """Admin action to recalculate CO2 emissions for selected trips"""
        updated = 0
        for trip in queryset:
            if trip.distance_km and trip.mode_of_travel:
                trip.co2_emission_kg = trip.calculate_co2_emission()
                trip.save()
                updated += 1
        
        self.message_user(request, f'{updated} trips updated with CO2 emissions.')
    
    calculate_emissions.short_description = "Recalculate CO2 emissions"


@admin.register(TripLocation)
class TripLocationAdmin(admin.ModelAdmin):
    list_display = [
        'trip',
        'latitude',
        'longitude',
        'accuracy',
        'speed',
        'timestamp',
    ]
    
    list_filter = [
        'timestamp',
    ]
    
    search_fields = [
        'trip__trip_number',
    ]
    
    readonly_fields = ['timestamp']
    
    date_hierarchy = 'timestamp'


from .models import Trip, TripLocation, TripNote

@admin.register(TripNote)
class TripNoteAdmin(admin.ModelAdmin):
    list_display = ['trip', 'note_text', 'created_at']
    search_fields = ['trip__trip_number', 'note_text']
    list_filter = ['created_at']