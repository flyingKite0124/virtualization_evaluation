# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity_name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActivityHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('result', models.TextField(null=True, blank=True)),
                ('start_time', models.DateTimeField(null=True, blank=True)),
                ('finish_time', models.DateTimeField(null=True, blank=True)),
                ('activity', models.ForeignKey(to='ves_ihep.Activity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('IP', models.IPAddressField()),
                ('username', models.CharField(max_length=128)),
                ('passwd', models.CharField(max_length=128)),
                ('status', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Scene',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('stable', models.BooleanField(default=False)),
                ('slug', models.SlugField(default=b'', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SceneHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scene', models.ForeignKey(to='ves_ihep.Scene')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('script_name', models.CharField(max_length=30)),
                ('upload_time', models.DateTimeField()),
                ('script_type', models.CharField(max_length=30)),
                ('script_path', models.CharField(max_length=60)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='activityhistory',
            name='host',
            field=models.ForeignKey(to='ves_ihep.Host'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activityhistory',
            name='scene_history',
            field=models.ForeignKey(to='ves_ihep.SceneHistory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='scene',
            field=models.ForeignKey(to='ves_ihep.Scene'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='script',
            field=models.ForeignKey(to='ves_ihep.Script'),
            preserve_default=True,
        ),
    ]
