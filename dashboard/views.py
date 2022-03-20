from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .forms import AccountCreateForm, SettingCreateForm
from .models import Members, Transaction, Setting


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

class SettingCreateView(SuccessMessageMixin, generic.UpdateView):
    form_class = SettingCreateForm
    template_name = 'dashboard/setting.html'
    model = Setting
    success_message = "داده شما با موفقیت ذخیره شد"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["successful_submit"] = True
        return context

    def get_object(self, queryset=None):
        obj, created = Setting.objects.get_or_create()
        return obj


class AccountCreateView(SuccessMessageMixin, generic.CreateView):
    form_class = AccountCreateForm
    template_name = 'dashboard/account_create_form.html'
    success_message = "داده شما با موفقیت ذخیره شد"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["successful_submit"] = True
        return context


def account_detail_view(request, pk):
    context = {'member': get_object_or_404(Members, pk=pk)}

    list_trans = list(Transaction.objects.filter(members=pk).values_list('update', 'Fund'))

    counter_trans = 0
    current_trans = []
    for x in list_trans:
        counter_trans += int(x[1])
        current_trans.append(counter_trans)

    context['list_transaction'] = zip(list_trans, current_trans)
    context['total_capital'] = sum(list([int(x[1]) for x in list_trans]))

    return render(request, 'dashboard/account_detail_view.html', {'context': context, })


def transaction_create_view(request):
    list_form = qs_trans_merge_members_transaction_create_view()
    if request.method == 'POST':
        pk = request.POST.get("pk")
        fund = request.POST.get("fund").replace(',', '')
        loan_p = request.POST.get("loan_p").replace(',', '')
        payer_name = request.POST.get("payer_name")
        member = Members.objects.get(id=int(pk))
        if is_valid_fund(fund):
            transaction = Transaction.objects.create(
                Fund=fund, loan_p=loan_p, payer_name=payer_name, members=member
            )
            transaction.save()
            messages.info(request, 'داده شما با موفقیت ذخیره شد')
            list_form = qs_trans_merge_members_transaction_create_view()
            return render(request, 'dashboard/transaction.html', {'formset': list_form, 'successful_submit': True})
        messages.info(request, 'مقدار سرمایه کمتر از حد مجاز است')
        return render(request, 'dashboard/transaction.html', {'formset': list_form, 'successful_submit': True})

    return render(request, 'dashboard/transaction.html', {'formset': list_form})


def is_valid_fund(fund):
    setting = Setting.objects.all()
    minimum_share = setting[0].minimum_share
    return bool(int(fund) >= minimum_share)


def qs_trans_merge_members_transaction_create_view():
    members = Members.objects.order_by('group_id').all()
    qs_trans = Transaction.objects.order_by('-update').all()
    qs_total_capital = Transaction.objects.order_by('members').all()
    unique_trans = []
    for member in set(qs_trans.values_list('members', flat=True)):
        unique_trans.append(
            qs_trans.filter(members=member).values('Fund', 'loan_p', 'payer_name', 'members').first())

    for i in unique_trans:
        s = Transaction.objects.filter(members=i['members']).values_list('Fund', flat=True)
        i['total_capital'] = sum(list([int(x) for x in s]))

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
