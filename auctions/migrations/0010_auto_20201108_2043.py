# Generated by Django 3.1.2 on 2020-11-08 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_listing_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image_url',
            field=models.URLField(blank=True, default=''),
        ),
    ]