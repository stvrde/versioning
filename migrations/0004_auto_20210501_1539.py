# Generated by Django 3.1.7 on 2021-05-01 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('software', '0003_auto_20210426_1926'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bug',
            old_name='software',
            new_name='version',
        ),
    ]
