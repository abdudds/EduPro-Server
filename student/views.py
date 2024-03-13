from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from tutor.models import Course
from users.models import User
from .models import *
from .serializer import *
from tutor.serializer import CourseSerializer, ModuleSerializer, ChapterSerializer
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.http import HttpResponse

# Create your views here.

# Payment Section

stripe.api_key=settings.STRIPE_SECRET_KEY

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        course_id = self.kwargs["pk"]
        print(course_id)
        try:
            course = Course.objects.get(id=course_id)
            user = request.user
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': course.title,
                        },
                        'unit_amount': int(course.price * 100),
                    },
                    'quantity': 1,
                }],
                 metadata={
                    "course_id":course.id,
                    "user_id": user.id,
                },
                mode='payment',
                success_url=settings.SITE_URL + 'payment?success=true',
                cancel_url=settings.SITE_URL + 'payment?canceled=true',
            )

            return Response({'checkout_url': checkout_session.url})
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, settings.STRIPE_SECRET_WEBHOOK
        )
    except ValueError as e:
        # Invalid payload
        return Response(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return Response(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email=session['customer_details']['email']
        course_id=session['metadata']['course_id']
        print(course_id,'++++++++++++++++')
        course=Course.objects.get(id=course_id)
        user_id = session['metadata']['user_id']

        user = User.objects.get(id=user_id)
        #sending confimation mail
        send_mail(
            subject="payment sucessful",
            message=f"thank for your purchase your course is ready.",
            recipient_list=[customer_email],
            from_email="edupro597@gmail.com"
        )

        Order.objects.create(user=user,course=course,amount=course.price,payment_status=True)
    return HttpResponse(status=200)

class PurchasedCourseView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        orders = Order.objects.filter(user=user)

        serializer = OrderSerializer(orders, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

class LearningRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        courseId = kwargs.get('courseId')
        print(courseId,'+++++++++++===========')

        try:
            # Get course details
            course = Course.objects.get(id=courseId)
            course_serializer = CourseSerializer(course)

            # Get modules related to the courseId
            modules = Module.objects.filter(course_id=courseId).order_by('moduleNo')
            module_serializer = ModuleSerializer(modules, many=True)

            # Get chapters related to the modules
            chapters = Chapter.objects.filter(module__in=modules).order_by('chapterNo')
            chapter_serializer = ChapterSerializer(chapters, many=True, context={'request':request})
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'course': course_serializer.data,
            'modules': module_serializer.data,
            'chapters': chapter_serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)

class LearningView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        courseId = kwargs.get('courseId')
        
        try:
            learning = Learning.objects.filter(id=courseId)
        except Course.DoesNotExist:
            return Response({'error': 'Learning progress not found'}, status=status.HTTP_404_NOT_FOUND)
        print(learning,'++++++++++Learning===========')
        serializer = LearningSerializer(learning, many=True, context={'request':request})

        return Response(serializer.data, status=status.HTTP_200_OK)