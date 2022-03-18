from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
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
        list_form = qs_trans_merge_members_transaction_create_view()
        return render(request, 'dashboard/transaction.html', {'formset': list_form, 'successful_submit': True})

    list_form = qs_trans_merge_members_transaction_create_view()
    return render(request, 'dashboard/transaction.html', {'formset': list_form})


def qs_trans_merge_members_transaction_create_view():
    members = Members.objects.order_by('group_id').all()
    qs_trans = Transaction.objects.order_by('-update').all()
    unique_trans = []
    for member in set(qs_trans.values_list('members', flat=True)):
        unique_trans.append(
            qs_trans.filter(members=member).values('Fund', 'loan_p', 'payer_name', 'members').first())

    list_form = []
    for member in members:
        available = True
        for c in range(len(unique_trans)):
            if member.id == unique_trans[c]['members']:
                list_form.append({'member': member, 'trans': unique_trans[c]})
                available = False
                break

        if available:
            list_form.append({'member': member, 'trans': ''})
    return list_form

# TODO unittest member.id transaction.html
# TODO unittest unique_trans models Transaction
