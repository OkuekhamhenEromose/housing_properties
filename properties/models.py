import uuid
from django.db import models
from housing.models import Profile
import secrets
from . paystack import Paystack


CATEGORY_CHOICES =(
    ('sale', 'For Sale'),
    ('rent', 'For Rent')
)
# for each property, there can be multiple listings. this presents a property for market
class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='sale')
    photo = models.ImageField(upload_to='property')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
  #  complete description of the property
class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    sqft = models.IntegerField()
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    main = models.ImageField(upload_to='listing')
    photo1 = models.ImageField(upload_to='listing',null=True,blank=True)
    photo2 = models.ImageField(upload_to='listing',null=True,blank=True)
    photo3 = models.ImageField(upload_to='listing',null=True,blank=True)
    photo4 = models.ImageField(upload_to='listing',null=True,blank=True)
    listing_id = models.UUIDField(unique=True,default=uuid.uuid4)
    is_published = models.BooleanField(default=True)
    posted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    def save(self,*args, **kwargs):
        if not self.listing_id:
            self.listing_id = uuid.uuid4()
        super().save(*args, **kwargs)

class UserListing(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True,blank=True)
    total = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{str(self.total)}'

class SingleListing(models.Model):
    userlisting = models.ForeignKey(UserListing, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'UserListing Listing - {self.userlisting.id} -{self.quantity}'

ORDER_STATUS=(
    ('pending','pending'),
    ('cancel','cancel'),
    ('complete','complete')
)
PAYMENT_METHOD=(
    ('paystack','paystack'),
    ('paypal','paypal'),
    ('transfer','transfer')
)
class Order(models.Model):
    userlisting = models.ForeignKey(UserListing, on_delete=models.CASCADE)
    order_by = models.CharField(max_length=255)
    shipping_address = models.TextField()
    mobile = models.CharField(max_length=50)
    email = models.EmailField()
    amount = models.PositiveBigIntegerField()
    subtotal = models.PositiveBigIntegerField()
    order_status = models.CharField(max_length=50,choices=ORDER_STATUS,default='pending')
    payment_method = models.CharField(max_length=50,choices=PAYMENT_METHOD,default='paystack')
    payment_complete = models.BooleanField(default=False)
    ref = models.CharField(max_length=255,null=True,unique=True)

    def __str__(self):
        return f'{self.amount} - {str(self.id)}'
    
    # auto save ref
    def save(self,*args,**kwargs):
        # if not self.ref:
        #     self.ref = self.secrets.token_urlsafe(50)
        # super().save(**args,**kwargs)
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            obj_with_sm_ref = Order.objects.filter(ref=ref)
            if not obj_with_sm_ref:
                self.ref = ref
        super().save(*args, **kwargs)
    
    # amount from cent/kobo to naira
    def amount_value(self)->int:
        return self.amount * 100
    
    # verifying payment on paystack
    def verify_payment(self):
        paystack = Paystack()
        status,result = paystack.verify_payment(self.ref)
        if status and result.get('status') == 'success':
            # ensure the amount  matches'
            if result['amount']/100 == self.amount:
                self.payment_complete = True
                # del self.cart
                self.save()
                return True
        # if payment is not successful
        return False


