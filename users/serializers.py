from rest_framework import serializers
from rest_registration.api.serializers import DefaultUserProfileSerializer

from .models import Specialization


class CustomProfileSerializer(DefaultUserProfileSerializer):

    def get_fields(self):
        fields = super().get_fields()

        fields["roles"] = serializers.PrimaryKeyRelatedField(
            many=True,
            queryset=Specialization.objects.all(),
            source="profile.roles",
            required=False
        )

        return fields

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        roles = profile_data.get("roles")

        user = super().update(instance, validated_data)

        if roles is not None:
            user.profile.roles.set(roles)

        return user