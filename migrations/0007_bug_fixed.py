# Generated by Django 3.1.7 on 2021-05-01 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('software', '0006_auto_20210501_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='bug',
            name='fixed',
            field=models.BooleanField(default=False),
        ),
    ]
