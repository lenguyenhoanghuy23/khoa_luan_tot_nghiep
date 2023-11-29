
import email
from xml.dom.minidom import NamedNodeMap
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from .models import *
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import messages


import datetime

#keras
from keras.models import load_model
from django.views.generic import CreateView
from tensorflow.keras.models import load_model
from django.urls import reverse_lazy
from tensorflow.keras.preprocessing.image import load_img,img_to_array
import numpy as np
from django.core.files.storage import default_storage

# Create your views here.

#view store

def index(request):
    return render(request,'store/index.html')

def product(request):
    return render(request,'store/product.html')

def details(request):
    return render(request,'store/details.html')

def cart(request):
    return render(request,'store/cart.html')


def contact(request):
    return render(request,'store/contact.html')

def vblog(request):
    return render(request,'store/blog.html')

def blogdetails(request):
    return render(request,'store/blog-details.html')

def ship(request):
    return render(request,'store/lsorder.html')

# action store

def index(request):
    total_amt=0
    category = Category.objects.all()
    products = Products.objects.filter(status=True)
    is_feature = Products.objects.filter(status=True ,is_feature =True)[:8] # lấy ra sản phẩm bán chạy
    is_new =Products.objects.filter(status=True ,is_new =True)[:8] # lấy ra sản phẩm mới
    blogg =blog.objects.filter()[:4]
    if 'cartdata' in request.session:
        for p_id,item in request.session['cartdata'].items():
            total_amt+=int(item['qty'])*int(item['price'])
        context ={'category':category,'products':products ,'is_feature':is_feature ,'total_amt':total_amt,'is_new':is_new,'blogg':blogg}
        return render(request, 'store/index.html',context)
    else:
        context ={'category':category,'products':products ,'is_feature':is_feature ,'total_amt':total_amt,'blogg':blogg,'is_new':is_new}
        return render(request, 'store/index.html',context)

def product(request):
    total_amt=0
    # show  all category
    category = Category.objects.all()
    # show product by status
    products = Products.objects.filter(status=True)
    totalproducts = Products.objects.filter(status=True).count()
    if request.method =="POST":
        name =request.POST.get('name')
        print(name)
    # pagination
    paginator =Paginator(products,per_page=16) 
    pageNumber = request.GET.get('page')
    try:
        productspage = paginator.page(pageNumber)
    except PageNotAnInteger:
        productspage = paginator.page(1)
    except EmptyPage:
        productspage = paginator.page(paginator.num_pages)
    
   
    
    if 'cartdata' in request.session:
        for p_id,item in request.session['cartdata'].items():
            total_amt+=int(item['qty'])*int(item['price'])
        context ={'category':category,'products':products,'products':productspage,'totalproducts':totalproducts,'total_amt':total_amt}
        return render(request, 'store/product.html',context)
    else:
        context ={'category':category,'products':products,'products':productspage,'totalproducts':totalproducts,'total_amt':total_amt}
        return render(request, 'store/product.html',context)

def productcate(request,pk):
    category = Category.objects.all()
    procate = Products.objects.filter(category_id=pk)
    count = Products.objects.filter(category_id=pk).count()
    get_name = Category.objects.get(id= pk)
   
    paginator =Paginator(procate,per_page=16) 
    pageNumber = request.GET.get('page')
    try:
        productspage = paginator.page(pageNumber)
    except PageNotAnInteger:
        productspage = paginator.page(1)
    except EmptyPage:
        productspage = paginator.page(paginator.num_pages)
    

    total_amt=0
    if 'cartdata' in request.session:
        for p_id,item in request.session['cartdata'].items():
            total_amt+=int(item['qty'])*int(item['price'])
        context ={'category':category,'procate':procate ,'number_of_product':count,'get_name':get_name,'total_amt':total_amt,'procate':productspage}
        return render(request, 'store/ProductCate.html',context)
    else:
        context ={'category':category,'procate':procate ,'number_of_product':count,'get_name':get_name,'total_amt':total_amt,'procate':productspage}
        return render(request, 'store/ProductCate.html',context)



def details(request,pk):
    category = Category.objects.all() # lấy tên danh mục
    prodel = Products.objects.filter(pk = pk) # lấy sản phẩm của danh mục
    products = Products.objects.get(id=pk )
    images =DProducts.objects.filter(products =pk)
    related_product =Products.objects.filter(category=products.category).exclude(id=pk)[:4]
    
    total_amt=0
    if 'cartdata' in request.session:
        for p_id,item in request.session['cartdata'].items():
            total_amt+=int(item['qty'])*int(item['price'])
        context= {'prodel':prodel,'category':category ,'related_product': related_product,'images':images ,'total_amt':total_amt}
        return render(request, 'store/details.html',context)
    else:
        context= {'prodel':prodel,'category':category ,'related_product': related_product,'images':images ,'total_amt':total_amt}
        return render(request, 'store/details.html',context)
    



def imgs(request,pk):
    pass

def searchproduct(request):
    category = Category.objects.all()
    
    if request.method =='GET':
        query =request.GET.get('query')
        if query:
            products =Products.objects.filter(nameProduct__icontains=query)
            paginator =Paginator(products,per_page=8) 
            pageNumber = request.GET.get('page')
            try:
                productspage = paginator.page(pageNumber)
            except PageNotAnInteger:
                productspage = paginator.page(1)
            except EmptyPage:
                productspage = paginator.page(paginator.num_pages)
            qty =Products.objects.filter(nameProduct__icontains=query).count()

            context={'category':category,'products':products ,'qty':qty,'products':productspage}

            return render(request,'store/search.html',context)
        else:
            print('không có sản phẩm này')
            return render(request,'store/search.html')
   


def AddtoCart(request):
    # del request.session['cartdata']
    cart_p={}
    cart_p[str(request.GET['id'])]={
		'image':request.GET['image'],
		'name':request.GET['name'],
		'qty':request.GET['qty'],
		'price':request.GET['price'],
	}
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data=request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty']=int(cart_p[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartdata']=cart_data
            messages.info(request, 'sản phẩm đã tồn tại trong giỏ hàng')
        else: 
            cart_data=request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata']=cart_data
            messages.info(request, 'sản phẩm đã thêm trong giỏ hàng')
           
        
    else:
        request.session['cartdata']=cart_p
        
    
   
    
    return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})
        

def cart(request):
    total_amt=0
    if 'cartdata' in request.session:
        for p_id,item in request.session['cartdata'].items():
            total_amt+=int(item['qty'])*int(item['price'])
           
        return render(request, 'store/cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
    else:
        return render(request, 'store/cart.html',{'cart_data':'','totalitems':0,'total_amt':total_amt})

def deletefromcart(request):
    p_id=str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data=request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata']=cart_data
    total_amt=0
    for p_id,item in request.session['cartdata'].items():
        total_amt+=int(item['qty'])*int(item['price'])
    t=render_to_string('store/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
    return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})


def update_cart_item(request):
	p_id=str(request.GET['id'])
	p_qty=request.GET['qty']
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[str(request.GET['id'])]['qty']=p_qty
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*int(item['price'])
	t=render_to_string('store/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

@login_required
def checkout(request):
    total_amt=0
    totalAmt=0

    total=0

    lastname =request.POST.get('lastname')
    addressform =request.POST.get('address')
    Phoneform =request.POST.get('phone')
    emailform =request.POST.get('email')
    descriptionform =request.POST.get('description')
    cart = request.session.get("cartdata")
    uid = request.session.get('_auth_user_id')
    user =User.objects.get(id=uid)
    now = datetime.datetime.now()

    print(lastname,addressform,Phoneform,emailform,descriptionform)

    print("time",now)


    if 'cartdata' in request.session:
        for p_id,item in request.session['cartdata'].items():
            totalAmt+=int(item['qty'])*int(item['price'])
           
        # Order
        for p_id,item in request.session['cartdata'].items():
            total_amt+=int(item['qty'])*int(item['price'])
            
        for i in cart:
            a = int(cart[i]['price'])
            b =int(cart[i]['qty'])
            
            total = a*b

            print(total)

        
    
            # OrderItems
            if request.method =="POST":
                # Order
                order=CartOrder(
                    user=user,
                    total_amt=totalAmt,
                    # order_dt=now
                )

                order.save()
                #CartOrderItems
                


                cartOrderItems =CartOrderItems(
                    order =order ,
                    invoice_no='INV-'+str(order.id),
                    item =cart[i]['name'],
                    image=cart[i]['image'],
                    qty=cart[i]['qty'],
                    price=cart[i]['price'],
                    total=total,
                )

                cartOrderItems.save()

                #ShippingAddress
                shipping =ShippingAddress(
                    order =order,
                    
                    address=addressform,
                    lastname=lastname,
                    phone=Phoneform,
                    des=descriptionform,
                    email=emailform,
                    
                    )
                shipping.save()
                
                return redirect("paymentsuccesss")
            # End
        # Process Payment
    
        return render(request, 'store/checkout.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt,'total':total})
        
    else:
        return render(request, 'store/checkout.html',{'cart_data':'','totalitems':0,'total_amt':totalAmt,'total':total})


        

def paymentsuccesss(request):
    if 'cartdata' in request.session:
        del request.session["cartdata"]
        return render(request,'store/payment-success.html')
    else:
        return render(request,'store/payment-fail.html')

    

def ship(request):
    if request.user.is_authenticated:
        user = request.user
        cartorder = CartOrder.objects.filter(user=user,complete=False)
        
        ship =ShippingAddress.objects.filter(order=cartorder)

        

        context ={'ship':ship,'cartorder':cartorder}
    return render(request,'store/lsorder.html',context)

def shipdel(request,pk):

    cartorder = CartOrder.objects.filter(id=pk).delete()
    return redirect('ship') 
   


def vblog(request):
    blogg =blog.objects.filter()
    paginator =Paginator(blogg,per_page=10) 
    pageNumber = request.GET.get('page')
    
    try:
        productspage = paginator.page(pageNumber)
    except PageNotAnInteger:
        productspage = paginator.page(1)
    except EmptyPage:
        productspage = paginator.page(paginator.num_pages)
    context ={'blogg':blogg ,'blogg':productspage}
    return render(request,'store/blog.html',context)

def contact(request):
    if request.method=="POST":
        nameform =request.POST.get('name')
        eamilform = request.POST.get("email")
        messform = request.POST.get("mess")
        

        ct = Contact(
            name=nameform,
            email=eamilform,
            message=messform

        )
        ct.save()

    return render(request,'store/contact.html')

def errorpage_404(request,exception):
    return render(request,'page_error/error.html')

def errorpage_500(request):
    return render(request,'page_error/error.html')

def blogdetails(request,pk):
    category = Category.objects.all()
    
    vblog = blog.objects.filter(pk =pk)
    rblog = blog.objects.get(id=pk )
    # related_product =Products.objects.filter(category=rblog.cateblog).exclude(id=pk)[:4]
    print(rblog.cateblog.id)
    related_product =blog.objects.filter(cateblog=rblog.cateblog).exclude(id=pk)[:4]
    print(related_product)
    context ={'vblog':vblog,'category':category ,'related_product':related_product}
    return render(request,'store/blog-details.html',context)

def searchImage(request):
    if request.method == "POST":
        searchImage = request.FILES['imageFile']
        file_name = default_storage.save(searchImage.name, searchImage)
        file_url = default_storage.path(file_name)
        reverse_mapping = {0: '00000', 1: 'anh đào', 2: 'bưởi đoan hùng', 3: 'chôm chôm', 4: 'dưa hấu bình sơn',
                           5: 'đào sapa',
                           6: 'Hồng xiêm', 7: 'khoai lang mật', 8: 'lựu', 9: 'mãn cầu bà đen', 10: 'măn cụt',
                           11: 'mận hậu', 12: 'nhãn lồng', 13: 'nho ninh thuận', 14: 'qủa mơ',
                           15: 'qủa thanh mai',
                           16: 'sầu riêng', 17: 'thanh long quảng trị', 18: 'trà trái cây', 19: 'trái bơ',
                           20: 'vải thanh hà', 21: 'xoài tượng'}
        
    
        def mapper(value):
            return reverse_mapping[value]

        model = load_model('store/static/weights-50-1.00.hdf5')
        image = load_img(file_url, target_size=(128,128))

        image = img_to_array(image)
        image = image / 255.1
        prediction_image = np.array(image)
        prediction_image = np.expand_dims(image, axis=0)

        prediction = model.predict(prediction_image)
        value = np.argmax(prediction)
        print(value)
        move_name = mapper(value)
        print("ảnh: {}.".format(move_name))
        searchImage1 = Products.objects.filter(nameProduct__icontains= move_name)
        print('searchImage',searchImage1)
        return render(request, "store/searchImage.html",{'searchImage':searchImage,'searchImage1': searchImage1})
    else:
        return render(request, "store/searchImage.html")

    #return render(request,"store/searchImage.html")
