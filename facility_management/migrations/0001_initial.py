# Generated by Django 4.2.9 on 2024-09-26 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cancelled', models.BooleanField(default=False)),
                ('reason', models.CharField(blank=True, max_length=255, null=True)),
                ('confirmed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='BookingSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('rate', models.DecimalField(decimal_places=2, max_digits=8)),
                ('available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(editable=False, max_length=100, unique=True)),
                ('location', models.CharField(max_length=200)),
                ('zip_code', models.CharField(max_length=10)),
                ('description', models.TextField()),
                ('capacity', models.PositiveIntegerField()),
                ('open_time', models.TimeField()),
                ('close_time', models.TimeField()),
                ('available', models.BooleanField(default=True)),
                ('past_bookings', models.PositiveIntegerField(default=0, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(editable=False, max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Maintainance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('date_issued', models.DateField(auto_now_add=True)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facility_management.facility')),
            ],
        ),
    ]
