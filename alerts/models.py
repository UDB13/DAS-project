from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class DisasterAlert(models.Model):
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    event_type = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    magnitude = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    source_url = models.URLField()

    def __str__(self):
        return self.title
        # return f"{self.event_type} - {self.location} - {self.magnitude}"
    
class AlertType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=100, default="India")
    alert_types = models.ManyToManyField(AlertType,related_name='user_preferences', blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.region} - {self.alert_types}"