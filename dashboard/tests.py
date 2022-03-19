import time

from django.test import TestCase
from django.urls import reverse

from .forms import AccountCreateForm
from .models import Members, Transaction
from .views import qs_trans_merge_members_transaction_create_view


class DashboardTest(TestCase):
    def setUp(self):
        self.member = Members.objects.create(
            group_id=1,
            name="ali",
            family="alavi"
        )

    def test_member_duplicate(self):
        form_data = {'group_id': 2, 'name': 'ali', 'family': 'alavi'}
        form = AccountCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

    def test_create_models_transaction(self):
        member = Members.objects.get(id=int(self.member.id))
        transaction = Transaction.objects.create(
            Fund='20000', loan_p='3000000', payer_name='ali', members=member
        )
        self.assertEqual(transaction.Fund, '20000')
        self.assertEqual(transaction.loan_p, '3000000')
        self.assertEqual(transaction.payer_name, 'ali')
        self.assertEqual(transaction.members, member)

    def test_create_view_transaction(self):
        data = {'fund': '20000', 'loan_p': '3000000', 'payer_name': 'ali', 'pk': self.member.id}
        response = self.client.post(reverse("transaction"), data=data, )

        trans = Transaction.objects.last()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(trans.Fund, "20000")
        self.assertEqual(trans.loan_p, "3000000")
        self.assertEqual(trans.payer_name, "ali")
        self.assertEqual(trans.pk, self.member.id)

    def test_qs_trans_merge_members_transaction_create_view(self):
        member = Members.objects.get(id=int(self.member.id))
        Transaction.objects.create(
            Fund='20000', loan_p='3000000', payer_name='ali', members=member
        )
        time.sleep(1)
        Transaction.objects.create(
            Fund='30000', loan_p='4000000', payer_name='ali', members=member
        )
        list = qs_trans_merge_members_transaction_create_view()
        self.assertEqual(list[0]['member'], member)
        self.assertEqual(list[0]['trans']['Fund'], '30000')
        self.assertEqual(list[0]['trans']['loan_p'], '4000000')
