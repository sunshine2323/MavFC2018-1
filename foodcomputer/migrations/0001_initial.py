# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 06:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_line_1', models.CharField(max_length=75)),
                ('street_line_2', models.CharField(max_length=75)),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=2)),
                ('zip', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('data_value', models.FloatField()),
                ('is_anomaly', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Data_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('descr', models.TextField()),
                ('min_limit', models.FloatField()),
                ('max_limit', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=50, verbose_name='Device ID')),
                ('upper_variance', models.FloatField()),
                ('lower_variance', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Device_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_controller', models.BooleanField()),
                ('data_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_types', to='foodcomputer.Data_Type')),
            ],
        ),
        migrations.CreateModel(
            name='Pi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pi_SN', models.CharField(max_length=50, verbose_name='Serial Number')),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pis', to='foodcomputer.Address')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pis', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Unit_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('abbr', models.CharField(max_length=10)),
                ('descr', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='device_type',
            name='unit_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_types', to='foodcomputer.Unit_Type'),
        ),
        migrations.AddField(
            model_name='device',
            name='device_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='foodcomputer.Device_Type'),
        ),
        migrations.AddField(
            model_name='device',
            name='pi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='foodcomputer.Pi'),
        ),
        migrations.AddField(
            model_name='data',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data', to='foodcomputer.Device'),
        ),
    ]
