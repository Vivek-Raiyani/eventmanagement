# Generated by Django 4.2.9 on 2024-09-26 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('facility_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='maintainance',
            name='issued_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facility',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facility',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facility_management.sport'),
        ),
        migrations.AddField(
            model_name='bookingslot',
            name='facility',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facility_management.facility'),
        ),
        migrations.AddField(
            model_name='booking',
            name='facility',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facility_management.facility'),
        ),
        migrations.AddField(
            model_name='booking',
            name='slots',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facility_management.bookingslot'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='bookingslot',
            unique_together={('facility', 'start_time', 'end_time')},
        ),
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together={('slots', 'booking_date')},
        ),
    ]
