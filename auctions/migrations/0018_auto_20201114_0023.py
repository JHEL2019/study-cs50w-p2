# Generated by Django 3.1.2 on 2020-11-14 00:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_auto_20201114_0022'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='owner',
            new_name='owner_id',
        ),
    ]
