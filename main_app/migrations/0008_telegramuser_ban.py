# Generated by Django 5.1.6 on 2025-05-27 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_post_reactions_post_views_telegramuser_last_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='ban',
            field=models.BooleanField(default=False),
        ),
    ]
