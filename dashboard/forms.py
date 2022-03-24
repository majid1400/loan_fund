from django import forms
from .models import Members, Setting


class AccountCreateForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = ['group_id', 'name', 'family']


class SettingCreateForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = '__all__'
