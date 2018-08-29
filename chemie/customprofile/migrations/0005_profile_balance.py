# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-29 18:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customprofile', '0004_profile_approved_terms'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=6),
            preserve_default=False,
        ),
    ]
