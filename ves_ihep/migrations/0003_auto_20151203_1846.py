# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ves_ihep', '0002_auto_20151203_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='script',
            name='script_name',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='script',
            name='script_type',
            field=models.CharField(max_length=30),
        ),
    ]
