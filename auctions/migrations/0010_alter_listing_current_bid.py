# Generated by Django 4.1.5 on 2023-01-29 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_listing_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='current_bid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]