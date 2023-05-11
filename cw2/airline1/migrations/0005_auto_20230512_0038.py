# Generated by Django 3.2.10 on 2023-05-11 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline1', '0004_passengers_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='remaining_first_seats',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='flight',
            name='remaining_seats',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='flight',
            name='remaining_second_seats',
            field=models.IntegerField(default=30),
        ),
        migrations.AddField(
            model_name='flight',
            name='remaining_third_seats',
            field=models.IntegerField(default=100),
        ),
    ]
