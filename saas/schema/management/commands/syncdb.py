from django.conf import settings
from django.utils.functional import curry

from optparse import make_option
from tenancy.base.signals import tenant_selection

try:
    from south.management.commands import syncdb
except ImportError:
    from django.core.management.commands import syncdb
        

class Command(syncdb.Command):
    option_list = syncdb.Command.option_list + (
        make_option('--tenant', action='store', dest='tenant', default=None, help='Tenant'),
    )
    
    def handle_noargs(self, tenant=None, **kwargs):
        ts = curry(lambda sender, **kwargs: kwargs.get('tenant', None), tenant=tenant)
        tenant_selection.connect(ts)
        from django.db import connection, transaction
        cursor = connection.cursor()
        cursor.execute('SET search_path = %s;', [tenant or 'public'])
        transaction.commit_unless_managed()
        
        super(Command, self).handle_noargs(**kwargs)
        tenant_selection.disconnect(ts)
