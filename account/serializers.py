from rest_framework import serializers

from account.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone_number', 'invite_code']


class ActivateInviteCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['invite_code']