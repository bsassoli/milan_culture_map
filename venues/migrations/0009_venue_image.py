# Generated by Django 3.1.7 on 2021-04-02 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0008_auto_20210401_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
