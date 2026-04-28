from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404

from .models import Income, Expense, Todo, Loan, Category


# -----------------------------
# Home
# -----------------------------
def home(request):
    return render(request, 'xeon/base.html')


# -----------------------------
# Auth
# -----------------------------
def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'xeon/login.html')


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            password=request.POST.get('password'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name')
        )

        messages.success(request, "Account created successfully")
        return redirect('login_page')

    return render(request, 'xeon/register.html')


def logout_page(request):
    logout(request)
    return redirect('login_page')


# -----------------------------
# Dashboard
# -----------------------------
@login_required
def dashboard(request):
    user = request.user

    total_income = Income.objects.filter(user=user)\
        .aggregate(Sum('amount'))['amount__sum'] or 0

    total_expense = Expense.objects.filter(user=user)\
        .aggregate(Sum('amount'))['amount__sum'] or 0

    balance = total_income - total_expense

    # 🔥 ADD THIS (IMPORTANT)
    todos = Todo.objects.filter(user=user).order_by('-created_at')[:5]

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'todos': todos
    }

    return render(request, 'xeon/dashboard.html', context)

# -----------------------------
# Income
# -----------------------------
@login_required
def income_list(request):
    incomes = Income.objects.filter(user=request.user).order_by('-date')
    return render(request, 'xeon/income.html', {'incomes': incomes})


@login_required
def add_income(request):
    categories = Category.objects.filter(user=request.user, type='income')

    if request.method == "POST":
        Income.objects.create(
            user=request.user,
            amount=request.POST.get('amount') or 0,
            category_id=request.POST.get('category'),
            source=request.POST.get('source'),
            date=request.POST.get('date'),
        )
        return redirect('income_list')

    return render(request, 'xeon/add_income.html', {'categories': categories})

@login_required
def delete_income(request, id):
    if request.method == "POST":
        income = get_object_or_404(Income, id=id, user=request.user)
        income.delete()
    return redirect('income_list')

# -----------------------------
# Expense
# -----------------------------
@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')

    monthly_expenses = (
        expenses
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('-month')
    )

    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'xeon/expense.html', {
        'expenses': expenses,
        'monthly_expenses': monthly_expenses,
        'total_expense': total_expense
    })


@login_required
def add_expense(request):
    categories = Category.objects.filter(user=request.user, type='expense')

    if request.method == "POST":
        Expense.objects.create(
            user=request.user,
            amount=request.POST.get('amount') or 0,
            category_id=request.POST.get('category'),
            payment_method=request.POST.get('payment_method'),
            date=request.POST.get('date'),
        )
        return redirect('expense_list')

    return render(request, 'xeon/add_expense.html', {'categories': categories})


@login_required
def delete_expense(request, id):
    if request.method == "POST":
        expense = get_object_or_404(Expense, id=id, user=request.user)
        expense.delete()
    return redirect('expense_list')


# -----------------------------
# Todo
# -----------------------------
@login_required
def todo_list(request):
    todos = Todo.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'xeon/todo.html', {'todos': todos})


@login_required
def add_todo(request):
    if request.method == "POST":
        Todo.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            priority=request.POST.get('priority'),
            due_date=request.POST.get('due_date'),
        )
        return redirect('todo_list')

    return render(request, 'xeon/add_todo.html')


@login_required
def delete_todo(request, id):
    if request.method == "POST":    
        todo = get_object_or_404(Todo, id=id, user=request.user)
        todo.delete()
    return redirect('todo_list')


# -----------------------------
# Loan
# -----------------------------
@login_required
def loan_list(request):
    loans = Loan.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'xeon/loan.html', {'loans': loans})


@login_required
def add_loan(request):
    if request.method == "POST":
        Loan.objects.create(
            user=request.user,
            person_name=request.POST.get('person_name'),
            loan_type=request.POST.get('loan_type'),
            total_amount=request.POST.get('total_amount') or 0,
            paid_amount=request.POST.get('paid_amount') or 0,
            due_date=request.POST.get('due_date'),
            note=request.POST.get('note'),
        )
        return redirect('loan_list')

    return render(request, 'xeon/add_loan.html')


@login_required
def delete_loan(request, id):
    if request.method == "POST":
        loan = get_object_or_404(Loan, id=id, user=request.user)
        loan.delete()
    return redirect('loan_list')


@login_required
def delete_expense(request, id):
    if request.method == "POST":
        expense = get_object_or_404(Expense, id=id, user=request.user)
        expense.delete()
    return redirect('expense_list')


@login_required
def toggle_todo(request, id):
    todo = get_object_or_404(Todo, id=id, user=request.user)
    todo.is_completed = not todo.is_completed
    todo.save()
    return redirect('todo_list')

@login_required
def edit_income(request, id):
    income = get_object_or_404(Income, id=id, user=request.user)
    categories = Category.objects.filter(user=request.user, type='income')

    if request.method == "POST":
        income.amount = request.POST.get('amount')
        income.category_id = request.POST.get('category')
        income.source = request.POST.get('source')
        income.date = request.POST.get('date')
        income.note = request.POST.get('note')
        income.save()

        return redirect('income_list')

    return render(request, 'xeon/edit_income.html', {
        'income': income,
        'categories': categories
    })


@login_required
def add_category(request):
    next_url = request.GET.get('next')

    if request.method == "POST":
        Category.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            type=request.POST.get('type')
        )

        if next_url:
            return redirect(next_url)

        return redirect('add_category')

    return render(request, 'xeon/add_category.html')