# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawl', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('message', models.CharField(max_length=200)),
                ('time', models.DateTimeField()),
                ('host', models.ForeignKey(to='crawl.Host')),
            ],
        ),
    ]
