# Generated by Django 3.1.2 on 2020-11-14 14:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auto_20201114_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='users',
            field=models.ManyToManyField(through='auctions.Bid', to=settings.AUTH_USER_MODEL),
        ),
    ]
