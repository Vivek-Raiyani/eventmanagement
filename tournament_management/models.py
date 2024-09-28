from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

# Get the User model in a more generic way to avoid issues if a custom user model is used
User = get_user_model()


class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensure unique sport names
    slug = models.SlugField(max_length=100, unique=True, editable=False)  # Slug should be auto-generated and non-editable
    banner=models.ImageField(upload_to='images/sport_banners/',null=True,blank=True)
    video=models.FileField(upload_to='videos/sport_videos/',null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Sport, self).save(*args, **kwargs)

    def __str__(self):
        return self.name  # Return name instead of slug for better readability


class Tournament(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensure unique tournament names
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    max_team = models.PositiveIntegerField()  # Ensure positive number of teams
    is_team_based = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    sport = models.ForeignKey(Sport, on_delete=models.PROTECT)  # Prevent sport deletion if associated with tournaments
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2)  # Use Decimal for monetary values
    registration_number = models.PositiveIntegerField()
    description = models.TextField()
    prizes_first = models.PositiveIntegerField(default=0)
    prizes_second = models.PositiveIntegerField(default=0)
    prizes_third = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tournament, self).save(*args, **kwargs)

    def __str__(self):
        return self.name  # Return human-readable name


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    captain = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='captain_of_team')  # Handle captain deletion gracefully
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    players = models.ManyToManyField(User)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Team, self).save(*args, **kwargs)

    def __str__(self):
        return self.name  # Return human-readable team name


class Match(models.Model):
    ROUND_CHOICES = [
        ("group_stage", "Group Stage"),
        ("round_of_16", "Round of 16"),
        ("quarter_finals", "Quarter Finals"),
        ("semi_finals", "Semi Finals"),
        ("final", "Final"),
    ]

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="matches_as_team2")
    scores_team1 = models.PositiveIntegerField()  # Scores should be numeric
    scores_team2 = models.PositiveIntegerField()
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name="wins")  # Handle nullable case
    round_info = models.CharField(max_length=50, choices=ROUND_CHOICES)

    def __str__(self):
        return f"{self.team1} vs {self.team2} on {self.date}"


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    youtube_link = models.URLField(blank=True, null=True)
    twitch_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    sports = models.ManyToManyField(Sport)
    times_participated = models.PositiveIntegerField(default=0)  # Renamed field to maintain consistency
    times_won = models.PositiveIntegerField(default=0)
    earnings = models.PositiveIntegerField(default=0)
    

    def __str__(self):
        return str(self.user)  # Return username




class History(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    ended_at = models.DateTimeField(auto_now_add=True)
    winners = models.ManyToManyField(User)  # Allow multiple winners for team-based tournaments

    def __str__(self):
        return f"History of {self.tournament}"


class Spouncer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    amount = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Spouncer, self).save(*args, **kwargs)

    def __str__(self):
        return self.name  # Return name instead of slug
