# Generated by Django 3.1.7 on 2021-04-02 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0020_remove_map_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='map',
            old_name='html_header',
            new_name='html_head',
        ),
    ]
