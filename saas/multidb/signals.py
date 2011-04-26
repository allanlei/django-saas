import django.dispatch

db_route_read = django.dispatch.Signal(providing_args=[])
db_route_write = django.dispatch.Signal(providing_args=[])






#from django.db.models.signals import post_save
#import subprocess

#def post_save_createdb(sender, database, created, **kwargs):
#    if created:
#        print 'CREATE DB'
#        if database.engine == 'django.db.backends.postgresql_psycopg2':
#            user = ['-U', database.user]
#            password = ['']
#        
#        
#        
#            subprocess.call(['createdb', '-U', database.user])
#        
#post_save.connect(post_save_createdb, sender=Database)
