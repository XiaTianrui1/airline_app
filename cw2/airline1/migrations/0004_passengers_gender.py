# Generated by Django 3.2.10 on 2023-05-11 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline1', '0003_auto_20230511_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='passengers',
            name='gender',
            field=models.CharField(default='Male', max_length=50),
        ),
    ]
