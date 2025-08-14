from django.db import models
from django.conf import settings
import uuid

# Create your models here.
class vehiclequalification(models.Model):
    vehiclequalification_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    vehicle_id = models.ForeignKey('vehicles.Vehicle', on_delete=models.CASCADE, related_name='qualifications')
    qualification_id = models.ForeignKey('qualifications.Qualification', on_delete=models.CASCADE, related_name='vehicle_qualifications')

    def __str__(self):
        return f"Qualification {self.qualification_id} for Vehicle {self.vehicle_id.licence_plate}"