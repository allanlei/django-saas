from django import forms
from django.conf import settings
from django.db.models import get_model

class TestDataForm(forms.Form):
    value = forms.CharField()
    database = forms.ChoiceField(choices=[(db, db) for db in settings.DATABASES.keys()])
    model = forms.ChoiceField()
    
    def __init__(self, models=[], *args, **kwargs):
        super(TestDataForm, self).__init__(*args, **kwargs)
        self.fields['value'].widget.attrs = {'autofocus': 'autofocus'}
        self.fields['model'].choices = [(model._meta.db_table, model.__name__) for model in models]
    
    def clean_model(self):
        app_label, model_name = self.cleaned_data['model'].split('_')
        return get_model(app_label, model_name)
