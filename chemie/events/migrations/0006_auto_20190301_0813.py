# Generated by Django 2.1.3 on 2019-03-01 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20180927_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bedpresregistration',
            name='arrival_status',
            field=models.BooleanField(default=False, verbose_name='Møtt'),
        ),
    ]
