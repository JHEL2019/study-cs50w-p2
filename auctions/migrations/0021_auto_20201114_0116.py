# Generated by Django 3.1.2 on 2020-11-14 01:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_auto_20201114_0111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='userid',
            new_name='user',
        ),
    ]
