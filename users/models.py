from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Specialization(models.Model):

    class SpecializationName(models.TextChoices):
        VIDEO_EDITOR = "VIDEO_EDITOR", "Video Editor"
        THREE_D_MODELER = "3D_MODELER", "3D Modeler"
        DESIGNER = "DESIGNER", "Designer"
        GRAPHIC_DESIGNER = "GRAPHIC_DESIGNER", "Graphic Designer"
        UI_UX_DESIGNER = "UI_UX_DESIGNER", "UI/UX Designer"
        MOTION_DESIGNER = "MOTION_DESIGNER", "Motion Designer"
        ANIMATOR = "ANIMATOR", "Animator"
        ILLUSTRATOR = "ILLUSTRATOR", "Illustrator"
        PHOTOGRAPHER = "PHOTOGRAPHER", "Photographer"
        VIDEOGRAPHER = "VIDEOGRAPHER", "Videographer"
        SOUND_DESIGNER = "SOUND_DESIGNER", "Sound Designer"
        COMPOSER = "COMPOSER", "Composer"
        MUSIC_PRODUCER = "MUSIC_PRODUCER", "Music Producer"
        DEVELOPER = "DEVELOPER", "Developer"
        GAME_DEVELOPER = "GAME_DEVELOPER", "Game Developer"
        VFX_ARTIST = "VFX_ARTIST", "VFX Artist"
        CONCEPT_ARTIST = "CONCEPT_ARTIST", "Concept Artist"
        TEXTURE_ARTIST = "TEXTURE_ARTIST", "Texture Artist"
        LEVEL_DESIGNER = "LEVEL_DESIGNER", "Level Designer"
        OTHER = "OTHER", "Other"

    name = models.CharField(
        max_length=20, choices=SpecializationName.choices, unique=True, verbose_name="Role Name"
    )

    def __str__(self):
        return self.get_name_display()


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", verbose_name="User"
    )
    roles = models.ManyToManyField(
        Specialization, blank=True, related_name="profiles", verbose_name="Roles"
    )

    def __str__(self):
        return f"Profile: {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    profile = getattr(instance, 'profile', None)
    if profile:
        profile.save()