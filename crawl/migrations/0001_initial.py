# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=50, unique=True)),
                ('title', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleRank',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('rank', models.IntegerField()),
                ('time', models.DateTimeField()),
                ('view', models.BooleanField(default=True)),
                ('article', models.ForeignKey(to='crawl.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=10, unique=True)),
                ('url', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='host',
            field=models.ForeignKey(to='crawl.Host'),
        ),
        migrations.AddField(
            model_name='articlerank',
            name='category',
            field=models.ForeignKey(to='crawl.Category'),
        ),
    ]
