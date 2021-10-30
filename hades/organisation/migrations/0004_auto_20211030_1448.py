# Generated by Django 3.2.8 on 2021-10-30 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organisation', '0003_rename_organisation_member_organisation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organisation', to='organisation.organisation'),
        ),
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
