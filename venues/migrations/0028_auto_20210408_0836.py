# Generated by Django 3.1 on 2021-04-08 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0027_auto_20210408_0736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='url',
            field=models.URLField(max_length=300),
        ),
    ]
