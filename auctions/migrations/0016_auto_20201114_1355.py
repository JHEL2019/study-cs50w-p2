# Generated by Django 3.1.2 on 2020-11-14 13:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_auto_20201111_2302'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['id']},
        ),
        migrations.RemoveField(
            model_name='listing',
            name='updatedate',
        ),
        migrations.AlterField(
            model_name='listing',
            name='users',
            field=models.ManyToManyField(null=True, through='auctions.Bid', to=settings.AUTH_USER_MODEL),
        ),
    ]
