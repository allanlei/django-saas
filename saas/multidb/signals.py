import django.dispatch

db_route_read = django.dispatch.Signal(providing_args=[])
db_route_write = django.dispatch.Signal(providing_args=[])
