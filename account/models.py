from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    verification_code = models.CharField(max_length=4, blank=True, null=True)
    invite_code = models.CharField(max_length=6, blank=True, null=True)


class Referral(models.Model):
    referrer = models.ForeignKey(Profile, related_name='referrals_given', on_delete=models.CASCADE)
    referred = models.ForeignKey(Profile, related_name='referrals_received', on_delete=models.CASCADE)
