# Generated by Django 3.2 on 2021-05-13 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0006_alter_signup_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signup',
            name='img',
            field=models.ImageField(blank=True, upload_to='pics'),
        ),
    ]
