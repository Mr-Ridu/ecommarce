
from django.contrib import admin
from django.urls import path, include
from. import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.home,name='home'),
    path('cart/' ,views.cart, name='cart'),
    path('addtocart/<int:id>' ,views.addtocart, name='addtocart'),
    path('login/' ,views.user_login, name='login'),
    path('logout/' ,views.user_logout, name='logout'),
    path('removecart/<int:id>/' ,views.removecart, name='removecart'),
    path('product_details/<int:id>/' ,views.product_details, name='product_details'),
    path('search/' ,views.search, name='search'),
    path('buy/<int:id>/' ,views.buy, name='buy'),
    path('userreg/' ,views.userreg, name='userreg'),
    path('vendorreg/' ,views.vendorreg, name='vendorreg'),
    path('vendorprofile/' ,views.vendorprofile, name='vendorprofile'),
    path('delProduct/<int:product_id>/', views.delProduct, name='delProduct'),
    path('confirmpurches/<int:product_id>/<int:quantity>/', views.confirmpurches, name='confirmpurches'),
    path('update_stock/<int:product_id>/', views.update_stock, name='update_stock'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
