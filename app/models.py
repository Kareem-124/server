from django.db import models
import re

# Create your models here.

class Validation(models.Manager):
    # Registration Validation
    def validate(self, data):
        error = {}
        get_emails = User.objects.all()
        if len(data['user_name']) < 2 :
            error['user_name'] = "User Name should be at least 2 characters"
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(data['email']):    # test whether a field matches the pattern            
            error['email'] = "Invalid email address!"
        
        for user in get_emails:
            if data['email'] == user.email:
                error['email_exists'] = "This Email Address already exists!"
        
        if data['password'] != data['conf_password']:
            error['password_conf'] = "Password and Password Confirmation should Match!"
        
        if len(data['password']) < 8 :
            error['password'] = "Password Must be at least 8 characters"
        return error
    
    def validate_team(self,data):
        error = {}
        days_list = ['saturday','sunday','monday','tuesday','wednesday','thursday','friday']
        day_found = False
        if len(data['team_name']) < 2 :
            error['team_name'] = "Team Name should be at least 2 characters"
        # Skill Level Validation 
        if len(data['skill_level']) < 1:
            error['skill_level_empty'] = "Skill level field is required"
        elif int(data['skill_level']) > 5 or int(data['skill_level']) <= 0:
            error['skill_level_range'] = "Skill level must be between 1 and 5"
        
        game_day = data['game_day'].lower()
        for day in days_list:
            if game_day == day:
                day_found = True
                break
        if not day_found :
            error['game_day'] = "Please enter a valid day name"
        return error
    
    def validate_player(self,data, team_id):
        error = {}
        if len(data['player_name']) < 2 :
            error['player_name'] = "Player Name should be at least 2 characters"
        team = Team.objects.get(id = team_id)
        if team.players.all().count() >= 9:
            error['player_number'] = "Only 9 Player at Maximum"
        return error



class User(models.Model):
    user_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    # teams 
    objects = Validation()

class Team(models.Model):
    team_name = models.CharField(max_length=100)
    skill_level = models.SmallIntegerField()
    game_day=models.CharField(max_length=12)
    user = models.ForeignKey(User, related_name='teams',on_delete=models.CASCADE )
    objects = Validation()
    # players

class player(models.Model):
    player_name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, related_name='players',on_delete=models.CASCADE )
    objects = Validation()