# Generated by Django 3.1.2 on 2020-11-08 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20201108_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='comments',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='auctions.comment'),
        ),
    ]
