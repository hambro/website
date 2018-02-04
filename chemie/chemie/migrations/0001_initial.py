# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-27 19:01
from __future__ import unicode_literals

import chemie.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='pictures_for_404',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', sorl.thumbnail.fields.ImageField(upload_to='404', verbose_name='tullebilde')),
            ],
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=200, validators=[chemie.validators.validate_http], verbose_name='Link')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField()),
                ('image', sorl.thumbnail.fields.ImageField(upload_to='sponsors', verbose_name='Bilde')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
