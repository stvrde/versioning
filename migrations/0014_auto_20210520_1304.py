# Generated by Django 3.1.7 on 2021-05-20 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('software', '0013_auto_20210520_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='softwareversion',
            name='software',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='software.software'),
        ),
    ]
