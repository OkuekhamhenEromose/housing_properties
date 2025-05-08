
from rest_framework import status,permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import reverse
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.conf import settings

import requests
from . serializers import *
from . models import *


# Create your views here.

class PropertyView(APIView):
    def get(self,request):
        try:
            property = Property.objects.all() 
            serializer = PropertySerializer(property,many=True)# getting many listings, then many = True
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # permission_classes=[permissions.IsAdminUser]
    def post(self,request):
        try:
            serializer = PropertySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PropertyEditView(APIView):
    def get(self,request,pk):
        try:
            property = get_object_or_404(Property,pk=pk)
            serializer = PropertySerializer(property)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self,request,pk):
        try:
            property = get_object_or_404(Property,pk=pk)
            serializer = PropertySerializer(property,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self,request,pk):
        try:
            property = get_object_or_404(Property,pk=pk)
            property.delete()
            return Response({"Message":"Property deleted"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListingView(APIView):
    def get(self,request):
        try:
            listing = Listing.objects.all() 
            serializer = ListingSerializer(listing,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # permission_classes=[permissions.IsAdminUser]
    def post(self,request):
        try:
            serializer = ListingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# :: product get,update and delete
class ListingEditView(APIView):
    def get(self,request,pk):
        try:
            listing = get_object_or_404(Listing,pk=pk)
            serializer = ListingSerializer(listing)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self,request,pk):
        try:
            listing = get_object_or_404(Listing,pk=pk)
            serializer = ListingSerializer(listing,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self,request,pk):
        try:
            product = get_object_or_404(Listing,pk=pk)
            product.delete()
            return Response({"Message":"Listing deleted"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddToListingsView(APIView):
    def post(self,request,id):
        try:
            # fet the product
            listing = get_object_or_404(Listing,id=id)
            # get the cart id
            userlisting_id = request.session.get('userlisting_id',None)
            
            with transaction.atomic():
                if userlisting_id:
                    userlisting = UserListing.objects.filter(id=userlisting_id).first()
                    if userlisting is None:
                        userlisting = UserListing.objects.create(total=0)
                        request.session['userlisting_id'] = userlisting.id
                    
                    this_listing = userlisting.singlelisting_set.filter(listing=listing)

                    # assigning cart to a user 
                    if request.user.is_authenticated and hasattr(request.user,'profile'):
                        userlisting.profile = request.user.profile
                        userlisting.save()

                    if this_listing.exists():
                        singlelisting = this_listing.last()
                        singlelisting.quantity +=1
                        singlelisting.subtotal +=listing.price
                        singlelisting.save()
                        # update our cart
                        userlisting.total += listing.price
                        userlisting.save()
                        return Response({"Message":"Item increase in cart"})
                    else:
                        singlelisting = SingleListing.objects.create(userlisting=userlisting,listing=listing,quantity=1,subtotal=listing.price)
                        singlelisting.save()
                        # update our cart
                        userlisting.total += listing.price
                        userlisting.save()
                        return Response({"Message":"A new Item added to cart"})

                else:
                    # create a cart
                    userlisting = UserListing.objects.create(total=0)
                    request.session['userlisting_id'] = userlisting.id
                    singlelisting = SingleListing.objects.create(userlisting=userlisting,listing=listing,quantity=1,subtotal=listing.price)
                    singlelisting.save()
                    # update our cart
                    userlisting.total += listing.price
                    userlisting.save()
                    return Response({"Message":"A new cart created"})

        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MyListingsView(APIView):
    def get(self,request):
        try:
            userlisting_id = request.session.get('userlisting_id', None)
            if userlisting_id:
                userlisting = get_object_or_404(UserListing,id=userlisting_id)
                # assigning cart to a user 
                if request.user.is_authenticated and hasattr(request.user,'profile'):
                    userlisting.profile = request.user.profile
                    userlisting.save()
                serializer = UserListingSerializer(userlisting)
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response({"error":"cart not found"},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ManageListings(APIView):
    def post(self,request,id):
        action = request.data.get('action')
        try:
            userlisting_obj = get_object_or_404(SingleListing,id=id)
            userlisting = userlisting_obj.userlisting
            if action == "inc":
                userlisting_obj.quantity +=1
                userlisting_obj.subtotal += userlisting_obj.product.price
                userlisting_obj.save()
                userlisting.total +=userlisting_obj.product.price
                userlisting.save()
                return Response({"Message":"Item increase"},status=status.HTTP_200_OK)
            elif action == "dcr":
                userlisting_obj.quantity -=1
                userlisting_obj.subtotal -= userlisting_obj.product.price
                userlisting_obj.save()
                userlisting.total -=userlisting_obj.product.price
                userlisting.save()
                if userlisting_obj.quantity == 0:
                    userlisting_obj.delete()
                return Response({"Message":"Item decrease"},status=status.HTTP_200_OK)
            elif action == 'rmv':
                userlisting.total -= userlisting_obj.subtotal
                userlisting.save()
                userlisting_obj.delete()
                return Response({"Message":"Item removed"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CheckoutView(APIView):
    def post(self,request):
        userlisting_id = request.session.get('userlisting_id',None)
        if not userlisting_id:
            return Response({"Error":"Cart not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            userlisting_obj = get_object_or_404(UserListing,id=userlisting_id)
        except UserListing.DoesNotExists:
            return Response({"Error":"Cart does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save(
                userlisting = userlisting_obj,
                amount = userlisting_obj.total,
                subtotal = userlisting_obj.total,
                order_status = 'pending'
            )
            del request.session['userlisting_id']

            if order.payment_method == 'paystack':
                payment_url = reverse('payment',args=[order.id])
                return Response({'redirect_url': payment_url},status=status.HTTP_302_FOUND)
            
            return Response({'Message': 'Order Created Successfully'})
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PaymentPageView(APIView):
    def get(self,request,id):
        try:
            order = get_object_or_404(Order,id=id)
        except Order.DoesNotExist:
            return Response({'Error':'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        # Create payment request
        url = "https://api.paystack.co/transaction/initialize"
        headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        data = {
            "amount": order.amount * 100,
            "email": order.email,
            "reference": order.ref
        }

        response = requests.post(url, headers=headers, data=data)
        response_data = response.json()

        if response_data["status"]:
            paystack_url = response_data["data"]["authorization_url"]

            return Response({
                'order': order.id,
                'total': order.amount_value(),
                'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
                'paystack_url': paystack_url
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST)

# verify payment
class VerifyPaymentView(APIView):
    def get(self,request,ref):
        try:
            order = get_object_or_404(Order,ref=ref)
            url = f'https://api.paystack.co/transaction/verify/{ref}'
            headers= {"Authorization":f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
            response = requests.get(url,headers=headers)
            response_data = response.json()

            if response_data["status"] and response_data["data"]["status"]=="success":
                order.payment_complete = True
                order.save()
                return Response({"Message":"Payment verify successfully"},status=status.HTTP_200_OK)
            elif response_data["data"]["status"] == "abandoned":
                # Handle abandoned payment
                order.order_status = "pending" 
                order.save()
                return Response({"Error": "Payment abandoned, please try again."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Error":"Payment verify failed"},status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({'error':'invalid payment reference'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
 