from django.contrib import admin
from .models import Category, Income, Expense, Loan, Todo


# -----------------------------
# Category Admin
# -----------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'user']
    list_filter = ['type']
    search_fields = ['name']


# -----------------------------
# Income Admin
# -----------------------------
@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'category', 'date']
    list_filter = ['date', 'category']
    search_fields = ['source']


# -----------------------------
# Expense Admin
# -----------------------------
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'category', 'payment_method', 'date']
    list_filter = ['payment_method', 'date']
    search_fields = ['note']


# -----------------------------
# Loan Admin
# -----------------------------
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['id', 'person_name', 'loan_type', 'total_amount', 'paid_amount', 'status']
    list_filter = ['loan_type', 'status']
    search_fields = ['person_name']


# -----------------------------
# Todo Admin
# -----------------------------
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'priority', 'is_completed', 'due_date']
    list_filter = ['priority', 'is_completed']
    search_fields = ['title']