# -*- coding: utf-8 -*-
#
# This file is part of Django appschema released under the MIT license.
# See the LICENSE for more information.
from optparse import make_option

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from appschema.models import Schema

from subprocess import Popen, PIPE
import shutil
import re
import os


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--pgdump_cmd', action='store', dest='pg_dump', default='pg_dump', help='Path to pg_dump command'),
        make_option('--filename', action='store', dest='filename', default=getattr(settings, 'PG_MASTER_TEMPLATE', None), help='Write output to this file'),
        make_option('--format', action='store', dest='format', default='raw', choices=['raw', 'python'], help='Output dump in a python string.'),
    )
    help = "Dumps the whole base schema creation and gives result on stdout."
    
    def handle(self, pg_dump='pg_dump', filename=getattr(settings, 'PG_MASTER_TEMPLATE', None), format='raw', *args, **options):
        schema, created = Schema.objects.get_or_create(name='__master__')

        call_command('syncdb', schema=schema.name, verbosity=options.get('verbosity', 0), interactive=False)
        call_command('migrate', schema=schema.name, verbosity=options.get('verbosity', 0), interactive=False)
        
        dump = self.dump(schema.name)
        if format == 'python':
            dump = self.format_python(dump, schema.name)
        dump= self.format(dump)
            
        if filename:
            if os.path.exists(filename):
                shutil.copyfile(filename, '%s.bak' % filename)
            self.write(filename, dump)
        schema.delete()
        
    def dump(self, schemaname):
        pf = Popen(
            [pg_dump,
                '--schema-only',
                '--schema', schemaname,
                '--no-owner',
                '--inserts',
                '-U',
                settings.DATABASES['default']['USER'],
                settings.DATABASES['default']['NAME']
            ],
            env={'PGPASSWORD': settings.DATABASES['default']['PASSWORD']},
            stdout=PIPE
        )
        return pf.communicate()[0]
            
    def format(self, dump):
        re_comments = re.compile(r'^--.*\n', re.M)
        re_duplines = re.compile(r'^\n\n+', re.M)
        dump = re_comments.sub('', dump)
        dump = re_duplines.sub('\n', dump)
        return dump
        
    def format_python(self, dump, schemaname):
        dump = dump.replace('%', '%%')
        dump = dump.replace(schemaname, '%(schema_name)s')
        dump = '# -*- coding: utf-8 -*-\nschema_sql = """%s"""' % dump
        return dump
    
    def write(self, filename, dump):
        f = open(filename,'w+')
        print 'Writing master pgsql template file to %s...' % filename
        f.write(dump)
        f.close()
