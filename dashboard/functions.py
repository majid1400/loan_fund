from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from dashboard.models import Transaction, Members, PeriodLoan, Setting, Loan, Cash


def get_unique_transaction_month():
    date_end = datetime.now()
    date_start = date_end - timedelta(days = 1)
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


def check_loan(loan):
    maximum_loan = get_setting()[0].maximum_loan
    if loan >= maximum_loan:
        return maximum_loan
    return loan


def get_choice_member_loan():
    sum_cash_desk_month = get_sum_cash_desk_month()
    sum_wage_member = 0
    sum_wage_cashier_member = 0
    counter = 0
    context = {}
    for index, period_loan_member in enumerate(PeriodLoan.objects.order_by('period_loan').all()):
        # TODO: check (if) is_receive_loan False and Installment loans zero
        if period_loan_member.members in get_list_members_month():
            loan_checker = int(get_total_capital_member(period_loan_member.members.id) * get_setting()[0].loan_ratio)
            loan = check_loan(loan_checker)
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
                       'sum_cash_desk_month': sum_cash_desk_month,
                       'get_sum_cash_desk_month': get_sum_cash_desk_month()}
    return context


def get_choice_member_loan_manual(*args):
    context = {}
    sum_wage_member = 0
    sum_wage_cashier_member = 0
    counter = 0
    sum_cash_desk_month = get_sum_cash_desk_month()
    for index, value in enumerate(args[0]):
        member_id = int(value[1])
        loan = clear_number(value[0])
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
            context[str(index)] = {'member': get_object_members(member_id), 'loan': loan,
                                   'sum_cash_desk_month': sum_cash_desk_month,
                                   'wage_cash_desk': wage_cash_desk, 'wage_cashier': wage_cashier,
                                   'sum_wage': sum_wage, 'payment': payment, 'before_loan': before_loan,
                                   'final_payment': final_payment}
        else:
            break
    context['wage'] = {'sum_wage_member': sum_wage_member,
                       'sum_wage_cashier_member': sum_wage_cashier_member,
                       'end': 1, 'number_loan': counter,
                       'sum_cash_desk_month': sum_cash_desk_month,
                       'get_sum_cash_desk_month': get_sum_cash_desk_month()}
    return context


def clear_number(number):
    return int(number.replace(",", ""))


def get_setting():
    return Setting.objects.all()


def number_of_installment_loans(loan):
    repayment = Setting.objects.values('number_months_loan_repayment').last()['number_months_loan_repayment']
    return int(repayment) / loan


def get_installment_loans(members):
    try:
        return Loan.objects.filter(members=members).values('installment_loans').last()['installment_loans']
    except TypeError:
        return 0


def get_total_wage():
    try:
        return Cash.objects.values('total_wage').last()['total_wage']
    except TypeError:
        return 0


def check_is_receive_loan_member(list_members):
    for member in list(list_members):
        if int(get_installment_loans(member)) != 0:
            return False
    return True


def handler_submit_final_loan(loan, member, wage_before_month, money_before_month):
    repayment = Setting.objects.values('number_months_loan_repayment').last()['number_months_loan_repayment']
    for loan, member in list(zip(loan, member)):
        PeriodLoan.objects.filter(members=member).update(is_receive_loan=True)
        Loan.objects.update_or_create(date_receive_loan=datetime.now(),
                                      receive_loan=clear_number(loan),
                                      installment_loans=int(repayment),
                                      members=get_object_members(member))

    total = get_total_wage() + int(wage_before_month)
    result = Cash.objects.update(money_before_month=money_before_month,
                                 wage_before_month=wage_before_month,
                                 total_wage=total)
    if int(result) == 0:
        Cash.objects.create(money_before_month=money_before_month,
                            wage_before_month=wage_before_month,
                            total_wage=total)

# TODO: unittest get_choice_member_loan, number_of_installment_loans,
#  get_total_wage, check_is_receive_loan_member, handler_submit_final_loan
