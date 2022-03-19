from django import forms
from .models import Members, Setting


class AccountCreateForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = ['group_id', 'name', 'family']


class SettingCreateForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = ['loan_ratio', 'number_months_loan_repayment', 'minimum_share']
