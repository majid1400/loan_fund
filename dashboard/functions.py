from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from dashboard.models import Transaction, Members, PeriodLoan


def get_unique_transaction_month():
    date_end = datetime.now()
    date_start = datetime.today().replace(day=1)
    qs_trans = Transaction.objects.order_by('-id').filter(create__range=(date_start, date_end))
    unique_trans = []
    for member in set(qs_trans.values_list('members', flat=True)):
        unique_trans.append(
            qs_trans.filter(members=member).values('Fund', 'loan_p', 'payer_name', 'members').first()
        )
    return unique_trans


def get_sum_cash_desk_month():
    total_fund_month = 0
    for i in get_unique_transaction_month():
        if i['Fund']: total_fund_month += int(i['Fund'])
        if i['loan_p']: total_fund_month += int(i['loan_p'])
    return total_fund_month


def get_object_members(pk):
    try:
        member = Members.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return False
    return member


def get_list_members_month():
    list_members = []
    for item in get_unique_transaction_month():
        list_members.append(get_object_members(item['members']))
    return list_members


def get_total_capital_member(pk):
    fund = 0
    for item in Transaction.objects.filter(members=pk).values('Fund'):
        fund += int(item['Fund'])
    return fund


def get_choice_member_loan():
    sum_cash_desk_month = get_sum_cash_desk_month()
    # sum_cash_desk_month = 6000000
    sum_wage_member = 0
    sum_wage_cashier_member = 0
    counter = 0
    context = {}
    for index, period_loan_member in enumerate(PeriodLoan.objects.order_by('period_loan').all()):
        if period_loan_member.members in get_list_members_month():
            loan = int(get_total_capital_member(period_loan_member.members.id) * 2)
            if sum_cash_desk_month >= loan:
                sum_cash_desk_month -= int(loan)
                wage_cash_desk = int(loan * 0.002)
                wage_cashier = int(loan * 0.005)
                sum_wage = wage_cash_desk + wage_cashier
                payment = loan - sum_wage
                before_loan = 0
                final_payment = payment - before_loan
                sum_wage_member += wage_cash_desk
                sum_wage_cashier_member += wage_cashier
                counter += 1
                context[str(index)] = {'member': period_loan_member.members, 'loan': loan,
                                       'sum_cash_desk_month': sum_cash_desk_month,
                                       'wage_cash_desk': wage_cash_desk, 'wage_cashier': wage_cashier,
                                       'sum_wage': sum_wage, 'payment': payment, 'before_loan': before_loan,
                                       'final_payment': final_payment}

            else:
                break
    context['wage'] = {'sum_wage_member': sum_wage_member,
                       'sum_wage_cashier_member': sum_wage_cashier_member,
                       'end': 1, 'number_loan': counter,
                       'sum_cash_desk_month': sum_cash_desk_month}
    return context