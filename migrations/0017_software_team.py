# Generated by Django 3.1.7 on 2021-06-14 10:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('software', '0016_auto_20210614_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='software',
            name='team',
            field=models.ManyToManyField(related_name='collabolator_in', to=settings.AUTH_USER_MODEL),
        ),
    ]