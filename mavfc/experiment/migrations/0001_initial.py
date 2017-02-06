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
        ('foodcomputer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('descr', models.TextField()),
                ('collection_interval', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Experiment_Instance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instance_rules', to='experiment.Experiment')),
                ('pi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiment_instances', to='foodcomputer.Pi')),
            ],
        ),
        migrations.CreateModel(
            name='Experiment_Rule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hour', models.IntegerField()),
                ('minute', models.IntegerField()),
                ('baseline_target', models.FloatField()),
                ('baseline_variance', models.FloatField()),
                ('days', models.ManyToManyField(to='experiment.Day')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_rules', to='experiment.Experiment')),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiment_rules', to='experiment.Experiment')),
            ],
        ),
        migrations.CreateModel(
            name='User_Experiment_Instance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_user', models.BooleanField()),
                ('experiment_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instance_users', to='experiment.Experiment_Instance')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='experiment_instances', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
