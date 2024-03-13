from rest_framework import serializers
from tutor.serializer import CourseSerializer, ModuleSerializer, ChapterSerializer
from .models import *
from tutor.models import Chapter

class OrderSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    class Meta:
        model = Order
        fields = '__all__'

class LearningSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Learning
        fields = '__all__'