# Generated by Django 5.1.2 on 2024-11-01 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='is_favorite',
            field=models.BooleanField(default=False, verbose_name='Избранный'),
        ),
    ]
