from django.db import models
from django.conf import settings
import uuid

# Create your models here.
class lease(models.Model):
    lease_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leases')
    vehicle_id = models.ForeignKey('vehicles.Vehicle', on_delete=models.CASCADE, related_name='leases')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    lease_type = models.CharField(max_length=50, choices=[
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ], default='hourly')
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('pending', 'pending'),
        ('returned', 'returned'),
        ('rejected', 'rejected'),
    ], default='pending')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def id(self):
        return self.lease_id

    class Meta:
        verbose_name = 'Lease'
        verbose_name_plural = 'Leases'
        ordering = ['-start_time']

    def __str__(self):
        return f"Lease {self.lease_id} - {self.user_id.name} ({self.vehicle_id.licence_plate})"
