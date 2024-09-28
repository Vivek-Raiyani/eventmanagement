# views.py
from django.shortcuts import render, redirect
from django.utils.text import slugify
from .models import Tournament, Sport

def register_tournament(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST['name']
        max_team = request.POST['max_team']
        is_team_based = request.POST['is_team_based'] == 'True'
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        sport_id = request.POST['sport']
        sport = Sport.objects.get(id=sport_id)
        registration_fee = request.POST['registration_fee']
        registration_number = request.POST['registration_number']
        description = request.POST['description']

        # Create Tournament instance
        tournament = Tournament(
            name=name,
            slug=slugify(name),
            max_team=max_team,
            is_team_based=is_team_based,
            start_date=start_date,
            end_date=end_date,
            sport=sport,
            registration_fee=registration_fee,
            registration_number=registration_number,
            description=description,
        )

        # Save tournament to the database
        tournament.save()

        # Redirect to a success page or back to the form
        return redirect('tournament_success')

    # Fetch available sports for the dropdown
    sports = Sport.objects.all()

    return render(request, 'tournamnet_registration.html', {'sports': sports})



def tournament_success(request):
    return render(request, 'tournamnet.html')

def tournamentdetails(request):
    return render(request, 'tournamentdetails.html')

