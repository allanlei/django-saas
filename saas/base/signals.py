from django.dispatch import Signal

tenant_selection = Signal(providing_args=['tenant'])
