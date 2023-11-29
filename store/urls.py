from django.urls import path
from .import views

urlpatterns=[
    # views
    # path('', views.homepage, name='home'),
    path('product/', views.product, name='product'),
    path('details/', views.details, name='details'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.vblog, name='blog'),
    path('blogdetails/', views.blogdetails, name='blogdetails'),
    path('searchproduct/', views.searchproduct, name='searchproduct'),
    path('add-to-cart/', views.AddtoCart, name='add_to_cart'),
    path('delete-from-cart/', views.deletefromcart, name='delete-from-cart'),
    path('update-cart/',views.update_cart_item,name='update-cart'),
    path('ship/',views.ship,name='ship'),
    path('shipdel/',views.shipdel,name='shipdel'),
    path('error_page_500/',views.errorpage_500,name='errorpage_500'),
    path('error_page_404/',views.errorpage_404,name='errorpage_404'),
    path('paymentsuccesss/',views.paymentsuccesss,name='paymentsuccesss'),
    path('searchImage/', views.searchImage, name='searchImage'),


 
    path('',views.index,name='index'),
    
    
    # action
    path('productcate/<int:pk>', views.productcate, name='productcate'),
    path('details/<int:pk>', views.details, name='details'),
    path('details/<int:pk>', views.imgs, name='details'),
    path('blogdetails/<int:pk>', views.blogdetails, name='blogdetails'),
    path('shipdel/<int:pk>', views.shipdel, name='shipdel'),



    
]