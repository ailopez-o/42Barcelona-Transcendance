from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    total_games = models.PositiveIntegerField(default=0)
    total_wins = models.PositiveIntegerField(default=0)
    total_losses = models.PositiveIntegerField(default=0)
    tournaments_won = models.PositiveIntegerField(default=0)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  # Cambiar el nombre de la relación inversa
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # Cambiar el nombre de la relación inversa
        blank=True
    )

    def __str__(self):
        return self.username

class Game(models.Model):
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_as_player1')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_as_player2')
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='games_won')
    score_player1 = models.PositiveIntegerField(default=0)
    score_player2 = models.PositiveIntegerField(default=0)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_remote = models.BooleanField(default=False)  # Partida en remoto o local

    def __str__(self):
        return f"Partida {self.id}: {self.player1} vs {self.player2}"


class GameEvent(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='events')
    timestamp = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=50)  # Ejemplo: "goal", "pause", "disconnect"
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Evento {self.event_type} en partida {self.game.id}"


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tournaments')
    participants = models.ManyToManyField(User, related_name='tournaments')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('ongoing', 'Ongoing'), ('completed', 'Completed')], default='pending')

    def __str__(self):
        return self.name


class TournamentGame(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='games')
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    round_number = models.PositiveIntegerField()

    def __str__(self):
        return f"Juego de torneo {self.tournament.name}, Ronda {self.round_number}"


class RemoteGameSession(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE, related_name='remote_session')
    player_connected = models.ManyToManyField(User, related_name='remote_sessions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sesión remota para partida {self.game.id}"






