# Generated by Django 3.1 on 2021-04-08 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0026_auto_20210408_0732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.TextField(),
        ),
    ]