from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

# Get the User model in a more generic way to avoid issues if a custom user model is used
User = get_user_model()

class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensure Sport name is unique
    slug = models.SlugField(max_length=100, unique=True, editable=False)  # Slug should not be editable manually
    banner=models.ImageField(upload_to='images/sport_banners/',null=True,blank=True)

    def save(self, *args, **kwargs):
        # Auto-generate slug only if not set, to allow editing names without changing URLs
        if not self.slug:
            self.slug = slugify(self.name)
        super(Sport, self).save(*args, **kwargs)

    def __str__(self):
        return self.name  # Using name as it's more human-readable


class Facility(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensure facility name is unique
    slug = models.SlugField(max_length=100, unique=True, editable=False)  # Auto-generated slug
    location = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=10)  # Increased length to accommodate more formats
    description = models.TextField()
    capacity = models.PositiveIntegerField()  # Ensure capacity is positive
    open_time = models.TimeField()
    close_time = models.TimeField()
    available = models.BooleanField(default=True)
    past_bookings = models.PositiveIntegerField(default=0, editable=False)  # Track past bookings, read-only

    sport = models.ForeignKey(Sport,on_delete=models.PROTECT)  # Prevent deleting Sport if linked to Facility
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Handle manager deletion gracefully
    
    video=models.FileField(upload_to='videos/', null=True, blank=True)
    image1=models.ImageField(upload_to='images/', null=True, blank=True)
    image2=models.ImageField(upload_to='images/', null=True, blank=True)
    image3=models.ImageField(upload_to='images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Facility, self).save(*args, **kwargs)

    def __str__(self):
        return self.name  # Return the human-readable name of the facility


class Maintainance(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    date_issued = models.DateField(auto_now_add=True)  # Automatically set the issue date
    cost=models.PositiveIntegerField(default=0)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)  # Deleting Facility deletes related maintenance
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Handle user deletion gracefully

    def __str__(self):
        return f"{self.facility} maintenance from {self.start_date} to {self.end_date}"


class BookingSlot(models.Model):
    set_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Handle user deletion gracefully
    start_time = models.TimeField()
    end_time = models.TimeField()
    rate = models.DecimalField(max_digits=8, decimal_places=2)  # Use DecimalField for financial data
    available = models.BooleanField(default=True)

    class Meta:
        unique_together = ( 'start_time', 'end_time')  # Prevent time overlaps

    def __str__(self):
        return f" slot {self.start_time} - {self.end_time}"


class Booking(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE) # Deleting Facility deletes slots
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Deleting User deletes their bookings
    slots = models.ForeignKey(BookingSlot, on_delete=models.CASCADE)
    booking_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set booking creation time
    cancelled = models.BooleanField(default=False)
    reason = models.CharField(max_length=255, blank=True, null=True)  # Allow more space and be optional
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking at {self.facility} by {self.user} on {self.booking_date}"

    class Meta:
        unique_together = ('facility','slots', 'booking_date','cancelled')  # Prevent double booking for the same slot

