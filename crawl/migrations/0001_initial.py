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
                ('id', models.CharField(primary_key=True, unique=True, serialize=False, max_length=50)),
                ('title', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleRank',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('rank', models.IntegerField()),
                ('time', models.DateTimeField()),
                ('view', models.BooleanField(default=True)),
                ('article', models.ForeignKey(to='crawl.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(unique=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(unique=True, max_length=10)),
                ('url', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='host',
            field=models.ForeignKey(to='crawl.Host'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(to='crawl.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='host',
            field=models.ForeignKey(to='crawl.Host'),
        ),
    ]
