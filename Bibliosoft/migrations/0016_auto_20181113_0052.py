# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-12 16:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bibliosoft', '0015_auto_20181112_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posttext',
            name='address',
            field=models.CharField(default='Xi_an', max_length=100),
        ),
        migrations.AlterField(
            model_name='posttext',
            name='auth',
            field=models.TextField(default='lmz'),
        ),
    ]
