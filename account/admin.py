from django.contrib import admin

from account.models import Profile, Referral


@admin.register(Profile)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    pass
