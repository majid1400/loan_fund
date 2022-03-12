from django import forms

from .models import STATUS_TRANSACTION, Members


# class OpenAccountForm(forms.Form):
#     group_id = forms.IntegerField(label="شماره گروه")
#     name = forms.CharField(label='نام')
#     family = forms.CharField(label='نام خانوادگی')

class AccountCreateForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = ['group_id', 'name', 'family']


class TransactionForm(forms.Form):
    fund = forms.IntegerField(label="مقدار سرمایه")
    loan_p = forms.IntegerField(label="وام")
    payer_name = forms.CharField(label="نام پرداخت کنند")
    status_transaction = forms.CharField(label="نوع پرداخت",
                                         max_length=3,
                                         widget=forms.Select(choices=STATUS_TRANSACTION))
