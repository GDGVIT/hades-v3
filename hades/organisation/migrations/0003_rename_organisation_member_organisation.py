# Generated by Django 3.2.8 on 2021-10-30 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0002_member'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='Organisation',
            new_name='organisation',
        ),
    ]
