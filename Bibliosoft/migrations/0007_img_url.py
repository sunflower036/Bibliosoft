# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-11 05:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bibliosoft', '0006_librarian'),
    ]

    operations = [
        migrations.AddField(
            model_name='img',
            name='url',
            field=models.CharField(default='none', max_length=32),
        ),
    ]
