from django.dispatch import Signal


db_route_read = Signal(providing_args=[])
db_route_write = Signal(providing_args=[])

db_pre_load = Signal(providing_args=['instance'])
db_post_load = Signal(providing_args=['instance'])

db_pre_unload = Signal(providing_args=['instance'])
db_post_unload = Signal(providing_args=['instance'])

db_pre_disconnect = Signal(providing_args=['instance'])
db_post_disconnect = Signal(providing_args=['instance'])
