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
                ('id', models.CharField(primary_key=True, max_length=30, unique=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='CrawlTime',
            fields=[
                ('article_ptr', models.OneToOneField(auto_created=True, parent_link=True, to='crawl.Article', primary_key=True, serialize=False)),
                ('rank', models.IntegerField()),
                ('time', models.DateTimeField()),
                ('view', models.BooleanField(default=True)),
            ],
            bases=('crawl.article',),
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
