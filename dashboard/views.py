from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views import generic
from .forms import AccountCreateForm
from .models import Members, Transaction


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


def transaction_create_view(request):
    members = Members.objects.order_by('group_id').all()

    if request.method == 'POST':
        pk = request.POST.get("pk")
        fund = request.POST.get("fund")
        loan_p = request.POST.get("loan_p")
        payer_name = request.POST.get("payer_name")
        member = Members.objects.get(id=int(pk))
        transaction = Transaction.objects.create(
            Fund=fund, loan_p=loan_p, payer_name=payer_name, members=member
        )
        transaction.save()
        messages.info(request, 'داده شما با موفقیت ذخیره شد')
        return render(request, 'dashboard/transaction.html', {'formset': members, 'successful_submit': True})

    return render(request, 'dashboard/transaction.html', {'formset': members})
