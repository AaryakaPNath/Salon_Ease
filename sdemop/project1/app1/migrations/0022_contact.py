# Generated by Django 5.0.6 on 2024-06-04 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0020_remove_usertable_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('contact_no', models.IntegerField()),
                ('message', models.CharField(max_length=50)),
            ],
        ),
    ]
