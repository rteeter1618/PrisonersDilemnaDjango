from django.urls import path

from . import views

app_name='games'

urlpatterns = [
    #creates new player and adds to database, no webpage
    path("addPlayerUpdater/", views.addPlayerUpdater, name="addPlayerUpdater"),
    #The creation page editor for a new player
    path("createNewPlayer/", views.createNewPlayer, name="createNewPlayer"),
    #Player statistics
    path("playerDetail/<int:pk>", views.playerDetail.as_view(), name="playerDetail"),
    #simulates rounds against other players, no webpage
    path("playRounds/<int:pk>", views.playRounds, name="playRounds")
]