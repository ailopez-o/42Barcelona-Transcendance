from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.login_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('game/new/', views.new_game_view, name='new_game'),
    path('game/<int:game_id>/', views.game_detail_view, name='game_detail'),
    path('game/game-result/', views.game_result_view, name='game_result'),
    path('tournament/new/', views.new_tournament_view, name='new_tournament'),
    path('tournament/<int:tournament_id>/', views.tournament_detail_view, name='tournament_detail'),
    path('game/<int:game_id>/accept/', views.accept_game_view, name='accept_game'),
    path('game/<int:game_id>/reject/', views.reject_game_view, name='reject_game'),
    path('global_chat/', views.global_chat_view, name='global_chat'),
    path('users/', views.users_list_view, name='users'),
    path('game_results/', views.game_results_list_view, name='game_results'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
