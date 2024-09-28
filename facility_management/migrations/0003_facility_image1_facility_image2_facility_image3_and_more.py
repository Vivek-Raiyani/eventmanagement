# Generated by Django 4.2.9 on 2024-09-26 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facility_management', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='facility',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='facility',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='facility',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
    ]
