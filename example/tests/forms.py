from django import forms
from django.conf import settings
from django.db.models import get_model

from saas.multidb.models import Database

class TestDataForm(forms.Form):
    value = forms.CharField()
    database = forms.ChoiceField()
    model = forms.ChoiceField()
    number = forms.IntegerField(initial=1)
    
    def __init__(self, models=[], *args, **kwargs):
        super(TestDataForm, self).__init__(*args, **kwargs)
        self.fields['value'].widget.attrs = {'autofocus': 'autofocus'}
        self.fields['model'].choices = [(model._meta.db_table, model.__name__) for model in models]
        self.fields['database'].choices = [(db, db) for db in settings.DATABASES.keys()]
    
    def clean_model(self):
        app_label, model_name = self.cleaned_data['model'].split('_')
        return get_model(app_label, model_name)

class DatabaseForm(forms.ModelForm):
    class Meta:
        model = Database
        exclude = ('extra', )
    
    def __init__(self, *args, **kwargs):
        super(DatabaseForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.help_text = ''
    
    def clean_name(self):
        return '%s%s' % (settings.DATABASE_DIR if 'sqlite' in self.cleaned_data['engine'] else '', self.cleaned_data['name'])
