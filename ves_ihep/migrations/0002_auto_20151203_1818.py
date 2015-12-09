# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ves_ihep', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='script',
            name='script_type',
            field=models.CharField(max_length=120),
        ),
    ]
