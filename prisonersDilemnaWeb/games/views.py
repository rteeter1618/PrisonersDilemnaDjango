from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from games.gameUtils.MatchManager import MatchManager
from games.gameUtils.payoffCalculator import PayoffCalculator

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

class playerDetail(generic.DetailView):
    model = Player
    template_name = "games/playerDetail.html"

def playRounds(request, pk):
    player = get_object_or_404(Player, id=pk)
    payoffCalculator = PayoffCalculator()
    matchManager = MatchManager(player)
    matchManager.playRounds(10, Player.objects.all)
    return HttpResponseRedirect(reverse("games:playerDetail", args=[pk]))