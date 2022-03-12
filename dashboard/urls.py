from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.AccountCreateView.as_view(), name="account_create"),
    path('trans', views.transaction, name="transaction")
]