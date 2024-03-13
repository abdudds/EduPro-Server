from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Tutor)
admin.site.register(Skill)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Chapter)

