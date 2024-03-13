# permissions.py
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status 
from .models import *

class CustomTutorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # tutor = Tutor.objects.filter(user=request.user)
        course = Course.objects.filter(tutor=request.user, id=request.id)
        if not course.exists() :
            return Response(status=status.HTTP_400_BAD_REQUEST,data="You're not tutor this course")
        # Add your custom permission logic here
        # Return True if the user has permission, False otherwise
        # Example: Allow access only to authenticated users
        return request.user and request.user.is_authenticated
