# Generated by Django 3.1.2 on 2020-11-08 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20201108_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='imageurl',
            field=models.URLField(default=''),
        ),
    ]
