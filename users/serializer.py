from django.contrib.auth import get_user_model
from .models import User
from rest_framework import serializers

class RegisterSe(serializers.ModelSerializer):
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if password != password_confirm:
                raise serializers.ValidationError('Passwords do not match')
        
        return attrs

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')