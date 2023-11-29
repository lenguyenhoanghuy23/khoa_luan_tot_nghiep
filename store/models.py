from typing import Text
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from datetime import datetime
from django.template.defaultfilters import truncatechars

from ckeditor.fields import RichTextField 
# Create your models here.
date_time = datetime.now() # current date and time




class Customer(models.Model):
    user =models.OneToOneField(User,verbose_name=("tài khoản"),null=False,blank=False, on_delete=models.CASCADE)
    phone_field = models.CharField(("số điện thoại"),max_length=15)

    def __str__(self) :
        return self.user.username
    
    class Meta:
        verbose_name_plural='01.khách hàng'

class Category(models.Model):
    Name =models.CharField(('tên danh mục'),max_length=100,null=False) 
    def __str__(self):
        return self.Name
    class Meta:
        verbose_name_plural='02.danh mục sản phẩm'

status_choice_unit=(
        ('kg','kg'),
        ('trái','trái'),
        ('giỏ','giỏ trái cây'),
     

    )



class Products(models.Model):
    nameProduct =models.CharField(('tên sản phẩm'),max_length=100,null=False)
    description =models.TextField(('mô tả'))
    img = models.ImageField(('ảnh sản phẩm'),upload_to='image/')
    price = models.IntegerField(('giá'),default=9999)
    status =models.BooleanField(('trạng thái'),default=True)
    slug = models.IntegerField(("số lượng"),default=9999)
    unit = models.CharField("đơn tính",choices=status_choice_unit ,default="kg" ,max_length=10)
    category =models.ForeignKey(Category,verbose_name=("danh mục"), on_delete=models.CASCADE)
    is_feature =models.BooleanField(("Sản phẩm nổi bật"), default=False )   
    is_new= models.BooleanField(("Sản phẩm mới"), default=False )   
    
    

    class Meta:
        verbose_name_plural='03.sản phẩm'
    
    def __str__(self):
        return self.nameProduct

    def img_tag(self):
        return mark_safe('<img src="%s" width="100"   />' % (self.img.url))

    @property
    def imageURL(self):
        try:
            url = self.img.url
        except:
            url = ''
        return url
    @property
    def short_description_product(self):
        return truncatechars(self.description, 100)

class DProducts(models.Model):
    products =models.ForeignKey(Products,verbose_name=("thuộc sản phẩm"), on_delete=models.CASCADE , null=True)
    imgs = models.ImageField(('chi tiết ảnh'),upload_to='image/details/') 
    
     
    def __str__(self):
        return str(self.products)
    
    def img_tag(self):
        return mark_safe('<img src="%s" width="100px"  height="70px"  />' % (self.imgs.url))

    class Meta:
        verbose_name_plural='04. chi tiết ảnh sản phẩm'

status_choice=(
        ('Confirmed','Đã được xác nhận '),
        ('sender ready','người gửi chuẩn bị hàng '),
        ('order has been delivered','đơn hàng đã được bàn giao cho đơn vị vận chuyển'),
        ('shipping',' đang giao hàng'),
        ('delivered','đã giao hàng'),

    )


class CartOrder(models.Model):
    user=models.ForeignKey(User,verbose_name=("thuộc tài khoản "),on_delete=models.CASCADE)
    total_amt=models.IntegerField(("tổng tiền"))
    paid_status=models.BooleanField(("trạng thái thanh toán"),default=False)
    order_dt=models.DateTimeField(("ngày đặt hàng"),auto_now_add=True)
    order_status=models.CharField(("tình trạng đơn hàng"),choices=status_choice,default='Confirmed',max_length=150)
    complete =models.BooleanField("hoàn thành" ,default=False)
    class Meta:
        verbose_name_plural='05.Đơn Hàng'
    def __str__(self):
        return str(self.user)

  

# OrderItems
class CartOrderItems(models.Model):
    order=models.ForeignKey(CartOrder,verbose_name=("đơn hàng"), on_delete=models.CASCADE)
    invoice_no=models.CharField(("mã hóa đơn"),max_length=150)
    item=models.CharField(("tên sản phẩm"),max_length=150)
    image=models.CharField(("ảnh sản phẩm"),max_length=200)
    qty=models.IntegerField(("số lượng"))
    price=models.IntegerField(("giá"))
    total=models.IntegerField(("tổng tiền"))

    class Meta:
        verbose_name_plural='06.Chi Tiết Đơn Đặt Hàng'

    def __str__(self):
        return self.item

    def img_tag(self):
        return mark_safe('<img src="%s" width="100px"  height="70px"  />' % (self.image))



class ShippingAddress(models.Model):
    order = models.ForeignKey(CartOrder,verbose_name=("địa chỉ thuộc tài khoản") ,on_delete=models.CASCADE)
    address = models.CharField(("địa chỉ"),max_length=200, null=False)
    lastname = models.CharField(("tên người nhận"),max_length=200, null=False)
    phone = models.CharField(("số điện thoại"),max_length=200, null=False)
    des = models.CharField(("mô tả"),max_length=200, null=False)
    email = models.CharField(("email"),max_length=200, null=False)
    date_added = models.DateTimeField(("thời gian đặt"),auto_now_add=True)
	
    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name_plural='07.địa chỉ giao hàng'

class categoryblog(models.Model):
    name=models.CharField(("tên chủ đề"),max_length=150) 

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural='08.chủ đề bài viết'

class blog(models.Model):
    cateblog = models.ForeignKey(categoryblog,verbose_name=("thuộc chủ đề") ,on_delete=models.CASCADE)
    name=models.CharField(("tên bài viết"),max_length=150)
    short_description =models.TextField(("mô tả ngắn"))
    description =RichTextField(("mô tả"))
    image = models.ImageField(("ảnh bài viết"), upload_to='image/blog')
    status = models.BooleanField(("trạng thái"),default=True )
    date_at = models.DateTimeField(("ngày đăng") , auto_now_add=True ,editable=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural='09.chi tiết bài viết'
    @property
    def short_description_blog(self):
        return truncatechars(self.description, 100)    
        
    def img_tag(self):
        return mark_safe('<img src="%s" width="100px"  height="70px"  />' % (self.image.url))

class Contact(models.Model):
    name = models.CharField(("tên người phản hồi"),max_length=50)
    email = models.EmailField(("email"),max_length=50)
    message = models.TextField(("lời nhắn"))
    date_at = models.DateTimeField(("ngày phản hồi"),auto_now_add=True)
    class Meta:
        verbose_name_plural='10.phản hồi'

