# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 17:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcomputer', '0005_auto_20170206_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicetype',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]