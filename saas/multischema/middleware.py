# -*- coding: utf-8 -*-
#
# This file is part of Django appschema released under the MIT license.
# See the LICENSE for more information.

from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages

from appschema.schema import schema_store
from appschema.models import Schema
import re

class NoSchemaError(Http404):
    pass

class FqdnMiddleware(object):
    """
    This Middleware sets schema based on FQDN.
    FQDN should be the public_name in your schema table.
    """
    def should_process(self, request):
        if settings.MEDIA_URL and request.path.startswith(settings.MEDIA_URL):
            return False
        
        if settings.ADMIN_MEDIA_PREFIX and request.path.startswith(settings.ADMIN_MEDIA_PREFIX):
            return False
        
        if request.path == '/favicon.ico':
            return False
        return True
    
    #Rewrite this
    def process_request(self, request):
        if self.should_process(request):
            try:
                fqdn = request.path.split('/')[1]
                if not re.search(settings.DOMAIN_NAME_REGEX_NO_CATCH_C, fqdn):
                    return None
                schema = Schema.objects.get(is_active=True, public_name=fqdn)
                schema.enter()
            except IndexError:
                return None
            except Schema.DoesNotExist:
                raise NoSchemaError()
                
    def process_response(self, request, response):
        if self.should_process(request):
            schema_store.clear()
        return response
    
    def process_exception(self, request, exception):
        if self.should_process(request):
            schema_store.clear()
