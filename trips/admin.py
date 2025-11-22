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



from django.contrib import admin
from .models import Trip, TripLocation, TripNote, PlannedTrip

@admin.register(PlannedTrip)
class PlannedTripAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'trip_name', 'user', 'status',
        'planned_start_date',
        'get_estimated_co2',  # <-- Changed
        'start_location_name', 'destination_name', 'created_at'
    ]
    list_filter = ['status', 'mode_of_travel', 'trip_purpose']
    search_fields = ['trip_name', 'start_location_name', 'destination_name']
    date_hierarchy = 'planned_start_date'
    
    readonly_fields = ['created_at', 'updated_at', 'get_estimated_co2']  # <-- Changed
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'trip_name', 'description', 'status')
        }),
        ('Schedule', {
            'fields': ('planned_start_date', 'planned_end_date')
        }),
        ('Start Location', {
            'fields': (
                'start_location_name', 'start_location_address',
                'start_latitude', 'start_longitude'
            )
        }),
        ('Destination', {
            'fields': (
                'destination_name', 'destination_address',
                'destination_latitude', 'destination_longitude'
            )
        }),
        ('Trip Details', {
            'fields': (
                'mode_of_travel', 'trip_purpose', 'number_of_companions',
                'estimated_budget', 'notes'
            )
        }),
        ('Route Information', {
            'fields': (
                'estimated_distance_km', 'estimated_duration_minutes',
                'get_estimated_co2',  # <-- Changed
                'route_polyline', 'waypoints'
            )
        }),
        ('Actual Trip Link', {
            'fields': ('actual_trip',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    # Add this method
    def get_estimated_co2(self, obj):
        return obj.estimated_co2_kg if obj.estimated_co2_kg else '-'
    get_estimated_co2.short_description = 'Estimated CO2 (kg)'



# ==================== ADD THESE IMPORTS AT THE TOP ====================
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe


# ==================== ADD THESE ADMIN CLASSES TO YOUR EXISTING admin.py ====================

# Import the new models
from .models import Vehicle, DailyStats


# ==================== VEHICLE ADMIN ====================

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    """Admin interface for Vehicle model"""
    
    list_display = [
        'id',
        'user_link',
        'name',
        'vehicle_type',
        'fuel_efficiency',
        'emissions_factor',
        'fuel_price_per_liter',
        'is_active_badge',
        'created_at',
    ]
    
    list_filter = [
        'vehicle_type',
        'is_active',
        'created_at',
    ]
    
    search_fields = [
        'name',
        'user__username',
        'user__email',
    ]
    
    
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'vehicle_type', 'is_active')
        }),
        ('Technical Specifications', {
            'fields': ('fuel_efficiency', 'emissions_factor', 'fuel_price_per_liter')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_link(self, obj):
        """Create clickable link to user"""
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'
    
    def is_active_badge(self, obj):
        """Show active status as colored badge"""
        if obj.is_active:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">Active</span>'
            )
        return format_html(
            '<span style="background-color: #6c757d; color: white; padding: 3px 10px; border-radius: 3px;">Inactive</span>'
        )
    is_active_badge.short_description = 'Status'
    
    actions = ['activate_vehicles', 'deactivate_vehicles']
    
    def activate_vehicles(self, request, queryset):
        """Set selected vehicles as active"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} vehicle(s) activated successfully.')
    activate_vehicles.short_description = 'Activate selected vehicles'
    
    def deactivate_vehicles(self, request, queryset):
        """Set selected vehicles as inactive"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} vehicle(s) deactivated successfully.')
    deactivate_vehicles.short_description = 'Deactivate selected vehicles'


# ==================== DAILY STATS ADMIN ====================

@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    """Admin interface for DailyStats model - User Contribution Stats"""
    
    list_display = [
        'id',
        'user_link',
        'date',
        'score_badge',
        'trips_count',
        'total_distance_km',
        'total_co2_kg',
        'total_fuel_cost_display',
        'updated_at',
    ]
    
    list_filter = [
        'date',
        'created_at',
        'updated_at',
    ]
    
    search_fields = [
        'user__username',
        'user__email',
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'score_visualization',
        'statistics_summary',
    ]
    
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'date')
        }),
        ('Metrics', {
            'fields': ('score', 'score_visualization', 'trips_count')
        }),
        ('Distance & Emissions', {
            'fields': ('total_distance', 'total_co2')
        }),
        ('Cost', {
            'fields': ('total_fuel_cost',)
        }),
        ('Statistics', {
            'fields': ('statistics_summary',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_link(self, obj):
        """Create clickable link to user"""
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'
    
    def score_badge(self, obj):
        """Show score as colored badge based on value"""
        if obj.score >= 80:
            color = '#28a745'  # Green
            label = 'Excellent'
        elif obj.score >= 60:
            color = '#ffc107'  # Yellow
            label = 'Good'
        elif obj.score >= 40:
            color = '#fd7e14'  # Orange
            label = 'Average'
        else:
            color = '#dc3545'  # Red
            label = 'Needs Improvement'
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{} ({})</span>',
            color, obj.score, label
        )
    score_badge.short_description = 'Score'
    
    def total_distance_km(self, obj):
        """Display distance in km"""
        return f"{obj.total_distance:.2f} km"
    total_distance_km.short_description = 'Distance'
    
    def total_co2_kg(self, obj):
        """Display CO2 in kg"""
        return f"{obj.total_co2 / 1000:.2f} kg"
    total_co2_kg.short_description = 'CO2 Emissions'
    
    def total_fuel_cost_display(self, obj):
        """Display fuel cost with currency symbol"""
        return f"₹{obj.total_fuel_cost:.2f}"
    total_fuel_cost_display.short_description = 'Fuel Cost'
    
    def score_visualization(self, obj):
        """Visual progress bar for score"""
        width = obj.score
        if obj.score >= 80:
            color = '#28a745'
        elif obj.score >= 60:
            color = '#ffc107'
        elif obj.score >= 40:
            color = '#fd7e14'
        else:
            color = '#dc3545'
        
        return format_html(
            '<div style="width: 200px; background-color: #e9ecef; border-radius: 5px; height: 20px;">'
            '<div style="width: {}%; background-color: {}; border-radius: 5px; height: 20px; text-align: center; color: white; font-weight: bold; line-height: 20px;">'
            '{}%'
            '</div></div>',
            width, color, obj.score
        )
    score_visualization.short_description = 'Score Visualization'
    
    def statistics_summary(self, obj):
        """Show detailed statistics"""
        if obj.total_distance > 0:
            co2_per_km = obj.total_co2 / obj.total_distance
            cost_per_km = obj.total_fuel_cost / obj.total_distance
        else:
            co2_per_km = 0
            cost_per_km = 0
        
        html = f"""
        <table style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #f8f9fa;">
                <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6;">Metric</th>
                <th style="padding: 8px; text-align: right; border: 1px solid #dee2e6;">Value</th>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #dee2e6;">Total Trips</td>
                <td style="padding: 8px; text-align: right; border: 1px solid #dee2e6;">{obj.trips_count}</td>
            </tr>
            <tr style="background-color: #f8f9fa;">
                <td style="padding: 8px; border: 1px solid #dee2e6;">Total Distance</td>
                <td style="padding: 8px; text-align: right; border: 1px solid #dee2e6;">{obj.total_distance:.2f} km</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #dee2e6;">Total CO2</td>
                <td style="padding: 8px; text-align: right; border: 1px solid #dee2e6;">{obj.total_co2:.2f} g</td>
            </tr>
            <tr style="background-color: #f8f9fa;">
                <td style="padding: 8px; border: 1px solid #dee2e6;">Total Cost</td>
                <td style="padding: 8px; text-align: right; border: 1px solid #dee2e6;">₹{obj.total_fuel_cost:.2f}</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #dee2e6;"><strong>CO2 per km</strong></td>
                <td style="padding: 8px; text-align: right; border: 1px solid #dee2e6;"><strong>{co2_per_km:.2f} g/km</strong></td>
            </tr>
            <tr style="background-color: #f8f9fa;">
                <td style="padding: 8px; border: 1px solid #dee2e6;"><strong>Cost per km</strong></td>
                <td style="padding: 8px; text-align: right; border: 1px solid #dee2e6;"><strong>₹{cost_per_km:.2f}/km</strong></td>
            </tr>
        </table>
        """
        return mark_safe(html)
    statistics_summary.short_description = 'Detailed Statistics'
    
    actions = ['recalculate_stats', 'export_to_csv']
    
    def recalculate_stats(self, request, queryset):
        """Recalculate stats for selected days"""
        from datetime import datetime
        from .models import Trip
        
        count = 0
        for stat in queryset:
            # Recalculate from trips
            trips = Trip.objects.filter(
                user=stat.user,
                start_time__date=stat.date,
                status='completed'
            )
            
            total_distance = 0
            total_co2 = 0
            total_fuel_cost = 0
            trips_count = trips.count()
            
            for trip in trips:
                if trip.distance_km:
                    total_distance += float(trip.distance_km)
                if trip.co2_emission_kg:
                    total_co2 += float(trip.co2_emission_kg) * 1000  # Convert to grams
                if trip.fuel_expense:
                    total_fuel_cost += float(trip.fuel_expense)
            
            # Update stats
            stat.total_distance = total_distance
            stat.total_co2 = total_co2
            stat.total_fuel_cost = total_fuel_cost
            stat.trips_count = trips_count
            
            # Recalculate score (simple version)
            if total_distance > 0:
                stat.score = min(100, int((trips_count * 20) + (50 - (total_co2 / total_distance))))
            else:
                stat.score = 0
                
            stat.save()
            count += 1
        
        self.message_user(request, f'Successfully recalculated stats for {count} day(s).')
    recalculate_stats.short_description = 'Recalculate selected stats'
    
    def export_to_csv(self, request, queryset):
        """Export selected stats to CSV"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="daily_stats.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Date', 'User', 'Score', 'Trips', 'Distance (km)', 'CO2 (g)', 'Fuel Cost (₹)'])
        
        for stat in queryset:
            writer.writerow([
                stat.date,
                stat.user.username,
                stat.score,
                stat.trips_count,
                stat.total_distance,
                stat.total_co2,
                stat.total_fuel_cost,
            ])
        
        return response
    export_to_csv.short_description = 'Export to CSV'


# ==================== OPTIONAL: CUSTOM ADMIN SITE TITLE ====================
# Add this at the bottom of your admin.py

admin.site.site_header = "Trip Tracker Admin"
admin.site.site_title = "Trip Tracker Admin Portal"
admin.site.index_title = "Welcome to Trip Tracker Administration"