from django.test import TestCase

from .forms import AccountCreateForm
from .models import Members


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
