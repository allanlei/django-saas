from django.utils import unittest
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class MultiDBRouterTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def testCreate(self):
        pass
#        self.client.post(reverse('testdata_create') + '?domain=helveticode.com', {'value': 'fred'})
    
#    def testWrite(self):
#        for i in range(10):
#            User.objects.create(username='user%s' % i)
    
    def testRead(self):
        for i in 
        print User.objects.all()
