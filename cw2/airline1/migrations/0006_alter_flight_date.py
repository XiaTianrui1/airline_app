# Generated by Django 3.2.10 on 2023-05-11 17:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline1', '0005_auto_20230512_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='date',
            field=models.DateField(default=datetime.date(2023, 5, 12)),
        ),
    ]
