# Generated by Django 5.0.6 on 2024-05-29 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0014_bookingtable_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookingtable',
            name='amount',
        ),
    ]
