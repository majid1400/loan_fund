from django import forms
from .models import Members


class AccountCreateForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = ['group_id', 'name', 'family']
