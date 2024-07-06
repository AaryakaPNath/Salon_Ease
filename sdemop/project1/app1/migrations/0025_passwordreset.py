# Generated by Django 5.0.6 on 2024-06-05 11:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0024_contact_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=4)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.usertable')),
            ],
        ),
    ]
