# Generated by Django 3.1.2 on 2020-11-11 22:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20201111_2010'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='users',
            new_name='user',
        ),
    ]
