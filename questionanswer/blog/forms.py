from django import forms
from .models import Option

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['name', 'correct']
