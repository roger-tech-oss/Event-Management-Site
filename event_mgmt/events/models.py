from django.db import models
from django.contrib.auth.models import User
from datetime import time

class Venue(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    event_time = models.TimeField(null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)

    def __str__(self):
        return self.title

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    tickets = models.PositiveIntegerField()
    registered_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user} - {self.event}"
