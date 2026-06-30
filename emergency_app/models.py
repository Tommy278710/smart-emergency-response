from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    full_name = models.CharField(
        max_length=100
    )

    username = models.CharField(
        max_length=50,
        unique=True
    )

    email = models.EmailField(
        unique=True
    )

    phone_number = models.CharField(
        max_length=15
    )

    state = models.CharField(
        max_length=50
    )

    lga = models.CharField(
        max_length=50
    )

    password = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.full_name


class EmergencyReport(models.Model):

    EMERGENCY_TYPES = [
        ("Fire", "Fire"),
        ("Medical", "Medical"),
        ("Accident", "Accident"),
        ("Security", "Security Threat"),
        ("Flood", "Flood"),
    ]

    SEVERITY_LEVELS = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Critical", "Critical"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Assigned", "Assigned"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    emergency_type = models.CharField(
        max_length=100,
        choices=EMERGENCY_TYPES
    )

    description = models.TextField()

    state = models.CharField(
        max_length=100
    )

    lga = models.CharField(
        max_length=100
    )

    address = models.TextField()

    severity = models.CharField(
        max_length=50,
        choices=SEVERITY_LEVELS
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    tracking_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.emergency_type} - {self.user.username}"

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        if not self.tracking_id:

            self.tracking_id = f"ER-{self.id:04d}"

            super().save(
                update_fields=["tracking_id"]
            )