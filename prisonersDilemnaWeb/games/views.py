from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from games.models import Player




def addPlayerUpdater(request):
    code = request.POST["code"]
    playerName = request.POST['playerName']
    player = Player(user=request.user, strategy=code, name=playerName)
    player.save()
    player.getNextMove([], [])

    return HttpResponseRedirect(reverse("home"))

def createNewPlayer(request):
    return render(request, "games/createPlayer.html", {})