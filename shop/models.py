from django.db import models

# Create your models here.
categoryList = [
    ("Marble Vases","Marble Vases"),
    ("Marble Lamps","Marble Lamps"),
    ("Marble Decorative","Marble Decorative"),
    ("Marble Artifacts","Marble Artifacts"),
    ("Marble Paintings","Marble Paintings"),
    ("Decorative Marble Pen Stands","Decorative Marble Pen Stands")
]

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    price = models.IntegerField()
    category = models.CharField(max_length=50, choices=categoryList)
    size = models.CharField(max_length=35, default='15"x15"x25"')
    material = models.CharField(max_length=20, default="Makrana Marble")
    color = models.CharField(max_length=15, default="White")
    publish_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="shop/products/images")
    instock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    minbuy = models.IntegerField(default=1)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

class ProductImage(models.Model):
    imageId = models.IntegerField()
    image = models.ImageField(upload_to="shop/products/images")

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


class Enquiry(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=6)
    phone = models.CharField(max_length=10)
    cartcontent = models.TextField()
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Contact(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    phone = models.CharField(max_length=10)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
