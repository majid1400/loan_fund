from django.contrib import admin
from .models import Members, ListPaymentCard, Loan, PeriodLoan, Transaction, \
    Setting, Cash


class ListPaymentCardInLine(admin.TabularInline):
    model = ListPaymentCard


class MembersAdmin(admin.ModelAdmin):
    inlines = [ListPaymentCardInLine]


class LoanAdmin(admin.ModelAdmin):
    pass


class PeriodLoanAdmin(admin.ModelAdmin):
    pass


class TransactionAdmin(admin.ModelAdmin):
    pass


class SettingAdmin(admin.ModelAdmin):
    pass


class CashAdmin(admin.ModelAdmin):
    pass


admin.site.register(Members, MembersAdmin)
admin.site.register(Loan, LoanAdmin)
admin.site.register(PeriodLoan, PeriodLoanAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(Cash, CashAdmin)
