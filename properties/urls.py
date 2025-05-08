from django.urls import path
from . import views
urlpatterns = [
    path('propertys/', views.PropertyView.as_view()),
    path('property/<str:pk>/',views.PropertyEditView.as_view()),
    path('listings/',views.ListingView.as_view()),
    path('listing/<str:pk>/',views.ListingEditView.as_view()),
    path('addtolistings/<str:id>/',views.AddToListingsView.as_view()),
    path('mylistings/',views.MyListingsView.as_view()),
    path('managelistings/<str:id>/',views.ManageListings.as_view()),
    path('checkout/',views.CheckoutView.as_view()),
    path('payment/<str:id>/',views.PaymentPageView.as_view(),name='payment'),
    path('<str:ref>/',views.VerifyPaymentView.as_view()),
]