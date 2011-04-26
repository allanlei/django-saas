from django import forms


class UserForm(forms.Form):
    value = forms.CharField()
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['value'].widget.attrs = {'autofocus': 'autofocus'}


class TestDataForm(forms.Form):
    value = forms.CharField()
    
    def __init__(self, *args, **kwargs):
        super(TestDataForm, self).__init__(*args, **kwargs)
        self.fields['value'].widget.attrs = {'autofocus': 'autofocus'}
