# Generated by Django 4.2.9 on 2024-09-29 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facility_management', '0007_alter_booking_facility_alter_bookingslot_set_by'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together={('facility', 'slots', 'booking_date', 'cancelled')},
        ),
    ]
