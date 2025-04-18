# Generated by Django 5.1.7 on 2025-04-02 15:12

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanagement', '0004_alter_profile_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='past_due_date',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
