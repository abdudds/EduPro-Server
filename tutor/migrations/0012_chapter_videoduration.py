# Generated by Django 4.2.3 on 2024-03-12 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0011_delete_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='videoDuration',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
