# Generated by Django 3.2 on 2021-05-15 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0012_alter_signup_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signup',
            name='img',
        ),
    ]