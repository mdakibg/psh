from django.contrib import admin
from .models import Product, Contact, Enquiry

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'publish_date')

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created_at' , 'text')

class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'city', 'state' , 'amount', 'created_at', 'updated_at')

admin.site.register(Product, ProductAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Enquiry, EnquiryAdmin)