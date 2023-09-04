from django.urls import path

from . import views

app_name='games'

urlpatterns = [
    #creates new player and adds to database, no webpage
    path("addPlayerUpdater/<int:game_id>", views.addPlayerUpdater, name="addPlayerUpdater"),
    #The creation page editor for a new player
    path("createNewPlayer/<int:game_id>", views.createNewPlayer, name="createNewPlayer"),
    #Player statistics
    path("playerDetail/<int:pk>", views.playerDetail.as_view(), name="playerDetail"),
    #Match details, shows all moves frome ach player
    path("matchDetail/<int:match_id>", views.matchDetail, name="matchDetail"),
    #simulates rounds against other players, no webpage
    path("playRounds/<int:pk>", views.playRounds, name="playRounds"),
    #Home page for a specific game
    path("gameHome/<int:game_id>", views.gameHome, name="gameHome"),
    #leaderBoard
    path("leaderboard/<int:game_id>", views.leaderboard, name="leaderboard"),
]