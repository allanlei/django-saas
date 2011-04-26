# -*- coding: utf-8 -*-
#
# This file is part of Django appschema released under the MIT license.
# See the LICENSE for more information.

from django.core.management.base import NoArgsCommand
from optparse import make_option
from appschema.models import Schema

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--name', action='store', dest='name', default=None, help='Name of the schema'),
        make_option('--hostname', action='store', dest='hostname', default=None, help='Hostname of the schema'),
    )
    help = 'Creates a new active schema'
    
    def handle_noargs(self, name=None, hostname=None, **options):
        if hostname is None:
            raise Exception('Needs hostname')
        elif name is None:
            name = hostname
        Schema.objects.create(name=name, public_name=hostname)
