from django.db import models
from django.urls import reverse

STATUS_TRANSACTION = (
    ('receive_money', 'دریافت وجه'),
    ('loan_repayment', 'پرداخت وام'),
)


class Members(models.Model):
    group_id = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=120)
    family = models.CharField(max_length=120)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.family}"

    def get_absolute_url(self):
        return reverse('account_create')

    class Meta:
        unique_together = [['name', 'family']]


class PeriodLoan(models.Model):
    period_loan = models.PositiveSmallIntegerField(unique=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    members = models.OneToOneField(Members, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.period_loan} {self.members}"


class Loan(models.Model):
    last_loan = models.BooleanField(default=False)
    receive_loan = models.PositiveSmallIntegerField()
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    members = models.OneToOneField(Members, on_delete=models.CASCADE)
    period_loan = models.OneToOneField(PeriodLoan, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.receive_loan}"


class ListPaymentCard(models.Model):
    card_bank = models.IntegerField()
    payment_card = models.ForeignKey(Members, on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.card_bank)


class Transaction(models.Model):
    Fund = models.CharField(max_length=120, default=200000)
    loan_p = models.CharField(max_length=120)
    payer_name = models.CharField(max_length=120)
    status_transaction = models.CharField(max_length=15,
                                          choices=STATUS_TRANSACTION,
                                          default="receive_money")
    # members = models.OneToOneField(Members, on_delete=models.CASCADE)
    members = models.ForeignKey('Members', on_delete=models.CASCADE)  # dashboard
    # TODO: open_account remove
    open_account = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('transaction')

    def __str__(self):
        return f"{self.members.name} {self.members.family}"


class Cash(models.Model):
    money_next_month = models.PositiveSmallIntegerField()
    wage = models.PositiveSmallIntegerField()
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)


class Setting(models.Model):
    loan_ratio = models.FloatField(default=2)
    number_months_loan_repayment = models.PositiveSmallIntegerField(default=20)
    minimum_share = models.PositiveSmallIntegerField(default=200000)
    maximum_loan = models.PositiveSmallIntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('setting')
