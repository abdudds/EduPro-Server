from rest_framework import serializers
from .models import *

class TutorSerializer(serializers.ModelSerializer):
    tutor_img = serializers.SerializerMethodField()

    class Meta:
        model = Tutor
        fields = '__all__'

    def get_tutor_img(self, obj):
        return obj.user.profile_img_url

class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = '__all__'

class AddCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(many=True)
    tutor_name = serializers.CharField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'

class ChapterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Chapter
        fields = '__all__'
