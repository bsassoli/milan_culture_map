# Generated by Django 3.1.7 on 2021-04-02 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0010_auto_20210402_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='image',
            field=models.ImageField(default='logo-comune-milano.png', upload_to='images/'),
        ),
    ]
