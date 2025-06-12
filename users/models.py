from django.db import models # type: ignore
from django.conf import settings # type: ignore
from django.utils import timezone # type: ignore
from rest_framework.exceptions import NotAcceptable # type: ignore
from django.utils.translation import gettext_lazy as _ # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
#from django_countries.fields import CountryField # type: ignore
from phonenumber_field.modelfields import PhoneNumberField # type: ignore

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatar", blank=True)
    bio = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.user.get_full_name()
    
class Address(models.Model):
    BILLING = "B"
    SHIPPING = "S"

    ADDRESS_CHOICES = ((BILLING, _("billing")), (SHIPPING, _("shipping")))

    user = models.ForeignKey(User, related_name="addresses", on_delete=models.CASCADE)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    city = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.user.get_full_name()

class PhoneNumber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='phone_number')
    phone_number = PhoneNumberField(unique=True)
    security_code = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    sent = models.DateTimeField(null=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.phone_number
    
    def generate_security_code(self):
        """
        Returns a random digit security code, default length = 6
        """
        
        token_length = getattr(settings, 'TOKEN_LENGTH', 6)
        return get_random_string(length=token_length, allowed_chars='0123456789')
    
    
    def is_security_code_expired(self):
        """
        Checks if the security code has expired
        """
        
        expiration_date = self.sent + timezone.timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
        return expiration_date <= timezone.now()