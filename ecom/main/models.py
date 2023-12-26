from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
# class CustomUser(AbstractUser):
#     is_vendor=models.BooleanField(default=False)

class ProductDetails(models.Model):
    Pvendorname = models.CharField(max_length=100) #vendors username
    Pname = models.CharField(max_length=100)
    Ppicture = models.ImageField(upload_to='product_picture', null=True,blank=True)
    Pdesc = models.CharField(max_length=1000)
    Pstock = models.IntegerField()
    Pprice = models.IntegerField()
    Pmallname = models.CharField(max_length=100)
    Pcatg = models.CharField(max_length=100)
    product_code = models.CharField(max_length=15, unique=True, editable=False)  # Custom product code field

    def generate_product_code(self):
        last_product = ProductDetails.objects.filter(Pvendorname=self.Pvendorname).order_by('-id').first()

        if last_product:
            zeros = "0" * (15 - len(f'pc-{self.Pvendorname[0:3]}{last_product.id}'))
            self.product_code = f'pc-{self.Pvendorname[0:3]}{zeros}{last_product.id}'
        else:
            self.product_code = f'pc-{self.Pvendorname[0:3]}{"0" * 9}'
    def __str__(self):
        return self.product_code
    


class cartProductitems(models.Model):
    username = models.CharField(max_length=100)
    CPname = models.CharField(max_length=150)
    CPpicture = models.ImageField(upload_to='cart_picture', null=True,blank=True)
    ProductID = models.IntegerField()
    CPrice = models.IntegerField() 

class PurchesDetails(models.Model):
    username= models.CharField(max_length=100) #its usernamer of buyer
    PPname= models.CharField(max_length=100) #it is products vendor name not product name
    PPid = models.IntegerField() #main products id
    Pfirstname= models.CharField(max_length=100)
    Plastname= models.CharField(max_length=100)
    Pmobile = models.IntegerField()
    Pemail =models.EmailField()
    Padderss= models.CharField(max_length=100)
    Pzipcode = models.IntegerField()
    Pdivision= models.CharField(max_length=100)
    Pcity= models.CharField(max_length=100)
    Parea= models.CharField(max_length=100)
    Pdeliverytyp= models.CharField(max_length=100)
    quantity = models.IntegerField()
    product_code = models.CharField(max_length=15, editable=False)  # Custom product code field
    confirmation = models.BooleanField(default=False)
    PurchesTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        conf = self.confirmation
        if conf == True:       
            return "confiremed"
        else:
            return "Not Confirmed"
