# Generated by Django 4.2.3 on 2024-03-12 01:31

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0012_chapter_videoduration'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student', '0003_alter_learning_course_completed'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RatingView',
            new_name='Rating',
        ),
    ]
