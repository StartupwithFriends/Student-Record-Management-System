# Generated by Django 3.2 on 2021-05-15 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0011_auto_20210514_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signup',
            name='img',
            field=models.ImageField(blank=True, default='dashboard/profile.png', upload_to='pics'),
        ),
    ]
