from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import Game, Tournament
from django.http import JsonResponse

# Obtener el modelo de usuario configurado en AUTH_USER_MODEL
User = get_user_model()

# Vista para login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Vista para registro
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Vista del perfil del usuario
@login_required
def profile_view(request):
    user = request.user
    games = Game.objects.filter(player1=user) | Game.objects.filter(player2=user)
    return render(request, 'profile.html', {
        'user': user,
        'games': games
    })

# Vista para crear una nueva partida
@login_required
def new_game_view(request):
    if request.method == 'POST':
        opponent_id = request.POST.get('opponent')
        opponent = get_object_or_404(User, id=opponent_id)
        game = Game.objects.create(player1=request.user, player2=opponent)
        return redirect('game_detail', game_id=game.id)

    users = User.objects.exclude(id=request.user.id)  # Lista de jugadores, excluyendo al usuario actual
    return render(request, 'game.html', {'users': users})

# Vista para el detalle de una partida
@login_required
def game_detail_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, 'game_detail.html', {'game': game})

# Vista para crear un nuevo torneo
@login_required
def new_tournament_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        participants_ids = request.POST.getlist('participants')
        participants = User.objects.filter(id__in=participants_ids)

        tournament = Tournament.objects.create(
            name=name,
            created_by=request.user
        )
        tournament.participants.set(participants)
        return redirect('tournament_detail', tournament_id=tournament.id)

    users = User.objects.exclude(id=request.user.id)
    return render(request, 'tournament.html', {'users': users})

# Vista para el detalle de un torneo
@login_required
def tournament_detail_view(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    return render(request, 'tournament_detail.html', {'tournament': tournament})
