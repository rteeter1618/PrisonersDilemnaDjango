# Generated by Django 4.2.4 on 2023-08-16 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='name',
            field=models.TextField(default='default', max_length=100),
        ),
        migrations.AlterField(
            model_name='player',
            name='strategy',
            field=models.TextField(default='default'),
        ),
    ]
