# Generated by Django 4.0.4 on 2022-05-29 14:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0002_topic_room_host_message_room_topic'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.AddField(
            model_name='room',
            name='practicipants',
            field=models.ManyToManyField(blank=True, related_name='practicipants', to=settings.AUTH_USER_MODEL),
        ),
    ]
