from rest_framework import serializers
from .models import *
from tutor.models import Course
from tutor.serializer import SkillSerializer


class UserSerializer(serializers.ModelSerializer):  
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'is_tutor', 'profile_img']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
       

class CourseSerializer(serializers.ModelSerializer):
    tutor_name = serializers.CharField(read_only=True)
    skill = SkillSerializer(many=True)
    # tutor = UserTutorSerializer()

    class Meta:
        model = Course
        fields = '__all__'


