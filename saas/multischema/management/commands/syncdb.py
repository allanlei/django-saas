from optparse import make_option

from appschema.schema import schema_store
from appschema.utils import get_public_apps, get_isolated_apps, get_schemas, RunWithApps
from django.conf import settings
try:
    from south.management.commands import syncdb
except ImportError:
    from django.core.management.commands import syncdb

    
class Command(syncdb.Command):
    option_list = syncdb.Command.option_list + (
        make_option('--hostname', action='store', dest='hostname', default=None, help='Hostname of schema to use'),
        make_option('--schema', action='store', dest='schemaname', default=None, help='Nominates a specific schema to load fixtures into'),
        make_option('--allschemas', action='store_true', dest='allschemas', default=True, help='Performs run_dilla on all schemas'),
    )
    help = syncdb.Command.help + '\nWith schema supprt'
    
    def logging(self, message):
        if self.debug and settings.DEBUG:
            print message



    def handle_noargs(self, hostname=None, schemaname=None, allschemas=True, **options):
        self.debug = bool(options.get('verbosity', 0))
        
        public_apps = get_public_apps()
        if (hostname is None and schemaname is None) and len(public_apps):
            with RunWithApps(public_apps):
                installed_apps = list(settings.INSTALLED_APPS)
                self.logging('Syncing "master" for %d apps:' % len(installed_apps))
                schema_store.reset_path()
                for app in installed_apps:
                    self.logging('\t- %s' % app)
                super(Command, self).handle_noargs(**options)
                self.logging('\t* Synced')

        schemas = get_schemas(hostname=hostname, schemaname=schemaname, allschemas=allschemas)
        isolated_apps = get_isolated_apps()
        
        for schema in schemas:
            with schema:
                with RunWithApps(isolated_apps):
                    installed_apps = list(settings.INSTALLED_APPS)
                    self.logging('\n')
                    self.logging('Syncing "%s" for %d apps:' % (schema, len(installed_apps)))
                    for app in installed_apps:
                        self.logging('\t- %s' % app)
                    super(Command, self).handle_noargs(**options)
                    self.logging('\t* Synced')
