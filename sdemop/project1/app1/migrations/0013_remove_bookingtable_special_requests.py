# Generated by Django 5.0.6 on 2024-05-29 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_remove_bookingtable_stylist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookingtable',
            name='special_requests',
        ),
    ]
