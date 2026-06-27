from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Expense

@login_required(login_url='/login/')
def expenses(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = int(request.POST.get('price', 0))
        Expense.objects.create(name=name, price=price)
        return redirect('/')

    queryset = Expense.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(name__icontains=request.GET.get('search'))

    total_sum = sum(expense.price for expense in queryset)
    context = {'expenses': queryset, 'total_sum': total_sum}
    return render(request, 'expenses.html', context)

@login_required(login_url='/login/')
def update_expense(request, id):
    expense = Expense.objects.get(id=id)
    if request.method == 'POST':
        expense.name = request.POST.get('name')
        expense.price = int(request.POST.get('price', 0))
        expense.save()
        return redirect('/')
    return render(request, 'update_expense.html', {'expense': expense})

@login_required(login_url='/login/')
def delete_expense(request, id):
    Expense.objects.get(id=id).delete()
    return redirect('/')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username).first()
        if not user_obj:
            messages.error(request, "Username not found")
            return redirect('/login/')
        user_auth = authenticate(username=username, password=password)
        if user_auth:
            login(request, user_auth)
            return redirect('expenses')
        messages.error(request, "Wrong Password")
        return redirect('/login/')
    return render(request, "login.html")

def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is taken")
            return redirect('/register/')
        user_obj = User.objects.create(username=username)
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request, "Account created")
        return redirect('/login/')
    return render(request, "register.html")

def custom_logout(request):
    logout(request)
    return redirect('login')