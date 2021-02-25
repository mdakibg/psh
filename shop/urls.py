from django.urls import path, include
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('products/product/<int:id>/', views.singleproductview, name='single_product'),
    path('products/category/<str:category>/<str:price_sort>/', views.productsview, name='products'),
    path('enquiry/', views.enquiry, name='enquiry'),

    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/clear/', views.cart_clear, name='cart_clear'),
]