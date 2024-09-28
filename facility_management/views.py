import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Booking, Facility, Maintainance, Sport, BookingSlot
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import login, authenticate,logout

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def home(request):
    sports=Sport.objects.all()
    print(sports)
    return render(request, 'homepage.html', {'sports': sports})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            print('logged in')
            return redirect('home')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def register_user(request):
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        
        if password != request.POST['confirm_password']:
            return render(request, 'login.html', {'error': 'Passwords do not match'})
        # Create a new user
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )
        # Save the user
        user.save()
        return redirect('login')
    return render(request, 'login.html')


def facility_list(request, slug):
    facilities = Facility.objects.filter(sport__slug=slug)  # Retrieve all facilities
    print(facilities)
    return render(request, 'facilitys.html', {'facilities': facilities})


def facility_detail(request, slug):
    
    facility = Facility.objects.get(slug=slug) # Get the specific facility by slug
    if request.method == 'POST':
        print("date selected view")
        data = json.loads(request.body)  # request.body contains raw JSON data
        date = data.get('date', None) 
        booked_slots=Booking.objects.filter(facility=facility,booking_date=date)
        available_slots=BookingSlot.objects.filter(set_by=facility.manager)
        print(available_slots)
        available_slots = available_slots.exclude(id__in=booked_slots.values_list('slots__id', flat=True))
        print(available_slots)

        # Convert available slots to a list of time strings or IDs
        slots_data = [slot.start_time for slot in available_slots]

        # Return the available slots in JSON format
        return JsonResponse({'slots': slots_data})
        
    else:
        print(facility)
        print(" intial view")
        return render(request, 'facilitydetail.html', {'facility': facility})


@login_required
def profile(request):
    current_user = request.user
    print(current_user)
    booking=Booking.objects.filter(user=current_user)
    return render(request, 'profile.html', {'user': current_user,'booking':booking})


@login_required
@user_passes_test(lambda u: u.is_authenticated and u.role == 'manager')
def manager(request):
    user=request.user
    facility_list=Facility.objects.filter(manager=user)
    print(facility_list)
    bookings=Booking.objects.filter(facility__in=facility_list)# to make a calander like view of slots booked
    maintenance=Maintainance.objects.filter(facility__in=facility_list)
    
    
    return render(request,"managerview.html",{"facility_list":facility_list,"bookings":bookings,"maintenance":maintenance})


@login_required
@user_passes_test(lambda u: u.is_authenticated and u.role == 'manager')
def register_facility(request):
    sports = Sport.objects.all()  # Get available sports to display in the form
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST['name']
        location = request.POST['location']
        zip_code = request.POST['zip_code']
        description = request.POST['description']
        capacity = request.POST['capacity']
        open_time = request.POST['open_time']
        close_time = request.POST['close_time']
        sport_id = request.POST['sport']  # Assuming you send sport ID from the form
        sport = Sport.objects.get(id=sport_id)

        # Handle file uploads
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')

        # Save images to media directory
        facility = Facility.objects.create(
            name=name,
            location=location,
            zip_code=zip_code,
            description=description,
            capacity=capacity,
            open_time=open_time,
            close_time=close_time,
            sport=sport,
            manager=request.user,
        )

        if image1:
            facility.image1 = image1
        if image2:
            facility.image2 = image2
        if image3:
            facility.image3 = image3
        
        facility.save()  # Save the facility with uploaded images

        return redirect('manager')  # Redirect to a success page after saving

    return render(request, 'facility_registration.html', {'sports': sports})


@login_required
@user_passes_test(lambda u: u.is_authenticated and u.role == 'manager')
def update_facility(request, slug):
    facility = Facility.objects.get(slug=slug)
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST['name']
        location = request.POST['location']
        zip_code = request.POST['zip_code']
        description = request.POST['description']
        capacity = request.POST['capacity']
        open_time = request.POST['open_time']
        close_time = request.POST['close_time'] # Assuming you send sport ID from the form

        # Handle file uploads
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')

        # Save images to media directory
        if image1:
            facility.image1 = image1
        if image2:
            facility.image2 = image2
        if image3:
            facility.image3 = image3
        
        facility.name = name
        facility.location = location
        facility.zip_code = zip_code
        facility.description = description
        facility.capacity = capacity
        facility.open_time = open_time
        facility.close_time = close_time
        facility.save()  # Save the facility with uploaded images

        return redirect('manager')  # Redirect to a success page after saving

    return render(request, 'facility_update.html', {'facility': facility})

@login_required
@user_passes_test(lambda u: u.is_authenticated and u.role == 'manager')
def delete_facility(request, slug):
    facility = Facility.objects.get(slug=slug)
    if request.method == 'POST':
        facility.delete()
        return redirect('manager')
    return render(request, 'facility_delete.html', {'facility': facility})


@login_required
@user_passes_test(lambda u: u.is_authenticated and u.role == 'manager')
def update_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if request.method == 'POST':
        booking.confirmed = request.POST['status']
        booking.save()

        return redirect('manager')  # Redirect to a success page after saving

    return render(request, 'booking_update.html', {'booking': booking})

def sport_list(request):
    Sports = Sport.objects.all()
    return render(request, 'sports.html', {'sports': Sports})