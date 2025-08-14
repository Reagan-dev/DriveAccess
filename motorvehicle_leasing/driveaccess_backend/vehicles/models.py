from django.db import models
import uuid
from django.utils import timezone

# Create your models here.
class Vehicle(models.Model):
    vehicle_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    type = models.CharField(max_length=50, choices=[
        ('matatu', 'Matatu'),
        ('motorcycle', 'Motorcycle'),
    ],)
    model = models.CharField(max_length=100)
    licence_plate = models.CharField(max_length=15, unique=True)
    status = models.CharField(max_length=20, choices=[
        ('available', 'Available'),
        ('leased', 'leased'),
        ('maintenance', 'Maintenance'),
    ], default='available')
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255, blank=True, null=True)  

    def mark_as_maintenance(self):
        self.status = 'maintenance'
        self.save()

    def mark_as_available(self):
        self.status = 'available'
        self.save()

    def mark_as_leased(self):
        self.status = 'leased'
        self.save()

    def __str__(self):
        return f"{self.model} ({self.licence_plate}) - {self.get_status_display()}"