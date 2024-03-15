from django.shortcuts import render,redirect,get_object_or_404
from django.views import View

from . models import Customer,Watch,Order,Cart
from .forms import SignupForm

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm

from . forms import RegistrationForm,AuthenticateForm,ChangePasswordForm,UserProfileForm,AdminProfileForm,CustomerForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash



#===============For Paypal =========================
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
#=========================================================


# Create your views here.

def home(request):
    return render(request,'home.html')

def contact(request):
    return render(request,'contact.html')

def titan(request):
    return render(request,'titan.html')

def timex(request):
    return render(request,'timex.html')

def noice(request):
    return render(request,'noice.html')

def navy(request):
    return render(request,'navy.html')

# def log_in(request):
#     return render(request,'login.html')

# def profile(request):
#     return render(request,'profile.html')



#==========registration=================
    
def registration(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            mf = RegistrationForm(request.POST)
            if mf.is_valid():
                mf.save()
                return redirect('login')    
        else:
            mf  = RegistrationForm()
        return render(request,'registration.html',{'mf':mf})
    else:
        return redirect('profile')

# ======================login===================
def log_in(request):
    if not request.user.is_authenticated:  # check whether user is not login ,if so it will show login option
        if request.method == 'POST':       # otherwise it will redirect to the profile page 
            mf = AuthenticationForm(request,request.POST)
            if mf.is_valid():
                name = mf.cleaned_data['username']
                pas = mf.cleaned_data['password']
                user = authenticate(username=name, password=pas)
                if user is not None:
                    login(request, user)
                    return redirect('home')
        else:
            mf = AuthenticationForm()
        return render(request,'login.html',{'mf':mf})
    else:
        return redirect('/profile/')
# #=================profile==================
def profile(request):
    if request.user.is_authenticated:  # This check wheter user is login, if not it will redirect to login page
        return render(request,'profile.html',{'name':request.user})
    else:                                                # request.user returns the username
        return redirect('/login/')



#==================logout======================
def log_out(request):
    logout(request)
    return redirect('/login/')

#=============change password================

def changepassword(request):                                       # Password Change Form               
    if request.user.is_authenticated:                              # Include old password 
        if request.method == 'POST':                               
            mf =ChangePasswordForm(request.user,request.POST)
            if mf.is_valid():
                mf.save()
                update_session_auth_hash(request,mf.user)
                return redirect('profile')
        else:
            mf = ChangePasswordForm(request.user)
        return render(request,'changepassword.html',{'mf':mf})
    else:
        return redirect('login')
    
#=============class based function=========================

class TitanCategoriesView(View):
    def get(self,request):
        watch_category = Watch.objects.filter(category='TITAN')  # we are using filter function of queryset, that will filter those data whose category belongs to dog
        return render(request,'titancategories.html',{'titan_category':watch_category})

class TimexCategoriesView(View):
    def get(self,request):
        watch_category = Watch.objects.filter(category='TIMEX')  # we are using filter function of queryset, that will filter those data whose category belongs to dog
        return render(request,'timexcategories.html',{'titan_category':watch_category})

class NavyforceCategoriesView(View):
    def get(self,request):
        watch_category = Watch.objects.filter(category='NAVYFORCE')  # we are using filter function of queryset, that will filter those data whose category belongs to dog
        return render(request,'navycategories.html',{'titan_category':watch_category})



class NoiseCategoriesView(View):
    def get(self,request):
        watch_category = Watch.objects.filter(category='NOISE')  # we are using filter function of queryset, that will filter those data whose category belongs to dog
        return render(request,'noisecategories.html',{'noise_category':watch_category})


class WatchDetailView(View):
    def get(self,request,id):     # id = It will fetch id of particular watch 
        watch = Watch.objects.get(pk=id)

        #------ code for caculate percentage -----
        if watch.discounted_price !=0:    # fetch discount price of particular watch
            percentage = int(((watch.selling_price-watch.discounted_price)/watch.selling_price)*100)
        else:
            percentage = 0
        # ------ code end for caculate percentage ---------
            
        return render(request,'watch_details.html',{'watch':watch,'percentage':percentage})





#========add to cart==========================
def add_to_cart(request, id):    # This 'id' is coming from 'watch.id' which hold the id of current watch , which is passing through {% url 'addtocart' watch.id %} from watch_detail.html 
    if request.user.is_authenticated:
        product = Watch.objects.get(pk=id) # product variable is holding data of current object which is passed through 'id' from parameter
        user=request.user                # user variable store the current user i.e steveroger
        Cart(user=user,product=product).save()  # In cart model current user i.e steveroger will save in user variable and current watch object will be save in product variable
        return redirect('watchdetails', id)       # finally it will redirect to watch_details.html with current object 'id' to display watch after adding to the cart
    else:
        return redirect('login')    


#================view cart================================
    
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)      # cart_items will fetch product of current user, and show product available in the cart of the current user.
    total =0
    delevery_charge =150
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.selling_price * item.quantity
        total += item.product.price_and_quantity_total
    final_price= delevery_charge + total
    return render(request, 'view_cart.html', {'cart_items': cart_items,'total':total,'final_price':final_price})


#===========quantity manage=======================

def add_quantity(request, id):
    product = get_object_or_404(Cart, pk=id)    # If the object is found, it returns the object. If not, it raises an HTTP 404 exception (Http404).
    product.quantity += 1                       # If object found it will be add 1 quantity to the current object   
    product.save()
    return redirect('viewcart')

def delete_quantity(request, id):
    product = get_object_or_404(Cart, pk=id)
    if product.quantity > 1:
        product.quantity -= 1
        product.save() 
    return redirect('viewcart')

def delete_cart(request,id):
    if request.method == 'POST':
        de = Cart.objects.get(pk=id)
        de.delete()
    return redirect('viewcart')




def address(request):
    if request.method == 'POST':
            print(request.user)
            mf =CustomerForm(request.POST)
            print('mf',mf)
            if mf.is_valid():
                user=request.user                # user variable store the current user i.e steveroger
                name= mf.cleaned_data['name']
                address= mf.cleaned_data['address']
                city= mf.cleaned_data['city']
                state= mf.cleaned_data['state']
                pincode= mf.cleaned_data['pincode']
                print(state)
                print(city)
                print(name)
                Customer(user=user,name=name,address=address,city=city,state=state,pincode=pincode).save()
                return redirect('address')           
    else:
        mf =CustomerForm()
        address = Customer.objects.filter(user=request.user)
    return render(request,'address.html',{'mf':mf,'address':address})


def delete_address(request,id):
    if request.method == 'POST':
        de = Customer.objects.get(pk=id)
        de.delete()
    return redirect('address')

#==========checkout==============
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)      # cart_items will fetch product of current user, and show product available in the cart of the current user.
    total =0
    delevery_charge =150
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
    final_price= delevery_charge + total
    
    address = Customer.objects.filter(user=request.user)

    return render(request, 'checkout.html', {'cart_items': cart_items,'total':total,'final_price':final_price,'address':address})


#=========payment=========================
def payment(request):

    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address')

    host = request.get_host()   # Will fecth the domain site is currently hosted on.

    cart_items = Cart.objects.filter(user=request.user)      # cart_items will fetch product of current user, and show product available in the cart of the current user.
    total =0
    delevery_charge =2000
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
    final_price= delevery_charge + total
    
    address = Customer.objects.filter(user=request.user)

#=============================== Paypal Code ===============================================
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': final_price,
        'item_name': 'Watch',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('paymentsuccess', args=[selected_address_id])}",
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

#==========================================================================================================
    return render(request, 'payment.html', {'cart_items': cart_items,'total':total,'final_price':final_price,'address':address,'paypal':paypal_payment})

#===================================== Payment Success ============================================

def payment_success(request,selected_address_id):
    print('payment sucess',selected_address_id)   # we have fetch this id from return_url': f"http://{host}{reverse('paymentsuccess', args=[selected_address_id])}
                                                  # This id contain address detail of particular customer
    user =request.user
    customer_data = Customer.objects.get(pk=selected_address_id,)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        Order(user=user,customer=customer_data,Watch=c.product,quantity=c.quantity).save()
        c.delete()
    return render(request,'payment_success.html')


#===================================== Payment Failed ============================================


def payment_failed(request):
    return render(request,'payment_failed.html')


#=========order=================

def order(request):
    ord=Order.objects.filter(user=request.user)
    return render(request,'order.html',{'ord':ord})


#========================================== Buy Now ========================================================
def buynow(request,id):
    watch = Watch.objects.get(pk=id)     # cart_items will fetch product of current user, and show product available in the cart of the current user.
    delhivery_charge =150
    final_price= delhivery_charge + watch.discounted_price
    
    address = Customer.objects.filter(user=request.user)

    return render(request, 'buynow.html', {'final_price':final_price,'address':address,'watch':watch})


def buynow_payment(request,id):

    if request.method == 'POST':
        selected_address_id = request.POST.get('buynow_selected_address')

    watch = Watch.objects.get(pk=id)     # cart_items will fetch product of current user, and show product available in the cart of the current user.
    delhivery_charge =150
    final_price= delhivery_charge + watch.discounted_price
    
    address = Customer.objects.filter(user=request.user)
    #================= Paypal Code ======================================

    host = request.get_host()   # Will fecth the domain site is currently hosted on.

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': final_price,
        'item_name': 'watch',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('buynowpaymentsuccess', args=[selected_address_id,id])}",
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    #========================================================================

    return render(request, 'payment.html', {'final_price':final_price,'address':address,'watch':watch,'paypal':paypal_payment})

def buynow_payment_success(request,selected_address_id,id):
    print('payment sucess',selected_address_id)   # we have fetch this id from return_url': f"http://{host}{reverse('paymentsuccess', args=[selected_address_id])}
                                                  # This id contain address detail of particular customer
    user =request.user
    customer_data = Customer.objects.get(pk=selected_address_id,)
    
    watch = watch.objects.get(pk=id)
    Order(user=user,customer=customer_data,watch=watch,quantity=1).save()
   
    return render(request,'buynow_payment_success.html')