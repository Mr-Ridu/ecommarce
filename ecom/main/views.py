from django.shortcuts import render, redirect
from .models import ProductDetails,cartProductitems, PurchesDetails
from django.core.cache import cache
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PurchesDetailsForms, ProductDetailsforms
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotAllowed
from django.core.mail import send_mail
from django.core.mail import send_mail, BadHeaderError

# Create your views here.

def home(request):
    a = ProductDetails.objects.all().order_by('-id')
    return render(request,'home.html',{'al':a})


def addtocart(request, id):
    carts = ProductDetails.objects.get(id=id)
    if cartProductitems.objects.filter(ProductID=id,username=request.user).exists():
        messages.warning(request,'Item already exists in your cart.')
        return redirect('/')
    elif not request.user.is_authenticated:
        messages.warning(request,'You Must Login first')
        return render(request,'parts/login.html')
    else:
        username = request.user
        CPname = carts.Pname
        CPpicture= carts.Ppicture
        ProductID = carts.id
        CPprice = carts.Pprice
        cartsdetails = cartProductitems(username=username,CPname=CPname,CPpicture=CPpicture,ProductID=ProductID,CPrice=CPprice)
        cartsdetails.save()
        messages.success(request,'item added to cardt!')
        return redirect('cart')


def cart(request):
    cartsproduct = cartProductitems.objects.filter(username=request.user)
    
    total_price = 0
    for c in cartsproduct:
        total_price += c.CPrice
    return render(request,'parts/cart.html',{'cartsproduct':cartsproduct,'total_price':total_price})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        users = authenticate(username=username,password=password)
        if users is not None:
            login(request,users)
            messages.success(request,f"Successfully Logged In as {request.user}")
            return redirect('/')
        else:
            messages.error(request,"Something went wrong")

    return render(request, 'parts/login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return redirect('/')

@login_required
def removecart(request,id):
    removecart = cartProductitems.objects.get(id=id)
    removecart.delete()
    messages.success(request,"Cart Item deleted")
    return redirect('cart')

def product_details(request,id):
    itemdetails= ProductDetails.objects.get(id=id)
    return render(request,'product_details.html',{'itemdetails':itemdetails})

def search(request):
    if request.method=='POST':
        query= request.POST['query']
        if query is not None:
            search_product_name = ProductDetails.objects.filter(Pname__icontains=query)
            search_Pro_caat = ProductDetails.objects.filter(Pcatg__icontains=query)
            search_mall_name = ProductDetails.objects.filter(Pmallname__icontains=query)
            context={
                'search_product_name':search_product_name,
                'search_Pro_caat':search_Pro_caat,
                'search_mall_name':search_mall_name
            }
            return render(request,'parts/search.html',context)
        else:
            messages.error(request,'Blank can\'t search')
            return redirect('/')

    messages.error(request,'Don\'t be selly hacker!!')
    return redirect('/')

def buy(request,id):
    buyProduct = ProductDetails.objects.get(id=id)
    mainproduct = ProductDetails.objects.get(id=id)
    if request.method == 'POST':
        form = PurchesDetailsForms(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity'] 
            if mainproduct.Pstock>=quantity:
                form.instance.product_code = mainproduct.product_code
                form.save()
                messages.success(request,'Order Placed!')
                return redirect('/')
            else:
                messages.error(request,'sorry! .Your demand is more then stock')
                return redirect('/')
        else:
            print(form.errors) 
    else:
        form = PurchesDetailsForms()
    return render(request,'purches.html',{'buyProduct':buyProduct,'form':form})





def userreg(request):
    if request.method == 'POST':
        username= request.POST['username']
        email= request.POST['email']
        password1= request.POST['password1']
        password2= request.POST['password2']
        if password1 != password2:
            messages.error(request,'Enter both password same')
            return render(request, 'parts/userreg.html')
        elif User.objects.filter(username=username).exists():
            messages.error(request,'This username already exist. Please choose another')
            return render(request, 'parts/userreg.html')  
        elif User.objects.filter(email=email).exists():
            messages.error(request,'This email already exist. Please choose another')
            return render(request, 'parts/userreg.html')  
        elif len(password1)<8:
            messages.error(request,'Password is too short. It must be contain 8 charecter')
            return render(request, 'parts/userreg.html')
        else:
            user =User.objects.create_user(username=username, password=password1,email=email)    
            user.save()
            try:
                send_welcome_email(request, "Welcome To NoiyaBazar", "Welcome to NoiyaBazar . Thanks for creating profile in NoiyaBazar",email)
                messages.success(request,'User Created')
                return redirect('/')
            except (BadHeaderError, Exception) as e:
                messages.error(request, f'Error sending email: {str(e)}')
               
                return redirect('/')
    return render(request, 'parts/userreg.html')




def vendorreg(request):
    if request.method == 'POST':
        username= request.POST['username']
        email= request.POST['email']
        password1= request.POST['password1']
        password2= request.POST['password2']
        if password1 != password2:
            messages.error(request,'Enter both password same')
            return render(request, 'parts/userreg.html')
        elif User.objects.filter(username=username).exists():
            messages.error(request,'This username already exist. Please choose another')
            return render(request, 'parts/userreg.html')  
        elif User.objects.filter(email=email).exists():
            messages.error(request,'This email already exist. Please choose another')
            return render(request, 'parts/userreg.html')  
        else:
            user =User.objects.create_user(username=username, password=password1,email=email,is_staff=True)    
            user.save()
            messages.success(request,'Vendor User Created')
            return redirect('/')
    return render(request, 'parts/vendorreg.html')


@login_required
def vendorprofile(request):
    if request.user.is_staff:
        vendors_product= ProductDetails.objects.filter(Pvendorname=request.user).order_by('-id') 
        msg = PurchesDetails.objects.filter(PPname=request.user,confirmation=False).order_by('-id')
        if request.method == 'POST':
            form = ProductDetailsforms(request.POST, request.FILES)
            if form.is_valid():
                new_product = form.save(commit=False)  # Create a new instance without saving
                new_product.generate_product_code()  # Generate the product code
                new_product.save()  # Save the instance with the generated product code
                messages.success(request, 'Product successfully added!')
                return redirect('vendorprofile')  # Redirect back to the vendor profile
            else:
                print(form.errors)
        else:
            form = ProductDetailsforms()
        return render(request, 'parts/vendorprofile.html', {'form': form, 'vendors_product': vendors_product,'msg':msg})
    else:
        return redirect('/')




def update_stock(request,product_id):
    if request.method == 'POST':
        try:
            new_stock= request.POST['stock']
            product = ProductDetails.objects.get(id=product_id)
            product.Pstock += int(new_stock)
            product.save()
            messages.success(request,'Stock Updated')
            return redirect('vendorprofile')
        except ValueError:
            messages.error(request, 'Enter a valid quantity')
            return redirect('vendorprofile')


def confirmpurches(request,product_id,quantity):
    product = ProductDetails.objects.get(id=product_id)
    unconfirmed_purches= PurchesDetails.objects.filter(PPid=product_id,confirmation=False)
    for purches_products in unconfirmed_purches:
        if quantity<=product.Pstock:
            product.Pstock -= quantity
            product.save() #for update quantity
            purches_products.confirmation = True
            purches_products.save() #for confirm order
            try:
                send_welcome_email(request, 'Order Confirmed', f"Sir We have confirmed your order. Your will get your product within 5-7 days. Your product code is {product.product_code}", purches_products.Pemail)
                messages.success(request, 'Confirmed and email sent to client')
            except (BadHeaderError, Exception) as e:
                messages.error(request, f'Error sending email: {str(e)}')
        else:
            messages.error(request,'sorry!')
            return redirect('/')
    return redirect('/')


def delProduct(request,product_id):
    product = ProductDetails.objects.get(id=product_id)
    product.delete()
    messages.success(request,'Deleted')
    return redirect('vendorprofile')





def send_welcome_email(request,subject,message,usermail):
    from_email = 'mr.ridu007@gmail.com'
    recipient_list = [usermail]
    send_mail(subject, message, from_email, recipient_list)
    messages.success(request,'email send')
    return redirect('vendorprofile')