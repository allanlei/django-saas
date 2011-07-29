from django.conf import settings

def settings_context(*args, **kwargs):
    return {'settings': settings}
