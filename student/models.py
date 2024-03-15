from django.db import models
from users.models import User
from tutor.models import *
# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now=True)
    payment_status=models.BooleanField(default=False)

    def __str__(self):
        return self.user.name
    
class Learning(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # module = models.ForeignKey(Module, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    # course_completed = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    chapter_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.course.title

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)
    review = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.course.title