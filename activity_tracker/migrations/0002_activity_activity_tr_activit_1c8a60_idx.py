# Generated by Django 5.1.3 on 2025-01-03 18:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_tracker', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name='activity',
            index=models.Index(fields=['activity_type'], name='activity_tr_activit_1c8a60_idx'),
        ),
    ]
