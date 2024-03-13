# Generated by Django 4.2.3 on 2023-07-30 14:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('courseimg', models.ImageField(default='courseDefault.webp', upload_to='Tutor/Course')),
                ('category', models.CharField(choices=[('It & Software Development', 'It & Software Development'), ('Personal Development', 'Personal Development'), ('Bioinformatics', 'Bioinformatics'), ('Design', 'Design'), ('Marketing', 'Marketing'), ('Music', 'Music')], max_length=255)),
                ('language', models.CharField(choices=[('English', 'English'), ('Spanish', 'Spanish'), ('French', 'French'), ('Malayalam', 'Malayalam'), ('Hindi', 'Hindi')], max_length=255)),
                ('level', models.CharField(blank=True, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], max_length=255, null=True)),
                ('duration', models.PositiveIntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('previewvideo', models.FileField(blank=True, null=True, upload_to='video/preview')),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualification', models.CharField(max_length=255)),
                ('experience', models.CharField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], max_length=255)),
                ('language', models.CharField(choices=[('English', 'English'), ('Spanish', 'Spanish'), ('French', 'French'), ('Malayalam', 'Malayalam'), ('Hindi', 'Hindi')], max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutor.course')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='skill',
            field=models.ManyToManyField(blank=True, to='tutor.skill'),
        ),
        migrations.AddField(
            model_name='course',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutor.tutor'),
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('video', models.FileField(blank=True, null=True, upload_to='video/chapters')),
                ('pdf', models.FileField(blank=True, null=True, upload_to='pdfs')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutor.module')),
            ],
        ),
    ]