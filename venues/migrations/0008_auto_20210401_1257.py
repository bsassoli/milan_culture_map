# Generated by Django 3.1.7 on 2021-04-01 12:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0007_auto_20210401_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='favorites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]
