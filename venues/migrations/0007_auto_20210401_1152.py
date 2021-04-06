# Generated by Django 3.1.7 on 2021-04-01 11:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0006_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='followers',
            field=models.ManyToManyField(blank=True, null=True, related_name='favorites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='favorite',
            field=models.ManyToManyField(blank=True, related_name='venue', to='venues.Venue'),
        ),
    ]
