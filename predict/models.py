from django.contrib.auth.models import User
from django.db import models


class HealthData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    diet = models.TextField()
    stress = models.PositiveIntegerField()  # Expected to be between 1 and 10
    activity = models.PositiveIntegerField()  # Expected in hours per week
    sleep = models.PositiveIntegerField()  # Expected in hours per night
    biometrics = models.CharField(max_length=255)  # For BP, Glucose levels, etc.
    medications = models.CharField(max_length=255)
    family_history = models.TextField()

    def __str__(self):
        return f"Health Data for Record {self.id}"
