# Generated by Django 4.2.4 on 2023-08-21 22:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_rename_pointsperround_player_points_per_round'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='timesC',
        ),
        migrations.RemoveField(
            model_name='player',
            name='timesD',
        ),
    ]