from django.core.exceptions import ValidationError
from django.utils import simplejson as json


def validate_json(value):
    try:
        json.loads(value)
    except ValueError:
        raise ValidationError('Database extra is not JSON serializable')
