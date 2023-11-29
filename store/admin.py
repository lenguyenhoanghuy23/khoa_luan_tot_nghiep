from django.contrib import admin


from .models import * 


class productadmin(admin.ModelAdmin):
    list_display = ('nameProduct','short_description_product','img_tag','price','status','is_feature','category')
    list_filter = ('nameProduct', 'price','status','is_feature','status','category') #lọc theo danh sách
    list_per_page = 15
    search_fields = ['nameProduct']
  

class dproductadmin(admin.ModelAdmin):
    list_display = ('products','img_tag')
    list_per_page = 15

class CartOrderadmin(admin.ModelAdmin):
    list_display = ('user','total_amt','paid_status','order_dt','order_status','complete')
    # fields = ('user', 'total_amt', 'paid_status') chọn table muốn hiện thị
    # list_display_links = ('paid_status', 'total_amt') chọn table muốn link
    list_filter = ('user', 'order_dt')
    ordering = ['order_dt']
    # search_fields = ['user','total_amt','order_dt']
    list_per_page = 15

    

class CartOrderItemsadmin(admin.ModelAdmin):
    list_display = ('order','invoice_no','item','img_tag','qty','price','total')
    list_per_page = 15

class ShippingAddressadmin(admin.ModelAdmin):
    list_display = ('order','address','lastname','phone','des','email','date_added')
    list_filter = ('address','lastname','date_added')
    list_per_page = 15

class blogAddressadmin(admin.ModelAdmin):
     list_display = ('cateblog','name','short_description_blog','img_tag','status','date_at')

class contactamdin(admin.ModelAdmin):
    list_display = ('name','email','message','date_at')
    
    def has_delete_permission(self, request, obj=None): #không cho phép xóa table
        #Disable delete
        return False    
    def has_add_permission(self, request, obj=None):
        return False

# Register your models here.


admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Products,productadmin)
admin.site.register(DProducts,dproductadmin)
admin.site.register(CartOrder,CartOrderadmin)
admin.site.register(CartOrderItems,CartOrderItemsadmin)
admin.site.register(ShippingAddress,ShippingAddressadmin)
admin.site.register(categoryblog)
admin.site.register(blog,blogAddressadmin)
admin.site.register(Contact,contactamdin)

