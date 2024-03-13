from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .serializer import *
from .models import *
# Create your views here.

class TutorRequest(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TutorSerializer
    queryset = Tutor.objects.all()

    def post(self, request):
        request.user.is_tutor = True
        request.user.save()
        prof = request.data.get("tutorpic",None)
        if prof:
            request.user.profile_img.save(prof.name,prof,save=True)

        request.data['user'] = request.user.id
        return super().post(request) 
    

class TutorDetailView(APIView):
    serializer_class = TutorSerializer
    queryset = Tutor.objects.all()

    def get(self, request, *args, **kwargs):
        print(' apiview')
        user_id = kwargs.get('user_id')

        try:
            tutor = Tutor.objects.get(user=user_id)
        except Tutor.DoesNotExist:
            return Response({'error': 'Tutor not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TutorSerializer(tutor)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchSkills(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SkillSerializer

    def post(self,request):

        query = self.request.data.get('query')
        if not query:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        queryset = Skill.objects.filter(skill__icontains=query)
        if not queryset.exists():
            return Response(status=status.HTTP_404_NOT_FOUND,data='null')
        queryset_data = SkillSerializer(queryset,many=True).data
        return Response(status=status.HTTP_200_OK,data=queryset_data)


class CreateSkill(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class CourseView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = AddCourseSerializer

    def get_queryset(self):
        tutor = Tutor.objects.filter(user=self.request.user.id).first()
        queryset = Course.objects.filter(tutor=tutor.id)
        return queryset
    
    def create(self, request, *args, **kwargs):
        print('create',request.data)
        tutor = Tutor.objects.filter(user=request.user)
        if not tutor.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST,data="You're not tutor")
        tutor = tutor.first()
        request.data['tutor'] = tutor.id
        serializer = AddCourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        print('post create')
        course = serializer.save()
        print('post', course)
        course.skill.set([int(strid) for strid in self.request.data.getlist('skill[]')])
        return 
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CourseSerializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        print('update')
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        print('update worked')
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        print('perform update')
        course = serializer.save()
        if self.request.data['skill[]']:
            course.skill.set([int(strid) for strid in self.request.data.getlist('skill[]')])
        return 


class ModuleView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def get_queryset(self):
        tutor = Tutor.objects.filter(user=self.request.user.id).first()
        course_id = self.request.query_params.get('course_id', None)
        course = Course.objects.filter(tutor=tutor.id, id=course_id).first()
        queryset = Module.objects.filter(course=course.id).order_by('moduleNo')
        return queryset
    
    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        modules_count = Module.objects.filter(course=course).count()
        serializer.save(moduleNo=modules_count + 1)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        queryset = Module.objects.filter(moduleNo__gt= instance.moduleNo, course = instance.course).order_by('moduleNo')
        print('query', queryset)
        for module in queryset:
            module.moduleNo -= 1
            module.save()
        return Response({"message": "Module deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        
    
class ChapterView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    def get_queryset(self):
        module_id = self.request.query_params.get('module_id', None)
        print(module_id,'++++++++++++++++++=================')
        queryset = Chapter.objects.filter(module=module_id).order_by('id')
        print(queryset,'+++++++++queryset')
        return queryset
    
    def create(self, request, *args, **kwargs):
        print(request.data, '++++++data++++++====')
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        print('==============+++++++++++++++++++')
        module = serializer.validated_data['module']
        print(module,'++++++++++++++++++=================')
        chapters_count = Chapter.objects.filter(module=module.id).count()
        serializer.save(chapterNo=chapters_count + 1)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        queryset = Chapter.objects.filter(chapterNo__gt= instance.chapterNo, module = instance.module).order_by('chapterNo')
        for chapter in queryset:
            chapter.chapterNo -= 1
            chapter.save()
        return Response({"message": "Chapter deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    
    