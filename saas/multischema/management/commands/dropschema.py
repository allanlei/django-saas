# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from optparse import make_option
from appschema.models import Schema

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--name', action='store', dest='name', default=None, help='Name of the schema'),
        make_option('--hostname', action='store', dest='hostname', default=None, help='Hostname of the schema'),
    )
    help = 'Drop an active schema'
    
    def handle_noargs(self, name=None, hostname=None, **options):
        filters = {}
        if hostname:
            filters['public_name'] = hostname
        elif name:
            filters['name'] = name
        schema = Schema.objects.get(**filters)
        schema.delete()
