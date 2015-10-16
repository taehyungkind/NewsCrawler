from django.test import TestCase
from crawl.models import *
from crawl.views import db_initializer


class Test1(TestCase):
    def setUp(self):
        db_initializer(self)

    def test(self):
        hosts = Host.objects.all()
        print(hosts)
        for host in hosts:
            categories = Category.objects.filter(host=host)
            for category in categories:
                url = "http://localhost:8000/" + host.name + "/" + category.name
                print(url)

# Create your tests here.
