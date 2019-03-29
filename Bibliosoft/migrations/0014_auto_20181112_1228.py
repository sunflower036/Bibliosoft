# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-12 04:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bibliosoft', '0013_post_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='librarian',
            name='name',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AddField(
            model_name='reader',
            name='name',
            field=models.CharField(default='', max_length=32),
        ),
    ]
