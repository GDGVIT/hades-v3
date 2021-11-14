# Generated by Django 3.2.8 on 2021-11-12 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0009_auto_20211112_1348'),
        ('event', '0004_alter_participant_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perm', models.CharField(max_length=10)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permissions', to='event.event')),
                ('role', models.ManyToManyField(related_name='permissions', to='organisation.Role')),
            ],
        ),
    ]
