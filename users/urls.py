from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path("login/", UserLogin.as_view(), name="login"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("logout/", Logout.as_view(), name="logout"),

    path("popular/course/", CourseView.as_view(), name="course"),
    path("categories/", CategoryView.as_view(), name="category"),
    path("courses/", AllCourseView.as_view(), name="allcourse"),
    path("course-details/<int:pk>/", CourseDetailsView.as_view(), name="course-details"),
    

]