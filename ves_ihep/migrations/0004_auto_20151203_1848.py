# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ves_ihep', '0003_auto_20151203_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='script',
            name='script_path',
            field=models.CharField(max_length=120),
        ),
    ]
