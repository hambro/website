# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-15 17:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('committiees', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='Committee',
            new_name='committee',
        ),
    ]