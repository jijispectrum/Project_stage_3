from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import ProductForm
from .models import Product, UserProfile
from .models import Product, UserProfile, CartItem
from django.contrib.auth.decorators import login_required
def members(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        mobile = request.POST['mobile']
        location = request.POST['location']
        
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error_message': 'Username already exists.'})
        
        user = User.objects.create_user(username=username, password=password, email=email)
        
        # Create UserProfile object and set additional fields
        profile = UserProfile.objects.create(user=user, mobile=mobile, location=location)
        
        login(request, user)
        return redirect('login')
       
    return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('members')  # Replace 'home' with your desired redirect URL
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password.'})
    return render(request, 'login.html')

def product(request):
    return render(request, 'product.html')

def upload_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=form.instance.pk)
    else:
        form = ProductForm()
    return render(request, 'upload_product.html', {'form': form})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})


@login_required
def cart(request):
    cart_items = CartItem.objects.all()
    cart_total = sum(item.total() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_total': cart_total})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()
    return redirect('cart')


from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect('members')  # Replace 'home' with the name of the view or URL pattern for your home page

