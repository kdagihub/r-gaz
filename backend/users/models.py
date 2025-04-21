from django.db import models
from location_field.models.plain import PlainLocationField
from django.conf import settings
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('vendor', 'Vendeur'),
        ('admin', 'Admin'),  # utile pour la clarté
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    location = PlainLocationField(based_fields=['address'], zoom=12, blank=True, null=True)
    
    is_verified_email = models.BooleanField(default=False)
    is_approved_vendor = models.BooleanField(default=False)

    def is_active_vendor(self):
        return self.role == "vendor" and self.is_verified_email and self.is_approved_vendor

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"



class VendorProfile(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('approved', 'Validé'),
        ('suspended', 'Suspendu'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    location = PlainLocationField(based_fields=['address'], zoom=12)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.business_name
