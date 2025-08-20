from django.db import models
import uuid
from django.conf import settings
from accounts.models import User
from django.utils import timezone



# Create your models here.
class Qualification(models.Model):
    qualification_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='qualifications')
    qualification_type = models.CharField(max_length=50, choices=[
        ('driving_license', 'Driving License'),
        ('PSV_license', 'PSV License'),
    ], default='driving_license')
    issue_date = models.DateField()
    expiry_date = models.DateField()
    approved = models.BooleanField(default=False)

        
    class Meta:
        verbose_name = 'Qualification'
        verbose_name_plural = 'Qualifications'
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.user_id.name} - {self.get_qualification_type_display()} ({self.issue_date})"