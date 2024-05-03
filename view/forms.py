from django import forms
from .models import Person

class YourModelForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'farsi_name', 'father']
