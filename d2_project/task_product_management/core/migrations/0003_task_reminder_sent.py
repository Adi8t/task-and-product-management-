# Generated by Django 5.1.4 on 2024-12-25 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='reminder_sent',
            field=models.BooleanField(default=False),
        ),
    ]