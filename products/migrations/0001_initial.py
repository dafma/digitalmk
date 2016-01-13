# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, default=9.99, max_digits=100)),
                ('sale_price', models.DecimalField(decimal_places=2, default=6.99, null=True, blank=True, max_digits=100)),
            ],
        ),
    ]
