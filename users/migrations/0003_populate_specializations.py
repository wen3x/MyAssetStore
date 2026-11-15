from django.db import migrations


def create_specializations(apps, schema_editor):
    Specialization = apps.get_model("users", "Specialization")

    specializations = [
        "VIDEO_EDITOR",
        "3D_MODELER",
        "DESIGNER",
        "GRAPHIC_DESIGNER",
        "UI_UX_DESIGNER",
        "MOTION_DESIGNER",
        "ANIMATOR",
        "ILLUSTRATOR",
        "PHOTOGRAPHER",
        "VIDEOGRAPHER",
        "SOUND_DESIGNER",
        "COMPOSER",
        "MUSIC_PRODUCER",
        "DEVELOPER",
        "GAME_DEVELOPER",
        "VFX_ARTIST",
        "CONCEPT_ARTIST",
        "TEXTURE_ARTIST",
        "LEVEL_DESIGNER",
        "OTHER",
    ]

    Specialization.objects.using(schema_editor.connection.alias).bulk_create(
        [
            Specialization(name=name)
            for name in specializations
        ],
        ignore_conflicts=True,
    )


class Migration(migrations.Migration):

    dependencies = [
    ("users", "0002_specialization_profile"),
    ]

    operations = [
        migrations.RunPython(
            create_specializations,
            migrations.RunPython.noop,
        ),
    ]