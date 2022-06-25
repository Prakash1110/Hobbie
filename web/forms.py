from django import forms
from django.forms import widgets
from .models import ContactModel
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = '__all__'
        widgets = {
            'phone': PhoneNumberPrefixWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = str(visible.field.label)

class SearchForm(forms.Form):
    seacrh= forms.CharField()
