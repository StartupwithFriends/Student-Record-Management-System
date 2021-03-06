# Generated by Django 3.2 on 2021-05-16 10:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myApp', '0017_delete_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('roll', models.CharField(max_length=50)),
                ('per', models.FloatField()),
                ('eng', models.IntegerField()),
                ('hin', models.IntegerField()),
                ('maths', models.IntegerField()),
                ('sci', models.IntegerField()),
                ('sst', models.IntegerField()),
                ('cs', models.IntegerField()),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
