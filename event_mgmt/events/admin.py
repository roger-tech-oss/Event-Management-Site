from django.contrib import admin
from .models import Venue, Event, Registration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_time', 'date', 'venue', 'organizer', 'price')
    list_filter = ('date', 'venue', 'organizer')
    search_fields = ('title', 'description')
    ordering = ('date',)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'capacity')
    search_fields = ('name', 'address')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'tickets', 'registered_at')
    list_filter = ('event', 'registered_at')
