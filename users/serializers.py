from rest_framework import serializers
from rest_registration.api.serializers import DefaultUserProfileSerializer
from django.conf import settings

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

        fields["avatar"] = serializers.ImageField(
            source="profile.avatar",
            required=False,
            allow_null=True
        )
        fields["remove_avatar"] = serializers.BooleanField(
            write_only=True,
            required=False
        )

        return fields

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})

        roles = profile_data.pop("roles", None)
        avatar = profile_data.pop("avatar", serializers.empty)
        remove_avatar = validated_data.pop("remove_avatar", False)

        user = super().update(instance, validated_data)
        profile = user.profile

        if roles is not None:
            profile.roles.set(roles)

        if remove_avatar:
            if profile.avatar:
                profile.avatar.delete(save=False)
                profile.avatar = None
                profile.save()

        elif avatar is not serializers.empty:
            if profile.avatar:
                profile.avatar.delete(save=False)

            profile.avatar = avatar
            profile.save()

        return user