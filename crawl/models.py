from django.db import models
# Create your models here.


class Host(models.Model):
    name = models.CharField(max_length=10, unique=True)
    url = models.CharField(max_length=100)
    # TODO host와 category는 따로 값을 넣어두어야 할듯


class Category(models.Model):
    host = models.ForeignKey(Host)
    name = models.CharField(max_length=20)


class Article(models.Model):
    id = models.CharField(max_length=50, primary_key=True, unique=True, null=False)
    host = models.ForeignKey(Host)
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=100, null=False)
    url = models.CharField(max_length=500, null=False)


class ArticleRank(models.Model):
    article = models.ForeignKey(Article)
    rank = models.IntegerField(null=False)
    time = models.DateTimeField()
    view = models.BooleanField(default=True)
