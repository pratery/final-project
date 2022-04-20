from django.shortcuts import render, redirect, get_object_or_404
from .models import Conference, Team, Player
from .forms import ConferenceForm, TeamForm, PlayerForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create views here


# the home page
def index(request):
    return render(request, 'league/index.html')


# Show all conferences
@login_required
def conferences(request):
    conferences = Conference.objects.filter(owner=request.user).order_by("name")
    context = {"conferences": conferences}
    return render(request, "league/conferences.html", context)



# Show a single conference and all its teams
@login_required
def conference(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    if conference.owner != request.user:
        raise Http404
    teams = conference.team_set.order_by("name")
    context = {"conference": conference, "teams": teams}
    return render(request, "league/conference.html", context)


# Show all teams
@login_required
def teams(request):
    teams = Team.objects.filter(owner=request.user).order_by("name")
    context = {"teams": teams}
    return render(request, "league/teams.html", context)


# Show a single team and all players on that team
@login_required
def team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if team.owner != request.user:
        raise Http404
    players = team.player_set.order_by("name")
    context = {"team": team, "players": players}
    return render(request, 'league/team.html', context)


# Show all players in the league
@login_required
def players(request):
    players = Player.objects.filter(owner=request.user).order_by("team", "name")
    context = {"players": players}
    return render(request, "league/players.html", context)


# Show a single player
@login_required
def player(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    if player.owner != request.user:
        raise Http404
    context = {"player": player}
    return render(request, "league/player.html", context)

# Add a new conference
@login_required
def new_conference(request):
    if request.method != "POST":
        form = ConferenceForm() # create a blank form is no data is submitted
    else:
        form = ConferenceForm(data=request.POST) # else, POST data is submitted, process data
    if form.is_valid():
        new_conference = form.save(commit=False)
        new_conference.owner = request.user
        new_conference.save()
        return redirect("league:conferences")
    context = {"form": form}
    return render(request, "league/new_conference.html", context)


# Add a new team to a particular conference
@login_required
def new_team(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    if request.method != "POST":
        form = TeamForm()
    else:
        form = TeamForm(data=request.POST)
        if form.is_valid():
            new_team = form.save(commit=False)
            new_team.conference = conference
            new_team.owner = request.user
            new_team.save()
            return redirect("league:conference", conference_id=conference_id)
    context = {"conference": conference, "form": form}
    return render(request, "league/new_team.html", context)

# Add a new player to a specific team
@login_required
def new_player(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method != "POST":
        form = PlayerForm()
    else:
        form = PlayerForm(data=request.POST)
        if form.is_valid():
            new_player = form.save(commit=False)
            new_player.team = team
            new_player.owner = request.user
            new_player.save()
            return redirect("league/team.html", team_id=team_id)
    context = {"team": team, "form": form}
    return render(request, "league/new_player.html", context)


# Editing an existing conference
def edit_conference(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    if request.method != "POST":
        form = ConferenceForm(instance=conference)
    else:
        form = ConferenceForm(instance=conference, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("league:conference", conference_id=conference_id)
    context = {"conference": conference, "form": form}
    return render(request, "league/edit_conference.html", context)


# Editing an existing team
def edit_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if request.method != 'POST':
        # Initial request; pre-fill form with the current team
        form = TeamForm(instance=team)
    else:
        # POST data submitted; process data
        form = TeamForm(instance=team, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('ncaa:team', team_id=team_id)

    context = {'team': team, 'form': form}
    return render(request, 'league/edit_team.html', context)


def edit_player(request, player_id):
    """Edit an existing player"""
    player = get_object_or_404(Player, id=player_id)

    if request.method != 'POST':
        # Initial request; pre-fill form with current player
        form = PlayerForm(instance=player)
    else:
        # POST data submitted; process data
        form = PlayerForm(instance=player, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('league:player', player_id=player_id)

    context = {'player': player, 'form': form}
    return render(request, 'league/edit_player.html', context)


def delete_conference(request, pk):
    """Delete an existing conference"""
    conference = get_object_or_404(Conference, pk=pk)

    if request.method == 'POST':
        conference.delete()
        return redirect('/')

    return render(request, '/', {'conference': conference})


def delete_team(request, pk):
    """Delete an existing team"""
    team = get_object_or_404(Team, pk=pk)

    if request.method == 'POST':
        team.delete()
        return redirect('/')

    return render(request, '/', {'team': team})


def delete_player(request, pk):
    """Delete an existing player"""
    player = get_object_or_404(Player, pk=pk)

    if request.method == 'POST':
        player.delete()
        return redirect('/')

    return render(request, '/', {'player': player})

