from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
   
    path('', views.home,name='home'),
    path('contact',views.contact, name='contact'),
    path('titan',views.titan, name='titan'),
    path('timex',views.timex, name='timex'),
    path('noice',views.noice, name='noice'),
    path('navy',views.navy, name='navy'),


     path('changepassword',views.changepassword, name="changepassword"),


    path('registration/',views.registration,name='registration'),
    path('login/',views.log_in,name='login'),

    path('logout/',views.log_out, name="logout"),


    

    path('profile/',views.profile,name='profile'),

    path('titancategories/',views.TitanCategoriesView.as_view(),name='titancategories'),
    path('timexcategories/',views.TimexCategoriesView.as_view(),name='timexcategories'),
    path('navycategories/',views.NavyforceCategoriesView.as_view(),name='navycategories'),

    path('noisecategories/',views.NoiseCategoriesView.as_view(),name='noisecategories'),

    path('watch_details/<int:id>/',views.WatchDetailView.as_view(),name='watchdetails'),

    
    path('addcart/<int:id>/',views.add_to_cart, name="addtocart"),
    path('view_cart/',views.view_cart, name="viewcart"),

    path('add_quantity/<int:id>/', views.add_quantity, name='add_quantity'),
    path('delete_quantity/<int:id>/', views.delete_quantity, name='delete_quantity'),
    path('delete_cart/<int:id>',views.delete_cart, name="deletecart"),

    path('address/',views.address,name='address'),
    path('delete_address/<int:id>',views.delete_address,name='deleteaddress'),

    
    path('checkout/',views.checkout,name='checkout'),


    path('payment/',views.payment,name='payment'),
    path('payment_success/<int:selected_address_id>/',views.payment_success,name='paymentsuccess'),
    path('payment_failed/',views.payment_failed,name='paymentfailed'),

    
    path('order/',views.order,name='order'),

    path('buynow/<int:id>',views.buynow,name='buynow'),

    path('buynow_payment/<int:id>',views.buynow_payment,name='buynowpayment'),

    path('buynow_payment_success/<int:selected_address_id>/<int:id>',views.buynow_payment_success,name='buynowpaymentsuccess'),




    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)