# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-26 02:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0007_auto_20170325_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='pi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiment', to='foodcomputer.Pi'),
        ),
    ]
