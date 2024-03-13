from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'course', CourseView)
router.register(r'module', ModuleView)
router.register(r'chapter', ChapterView)


urlpatterns = [
    path('', include(router.urls)),
    path('request/', TutorRequest.as_view()), 
    path('<int:user_id>/', TutorDetailView.as_view(), name='tutor-detail'),
    path('search-skill/',SearchSkills.as_view()),
    path('add-skill/',CreateSkill.as_view()),
]