# Generated by Django 3.1.2 on 2020-11-08 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_listing_imageurl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='imageurl',
        ),
        migrations.AddField(
            model_name='listing',
            name='image_url',
            field=models.URLField(default='', null=True),
        ),
    ]
