# Generated by Django 3.1.2 on 2020-11-10 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20201108_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='owner',
            field=models.IntegerField(default='1'),
        ),
    ]
