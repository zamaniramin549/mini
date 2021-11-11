from django.urls import path
from miniapp import views
urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('loginuser/', views.loginuser, name='loginuser'),
    path('register/', views.register, name='register'),
    path('product_detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('viewcart/', views.viewcart, name='viewcart'),
    path('add_more/<int:pk>/', views.add_more, name='add_more'),
    path('reduce/<int:pk>/', views.reduce, name='reduce'),
    path('remove/<int:pk>/', views.remove, name='remove'),
    path('viewproducts_user/<int:pk>/', views.viewproducts_user, name='viewproducts_user'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('payment/', views.payment, name='payment'),
    path('phistory/', views.phistory, name='phistory'),
    path('logoutuser/', views.logoutuser, name='logoutuser'),
    path('Q&A/', views.qa, name='Q&A'),
    path('returnspolicy/', views.returnspolicy, name='returnspolicy'),
    path('shippingpolicy/', views.shippingpolicy, name='shippingpolicy'),
    path('termscondition/', views.termscondition, name='termscondition'),
    path('Contact/', views.contact, name='contact'),
]