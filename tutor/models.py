from django.db import models
from users.models import User

# Create your models here.
class Tutor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=255)
    experience = models.CharField(choices=(('Beginner', 'Beginner'),('Intermediate', 'Intermediate'),('Advanced', 'Advanced')), max_length=255)
    language = models.CharField(choices=(('English', 'English'),('Spanish', 'Spanish'),('French', 'French'), ('Malayalam', 'Malayalam'),('Hindi','Hindi')), max_length=255)
    about = models.TextField(blank=True, null=True)

    @property
    def tutor_img(self):
        return self.user.profile_img_url()

    def __str__(self):
        return self.user.email
    
class Skill(models.Model):
    skill = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.skill

class Course(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    courseimg = models.ImageField(upload_to='Tutor/Course', default='courseDefault.webp')
    category = models.CharField(choices=(('Software Development', 'Software Development'),('Personal Development','Personal Development'),('Bioinformatics','Bioinformatics'),('Design','Design'),('Marketing','Marketing'),("Music","Music")),max_length=255)
    language = models.CharField(choices=(("English","English"),("Spanish","Spanish"),("French","French"),("Malayalam","Malayalam"),("Hindi","Hindi")),max_length=255)
    level = models.CharField(choices=(('Beginner', 'Beginner'),('Intermediate', 'Intermediate'),('Advanced', 'Advanced')), max_length=255, null=True, blank=True)
    skill = models.ManyToManyField(Skill,blank=True)
    duration = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    previewvideo = models.FileField(upload_to='video/preview',null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255, default='Draft')

    class Meta:
        unique_together = ('title','tutor')

    @property
    def tutor_name(self):
        return self.tutor.user.name

    def __str__(self):
        return self.title
    
class Module(models.Model):
   course = models.ForeignKey(Course, on_delete=models.CASCADE)
   title = models.CharField(max_length=255, null=True, blank=True)
   moduleNo = models.PositiveIntegerField(default=0)

   def __str__(self):
        return self.course.title
   
class Chapter(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    chapterNo = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to='video/chapters', null=True, blank=True)
    videoDuration = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    pdf = models.FileField(upload_to='pdfs', null=True, blank=True)

    def __str__(self):
        return self.module.course.title
    


