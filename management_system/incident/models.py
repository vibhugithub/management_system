from django.contrib.auth.models import AbstractUser
from django.db import models
import random
from django.conf import settings
from django.utils import timezone

"""
    In Django's default AbstractUser model, the email field is already
    present by default
"""


class UserProfile(AbstractUser):
    # email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50, blank=True, null=True)
    user_type = models.CharField(
        max_length=20,
        choices=[
            ("individual", "Individual"),
            ("enterprise", "Enterprise"),
            ("government", "Government"),
        ],
        default="individual",
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Custom logic
        super(UserProfile, self).save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     if self.pin_code:
    #         self.city, self.country = get_city_country(self.pin_code)
    #     super().save(*args, **kwargs)


class RegisterProfile(models.Model):
    INCIDENT_TYPE_CHOICES = [
        ("Enterprise", "Enterprise"),
        ("Government", "Government"),
    ]

    PRIORITY_CHOICES = [
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]

    STATUS_CHOICES = [
        ("Open", "Open"),
        ("In progress", "In progress"),
        ("Closed", "Closed"),
    ]

    incident_id = models.CharField(max_length=20, unique=True, editable=False)
    reporter_name = models.ForeignKey(
        "UserProfile", on_delete=models.CASCADE, related_name="incidents"
    )
    incident_details = models.TextField()
    reported_date = models.DateTimeField(auto_now_add=True)
    incident_type = models.CharField(max_length=20, choices=INCIDENT_TYPE_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="Open")

    def save(self, *args, **kwargs):
        if not self.incident_id:
            self.incident_id = f"RMG{random.randint(10000, 99999)}{timezone.now().year}"
            while RegisterProfile.objects.filter(incident_id=self.incident_id).exists():
                self.incident_id = (
                    f"RMG{random.randint(10000, 99999)}{timezone.now().year}"
                )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.incident_id
