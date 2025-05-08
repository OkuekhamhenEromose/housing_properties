
from rest_framework import serializers
from .models import *

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model=Property
        fields='__all__'

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Listing
        fields='__all__'

class UserListingSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserListing
        fields='__all__'

class SingleListingSerializer(serializers.ModelSerializer):
    class Meta:
        model=SingleListing
        fields='__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'

class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        exclude=['userlisting','amount','order_status','subtotal','payment_complete','ref']
 