from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from .forms import AccountCreateForm, TransactionForm
from .models import Members, PeriodLoan


# Create your views here.
# def home(request):
#     if request.method == 'POST':
#         form = OpenAccountForm(request.POST)
#         if form.is_valid():
#             group_id = form.cleaned_data["group_id"]
#             name = form.cleaned_data["name"]
#             family = form.cleaned_data["family"]
#             data = Members(group_id=group_id, name=name, family=family)
#
#             obj = PeriodLoan.objects.order_by('period_loan').last()
#             number = obj.period_loan + 1
#
#
#             try:
#                 data.save()
#                 memid = Members.objects.order_by('id').last()
#                 lastid = memid.id
#                 period = PeriodLoan(period_loan=number, members_id=lastid)
#                 period.save()
#             except IntegrityError:
#                 messages.error(request,
#                                'داده تکراری')
#                 return render(request, 'dashboard/open-an-account.html',
#                               {'form': form, 'successful_submit': True})
#             else:
#
#                 messages.info(request,
#                               'داده شما با موفقیت ذخیره شد')
#                 return render(request, 'dashboard/open-an-account.html',
#                               {'form': form, 'successful_submit': True})
#
#
#     else:
#         form = OpenAccountForm()
#     return render(request, 'dashboard/open-an-account.html', {"form": form})

class AccountCreateView(SuccessMessageMixin, generic.CreateView):
    form_class = AccountCreateForm
    template_name = 'dashboard/account_create_form.html'
    success_message = "داده شما با موفقیت ذخیره شد"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["successful_submit"] = True
        return context


def transaction(request):
    members = Members.objects.order_by('group_id').all()
    d = {}
    for i in members:
        if i.group_id in d:
            d[i.group_id].append(i)
        else:
            d[i.group_id] = [i]
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            fund = form.cleaned_data["fund"]
            loan_p = form.cleaned_data["loan_p"]
            payer_name = form.cleaned_data["payer_name"]
            status_transaction = form.cleaned_data["status_transaction"]
            messages.info(request,
                          'داده شما با موفقیت ذخیره شد')
            return render(request, 'dashboard/open-an-account.html',
                          {'form': form, 'successful_submit': True})

    form = TransactionForm()
    return render(request, 'dashboard/transaction.html', {'form': form, 'members': d})
