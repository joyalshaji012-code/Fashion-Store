from django.contrib.auth.models import User as Logins
from django.db import models

# Create your models here.
class Workers(models.Model):
    name=models.CharField(max_length=20)
    email=models.CharField(max_length=30)
    phone=models.BigIntegerField(max_length=200)
    place = models.CharField(max_length=30)
    post = models.CharField(max_length=30)
    pin = models.IntegerField(max_length=30)
    proof = models.CharField(max_length=200)
    LOGIN=models.ForeignKey(Logins,on_delete=models.CASCADE)
    status = models.CharField(max_length=30)
    reason = models.CharField(max_length=300)

class Products(models.Model):
    WORKER=models.ForeignKey(Workers,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    requested_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.CharField(max_length=200)
    # size = models.CharField(max_length=30)
    status = models.CharField(max_length=30, default="pending")
    categories = models.CharField(max_length=30)
    
    def get_colors(self):
        """Get all unique colors for this product from Stock"""
        return self.stock_set.values_list('color', flat=True).distinct()
    
    def get_sizes(self):
        """Get all unique sizes for this product from Stock"""
        return self.stock_set.values_list('size', flat=True).distinct()
    
    def get_stock_items(self):
        """Get all stock items (combines size, color, image, and quantity)"""
        return self.stock_set.all()
    
    def get_primary_image(self):
        """Get primary product image or first stock image"""
        if self.image:
            return self.image
        stock = self.stock_set.first()
        return stock.image if stock else None

class Productsbycolor(models.Model):
    PRODUCT=models.ForeignKey(Products,on_delete=models.CASCADE)
    color = models.CharField(max_length=30)
    image = models.CharField(max_length=200)

class Salerequests(models.Model):
    PRODUCT=models.ForeignKey(Products,on_delete=models.CASCADE)
    qty=models.CharField(max_length=20)
    date = models.DateField(max_length=30)
    status = models.CharField(max_length=20)
    paymentstatus = models.CharField(max_length=20)
    paymentdate = models.DateField(max_length=20)

class Customers(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    phone = models.IntegerField(max_length=100)
    LOGIN=models.ForeignKey(Logins,on_delete=models.CASCADE)

class Carts(models.Model):
    CUSTOMER=models.ForeignKey(Customers,on_delete=models.CASCADE)
    PRODUCT=models.ForeignKey(Products,on_delete=models.CASCADE)
    qty = models.IntegerField(max_length=20)
    selectedcolor = models.CharField(max_length=20)
    size = models.CharField(max_length=20)
    customization = models.CharField(max_length=200)

class Orders(models.Model):
    CUSTOMER=models.ForeignKey(Customers,on_delete=models.CASCADE)
    date = models.DateField(max_length=20)
    status = models.CharField(max_length=20)
    amount = models.IntegerField(max_length=20)
    paymentstatus = models.CharField(max_length=20)
    paymentdate = models.DateField(max_length=20)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    address = models.CharField(max_length=50)

class Ordereditems(models.Model):
    ORDER=models.ForeignKey(Orders,on_delete=models.CASCADE)
    PRODUCT=models.ForeignKey(Products,on_delete=models.CASCADE)
    qty = models.CharField(max_length=20)
    selectcolor = models.CharField(max_length=20)
    size = models.CharField(max_length=20)
    customization = models.CharField(max_length=20)

class Feedback(models.Model):
    CUSTOMER=models.ForeignKey(Customers,on_delete=models.CASCADE)
    feedback = models.CharField(max_length=200)
    date = models.DateField(max_length=20)

class Review(models.Model):
    CUSTOMER=models.ForeignKey(Customers,on_delete=models.CASCADE)
    PRODUCT=models.ForeignKey(Products,on_delete=models.CASCADE)
    rating = models.CharField(max_length=20)
    comment = models.CharField(max_length=200)
    date = models.DateField(max_length=20)

class Balance(models.Model):
    WORKER=models.ForeignKey(Workers,on_delete=models.CASCADE)
    amount=models.CharField(max_length=20)

class Deliverystatus(models.Model):
    ORDER=models.ForeignKey(Orders,on_delete=models.CASCADE)
    status=models.CharField(max_length=20)
    date=models.DateField(max_length=20)
    description=models.CharField(max_length=300)

class Stock(models.Model):
    PRODUCT=models.ForeignKey(Products,on_delete=models.CASCADE)
    size=models.CharField(max_length=20)
    stock = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    image = models.CharField(max_length=200)
    
    def in_stock(self):
        """Check if this size/color combination is in stock"""
        try:
            return int(self.stock) > 0
        except:
            return False
    
    def get_stock_quantity(self):
        """Get stock quantity as integer"""
        try:
            return int(self.stock)
        except:
            return 0


