from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.AccountCreateView.as_view(), name="account_create"),
    path('transaction/', views.transaction_create_view, name="transaction"),
    path('setting/', views.SettingCreateView.as_view(), name="setting"),
]
