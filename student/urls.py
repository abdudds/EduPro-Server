from django.urls import path
from .views import *


urlpatterns = [
    path('payment/<int:pk>', CheckoutView.as_view(), name='create-checkout-session'),
    path('stripe-webhook/', stripe_webhook_view, name='stripe-webhook'),
    path("purchased-courses/", PurchasedCourseView.as_view()),
    path("learning/", LearningView.as_view()),
    path("learningroom/<int:courseId>/", LearningRoomView.as_view()),

]