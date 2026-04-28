from django.urls import path
from .views import *

urlpatterns = [

    path('login/', login_page, name='login_page'),
    path('register/', register_page, name='register'),
    path('logout/', logout_page, name='logout'),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),  # IMPORTANT
    path('income/', income_list, name='income_list'),
    path('expense/', expense_list, name='expense_list'),
    path('todo/', todo_list, name='todo_list'),
    path('income/add/', add_income, name='add_income'),
    path('expense/add/', add_expense, name='add_expense'),
    path('todo/add/', add_todo, name='add_todo'),
    path('loan/', loan_list, name='loan_list'),
    path('loan/add/', add_loan, name='add_loan'),
    path('category/add/', add_category, name='add_category'),
    path('loan/delete/<int:id>/', delete_loan, name='delete_loan'),
    path('expense/delete/<int:id>/', delete_expense, name='delete_expense'),
    path('income/delete/<int:id>/', delete_income, name='delete_income'),
    path('income/edit/<int:id>/', edit_income, name='edit_income'),
]