import time
from django.test import TestCase
from django.urls import reverse
from .forms import AccountCreateForm
from .functions import get_unique_transaction_month, get_sum_cash_desk_month, get_object_members, \
    get_list_members_month, get_choice_member_loan
from .models import Members, Transaction, Setting, PeriodLoan
from .views import qs_trans_merge_members_transaction_create_view


class DashboardTest(TestCase):
    def setUp(self):
        self.member = Members.objects.create(
            group_id=1,
            name="ali",
            family="alavi"
        )
        self.transaction = Transaction.objects.create(
            Fund='200000', loan_p='3000000', payer_name='ali', members=self.member
        )
        self.setting = Setting.objects.create(
            loan_ratio='2',
            number_months_loan_repayment="200",
            minimum_share="200000",
            maximum_loan="100000000"
        )

    def test_create_account(self):
        data = {'group_id': 2, 'name': 'maryam', 'family': 'alavi'}
        response = self.client.post(reverse("account_create"), data=data)

        member = Members.objects.last()
        period = PeriodLoan.objects.last()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(member.group_id, 2)
        self.assertEqual(member.name, 'maryam')
        self.assertEqual(member.family, 'alavi')
        self.assertEqual(period.members_id, member.pk)
        self.assertEqual(period.period_loan, 1)

    def test_member_duplicate(self):
        form_data = {'group_id': 2, 'name': 'ali', 'family': 'alavi'}
        form = AccountCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

    def test_create_models_transaction(self):
        member = Members.objects.get(id=int(self.member.id))
        transaction = Transaction.objects.create(
            Fund='200000', loan_p='3000000', payer_name='ali', members=member
        )
        self.assertEqual(transaction.Fund, '200000')
        self.assertEqual(transaction.loan_p, '3000000')
        self.assertEqual(transaction.payer_name, 'ali')
        self.assertEqual(transaction.members, member)

    def test_create_view_transaction(self):
        data = {'fund': '200000', 'loan_p': '3000000', 'payer_name': 'ali', 'pk': self.member.pk}
        response = self.client.post(reverse("transaction"), data=data)

        trans = Transaction.objects.last()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(trans.Fund, "200000")
        self.assertEqual(trans.loan_p, "3000000")
        self.assertEqual(trans.payer_name, "ali")
        self.assertEqual(1, self.member.pk)
        self.assertEqual(trans.pk, 2)

    def test_qs_trans_merge_members_transaction_create_view(self):
        member = Members.objects.get(id=int(self.member.id))
        time.sleep(1)
        Transaction.objects.create(
            Fund='300000', loan_p='4000000', payer_name='ali', members=member
        )
        result = qs_trans_merge_members_transaction_create_view()
        self.assertEqual(result[0]['member'], member)
        self.assertEqual(result[0]['trans']['Fund'], '300000')
        self.assertEqual(result[0]['trans']['loan_p'], '4000000')
        self.assertEqual(result[0]['trans']['total_capital'], 500000)

    def test_create_update_models_setting(self):
        data = {'loan_ratio': '20', 'number_months_loan_repayment': '200', 'minimum_share': '1000',
                'maximum_loan': '100000'}
        self.client.post(reverse("setting"), data=data)

        data2 = {'loan_ratio': '2', 'number_months_loan_repayment': '20', 'minimum_share': '200000',
                 'maximum_loan': '100000000'}
        self.client.post(reverse("setting"), data=data2)

        setting = Setting.objects.all()
        self.assertEqual(len(setting), 1)
        self.assertEqual(setting[0].loan_ratio, 2)
        self.assertEqual(setting[0].number_months_loan_repayment, 20)
        self.assertEqual(setting[0].minimum_share, 200000)
        self.assertEqual(setting[0].maximum_loan, 100000000)

    def test_account_detail_view(self):
        response = self.client.get(reverse('account_detail', args=[self.member.pk]))
        self.assertEqual(response.status_code, 200)

    def test_choice_loan_view(self):
        response = self.client.post(reverse("choice_loan"))
        self.assertEqual(response.status_code, 200)

    def test_get_unique_transaction_month(self):
        Transaction.objects.create(
            Fund='500000', loan_p='5000000', payer_name='ali', members=self.member
        )
        result = get_unique_transaction_month()
        self.assertEqual(result[0]['Fund'], '500000')
        self.assertEqual(result[0]['loan_p'], '5000000')
        self.assertEqual(result[0]['payer_name'], 'ali')
        self.assertEqual(result[0]['members'], self.member.pk)

    def test_get_sum_cash_desk_month(self):
        Transaction.objects.create(
            Fund='500000', loan_p='5000000', payer_name='ali', members=self.member
        )
        result = get_sum_cash_desk_month()
        self.assertEqual(result, 5500000)

        member = Members.objects.create(
            group_id=2,
            name="kamal",
            family="alavi"
        )
        Transaction.objects.create(
            Fund='500000', loan_p='5000000', payer_name='ali', members=member
        )
        result = get_sum_cash_desk_month()
        self.assertEqual(result, 11000000)

    def test_get_object_members(self):
        result = get_object_members(self.member.pk)
        self.assertEqual(result, self.member)

    def test_get_list_members_month(self):
        member = Members.objects.create(
            group_id=2,
            name="kamal",
            family="alavi"
        )
        Transaction.objects.create(
            Fund='500000', loan_p='5000000', payer_name='ali', members=member
        )
        result = get_list_members_month()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1], member)

    def test_get_choice_member_loan(self):
        PeriodLoan.objects.create(period_loan=1, members_id=self.member.pk)
        member = Members.objects.create(
            group_id=2,
            name="kamal",
            family="alavi"
        )
        PeriodLoan.objects.create(period_loan=2, members_id=member.pk)
        Transaction.objects.create(
            Fund='200000', loan_p='0', payer_name='ali', members=member
        )
        result = get_choice_member_loan()
        m1 = {'member': self.member, 'loan': 400000, 'sum_cash_desk_month': 3000000, 'wage_cash_desk': 800,
              'wage_cashier': 2000, 'sum_wage': 2800, 'payment': 397200, 'before_loan': 0, 'final_payment': 397200}
        m2 = {'member': member, 'loan': 400000, 'sum_cash_desk_month': 2600000, 'wage_cash_desk': 800,
              'wage_cashier': 2000, 'sum_wage': 2800, 'payment': 397200, 'before_loan': 0, 'final_payment': 397200}
        wage = {'sum_wage_member': 1600, 'sum_wage_cashier_member': 4000, 'end': 1, 'number_loan': 2,
                'sum_cash_desk_month': 2600000, 'get_sum_cash_desk_month': 3400000}
        self.assertEqual(len(result), 3)
        self.assertEqual(result['0'], m1)
        self.assertEqual(result['1'], m2)
        self.assertEqual(result['wage'], wage)
