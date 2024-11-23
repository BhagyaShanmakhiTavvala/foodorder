from django.shortcuts import render, get_object_or_404, redirect
from .models import FoodItem, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
def food_list(request):
    foods = FoodItem.objects.filter(available=True)
    return render(request, 'food_list.html', {'foods': foods})

def create_order(request):
    if request.method == 'POST':
        seat_number = request.POST['seat_number']
        order = Order.objects.create(seat_number=seat_number)

        for item_id, quantity in request.POST.items():
            if item_id.startswith('food_'):
                item = get_object_or_404(FoodItem, id=int(item_id[4:]))
                if quantity:
                    OrderItem.objects.create(order=order, food_item=item, quantity=int(quantity))
        return redirect('order_summary', order_id=order.id)
    foods = FoodItem.objects.filter(available=True)
    return render(request, 'create_order.html', {'foods' : foods})

def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_summary.html', {'order': order})

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('login')
    orders = Order.objects.all()
    food_items = FoodItem.objects.all()
    return render(request, 'dashboard.html', {'orders' : orders, 'food_items' : food_items})

@login_required
def order_details(request, order_id):
    if not request.user.is_staff:
        return redirect('login')
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_details.html', {'order': order})

@login_required
def update_order_status(request, order_id):
    if not request.user.is_staff:
        return redirect('login')
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        status = request.POST['status']
        order.status = status
        order.save()
        return redirect('order_details', order_id=order_id)
    return render(request, 'update_order_status.html', {'order': order})

@login_required
def delete_order(request, order_id):
    if not request.user.is_staff:
        return redirect('login')
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('admin_dashboard')
    return render(request, 'delete_order.html', {'order': order})

@login_required
def food_management(request):
    if not request.user.is_staff:
        return redirect('login')
    food_items = FoodItem.objects.all()
    return render(request, 'food_management.html', {'food_items': food_items})

@login_required
def add_food_item(request):
    if not request.user.is_staff:
        return redirect('login')
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        available = request.POST.get('available') == 'on'
        image = request.FILES.get('image')
        FoodItem.objects.create(name=name, description=description, price=price, available=available, image=image)
        return redirect('food_management')
    return render(request, 'add_food_item.html')

@login_required
def update_food_item(request, food_id):
    if not request.user.is_staff:
        return redirect('login')
    food_item = get_object_or_404(FoodItem, id=food_id)
    if request.method == 'POST':
        food_item.name = request.POST['name']
        food_item.description = request.POST['description']
        food_item.price = request.POST['price']
        food_item.available = request.POST.get('available') == 'on'
        if 'image' in request.FILES:
            food_item.image = request.FILES['image']
        food_item.save()
        return redirect('food_management')
    return render(request, 'update_food_item.html', {'food_item': food_item})

@login_required
def delete_food_item(request, food_id):
    if not request.user.is_staff:
        return redirect('login')
    food_item = get_object_or_404(FoodItem, id=food_id)
    if request.method == 'POST':
        food_item.delete()
        return redirect('food_management')
    return render(request, 'delete_food_item.html', {'food_item': food_item})


def register(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You are now able to log in.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please check the form for errors.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Login failed. Please check your credentials.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')
