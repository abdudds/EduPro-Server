# Generated by Django 4.2.3 on 2023-11-17 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0003_course_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
