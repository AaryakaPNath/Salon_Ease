# Generated by Django 5.0.6 on 2024-05-27 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_servicetable_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicetable',
            name='category',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
