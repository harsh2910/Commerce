# Generated by Django 3.2 on 2021-06-04 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_listing_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='name',
            field=models.CharField(max_length=32),
        ),
    ]
