from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from tutor.models import *
from student.models import *
from tutor.serializer import TutorSerializer
from .serializer import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




# Create your views here.

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email',None)
        serializer = UserSerializer(data=request.data)
        if User.objects.filter(email=email).exists():
            return Response(data={'message':'Email Already Exists'},status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        user.is_active = True
        user.save()
        return Response(serializer.data)
    
class UserLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.pop("email", None)
        password = request.data.pop("password", None)

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                user_data = {
                "email": user.email,
                "user_id": user.id,
                "profile": user.profile_img_url,
                "is_tutor": user.is_tutor,
                }
                
                return Response(
                    status=status.HTTP_202_ACCEPTED,
                    data={"message": "logged in", "user": user_data},
                )
            else:
                if User.objects.filter(email=email).exists():
                    return Response(
                        status=status.HTTP_401_UNAUTHORIZED,
                        data={"message": "Wrong Password !"},
                    )
                else:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={"message": "No Such User !"},
                    )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "credentials not provided"},
            )
        
class Logout(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            token = RefreshToken(request.data["refresh-token"])
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Token Not Provided"},
            )


class CourseView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset = Course.objects.filter(status='Running').order_by('?')[:4]
        return queryset
    

class CategoryView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, format=None):
        category_choices = Course._meta.get_field('category').choices
        category = [{'id': idx+1, 'category': category_choices[idx][0]} for idx in range(len(category_choices))]
        # print(category)
        return Response(category)
    

class AllCourseView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        all_params = self.request.GET.dict()
        print(all_params)
        
        category = all_params.get('category', 'All')
        level = all_params.get('level', 'All')
        price_range = all_params.get('price', 'All')
        search_query = all_params.get('search', 'All')

        category = None if category == 'All' else category
        level = None if level == 'All' else level

        if price_range != 'All':
            min_price, max_price = price_range.split(',')
            min_price = int(min_price) if min_price != 'Infinity' else None
            max_price = int(max_price) if max_price != 'Infinity' else None
        else:
            min_price, max_price = None, None

        filter_conditions = Q(status='Running')

        if category is not None:
            filter_conditions &= Q(category=category)
        if level is not None:
            filter_conditions &= Q(level=level)
        if min_price is not None:
            filter_conditions &= Q(price__gte=min_price)
        if max_price is not None:
            filter_conditions &= Q(price__lte=max_price)

        if search_query != 'All':
            filter_conditions &= (Q(title__icontains=search_query) | Q(tutor__user__name__icontains=search_query))

        print(filter_conditions)

        limit = int(all_params.get('limit', 9))  
        offset = int(all_params.get('skip', 0))

        queryset = Course.objects.filter(filter_conditions)

        paginator = Paginator(queryset, limit)

        try:
            page = paginator.page(offset // limit + 1)
        except (EmptyPage, PageNotAnInteger):
            return Course.objects.none()

        return page.object_list
    

class CourseDetailsView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            course = self.get_object()
            tutor = Tutor.objects.get(id=course.tutor.id)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        except Tutor.DoesNotExist:
            return Response({'error': 'Tutor not found'}, status=status.HTTP_404_NOT_FOUND)

        course_serializer = self.get_serializer(course)
        tutor_serializer = TutorSerializer(tutor)

        # Return a dictionary containing both course and tutor data
        data = {
            'course': course_serializer.data,
            'tutor': tutor_serializer.data,
        }

        return Response(data)  






        