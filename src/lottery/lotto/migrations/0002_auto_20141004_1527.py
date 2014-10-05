# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import lottery.lotto.models


class Migration(migrations.Migration):

    dependencies = [
        ('lotto', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lottery',
            options={'verbose_name_plural': 'Lotteries'},
        ),
        migrations.AddField(
            model_name='lottery',
            name='active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lottery',
            name='end_date',
            field=models.DateTimeField(default=lottery.lotto.models.default_end_date),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lottery',
            name='start_date',
            field=models.DateTimeField(default=datetime.date(2014, 10, 4), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lottery',
            name='slug',
            field=models.SlugField(help_text='Automatically pre-populated from title', unique=True, max_length=255),
        ),
    ]
