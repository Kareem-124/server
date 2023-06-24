from django.shortcuts import render, redirect
from app.models import *
from django.contrib import messages
import bcrypt

# Page : Login Page
def index(request):
    return render(request, 'index.html')

# Process: Registration Process: Validation Included
def reg_process(request):
    # Validation Part Section
    error = User.objects.validate(request.POST)
    if len(error) > 0:
        for key, value in error.items():
            messages.error(request, value)
        return redirect('/')
    else:  # if Validation passed store the user in the db and encrypt the password
        password = request.POST['password']
        ps_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(
            user_name=request.POST['user_name'], email=request.POST['email'], password=ps_hash
        )
        messages.success(request, "User has been created Successfully!")
        return redirect('/')
    

# Process: Login Process: Validation Included
def login_process(request):
    # see if the username provided exists in the database
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            # if we get True after checking the password, we may put the user id in session
            request.session['user_id'] = logged_user.id
            messages.success(request, "You have Successfully logged in")
            return redirect('/home')
        else:
            # if we didn't find anything in the database by searching by username or if the passwords don't match,
            messages.error(request, "Email or Password incorrect")
            return redirect('/')
    else:
        # if we didn't find anything in the database by searching by username or if the passwords don't match,
        messages.error(request, "Email or Password incorrect")
        return redirect('/')
    
# : This will clear the massages from messages (error / success) --> redirect to /success
def success_redirect_process(request):
    list(messages.get_messages(request))
    return redirect('/home')

# Page : Open The main page after the user successfully logged in, it will open ""
def success(request):
    # Create User Session
    user = User.objects.get(id=request.session['user_id'])
    team = Team.objects.all()
    context = {
        'user_object' : user,
        'team_object' :team,
        'user_session' : request.session['user_id'],
    }
    return render(request, 'home.html', context)


# Process : Logout
def logout_process(request):
    # This will clear the massages from messages (error / success)
    list(messages.get_messages(request))
    request.session.flush()
    return redirect('/')

# Page : table
def table(request):
    return render(request,'table.html')


# Page : form
def form(request):
    return render(request,'form.html')

def new_team_redirect_process(request):
    list(messages.get_messages(request))
    return redirect('/team/new')
# Page : new_team
def new_team(request):
    return render(request,'new_team.html')

def create_new_team_process(request):
    error = Team.objects.validate_team(request.POST)
    if len(error) > 0:
        for key, value in error.items():
            messages.error(request, value)
        return redirect('/team/new')
    else:  # if Validation passed store the team in the db and encrypt the password
        user = User.objects.get(id = request.session['user_id'])
        Team.objects.create(
            team_name=request.POST['team_name'], skill_level=request.POST['skill_level'], game_day=request.POST['game_day'].capitalize(),user = user
        )
        return redirect('/success_redirect_process')
    

# Page : Team Details
def team_details(request, id):
    user = User.objects.get(id = request.session['user_id'])
    team = Team.objects.get(id = id)
    player_obj = team.players.all()
    print(player_obj)
    context = {
        'current_user' : user,
        'team_object' : team,
        'player_object' : player_obj,
        'user_session' : request.session['user_id'],

    }
    return render(request,'team_details.html',context)


def edit_new_team_process(request,team_id):
    error = Team.objects.validate_team(request.POST)
    if len(error) > 0:
        for key, value in error.items():
            messages.error(request, value)
        return redirect('/team/' + str(team_id) + '/edit')

    team = Team.objects.get(id = team_id)
    team.team_name = request.POST['team_name']
    team.skill_level = request.POST['skill_level']
    team.game_day = request.POST['game_day']
    team.save()

    return redirect('/success_redirect_process')


def delete_team(request,team_id):
    team = Team.objects.get(id=team_id)
    team.delete()
    return redirect ('/success_redirect_process')


def team_edit(request,team_id):
    user = User.objects.get(id = request.session['user_id'])
    team = Team.objects.get(id = team_id)

    context = {
        'current_user' : user,
        'team_object' : team,
        'user_session' : request.session['user_id']

    }
    return render(request,'team_edit.html',context)

def add_player_process(request,team_id):
    error = player.objects.validate_player(request.POST,team_id)
    if len(error) > 0:
        for key, value in error.items():
            messages.error(request, value)
        return redirect('/team/' + str(team_id))
    team = Team.objects.get(id = team_id)
    player.objects.create(player_name = request.POST['player_name'],team = team)
    return redirect('/team/' + str(team_id))