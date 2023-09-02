from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from games.gameUtils.MatchManager import MatchManager
from games.gameUtils.payoffCalculator import TwoPlayerPayoffCalculator

from games.models import Game, MatchSummary, Player




def addPlayerUpdater(request):
    code = request.POST["code"]
    playerName = request.POST['playerName']
    player = Player(user=request.user, strategy=code, name=playerName)
    player.save()
    player.getNextMove([], [])

    return HttpResponseRedirect(reverse("home"))

def gameHome(request, game_id):
    players = request.user.players.filter(game=game_id)
    return render(request, "games/gameHome.html",
        {"game_id": game_id,
         "players": players,
         "game": Game.objects.get(pk=game_id)})

def createNewPlayer(request, game_id):
    return render(request, "games/createPlayer.html", {"game_id":game_id})

class playerDetail(generic.DetailView):
    #This code was used to delete match history when refactored
#     allObjs = MatchSummary.objects.all()
#     for obj in allObjs:
#         obj.delete()
    model = Player
    template_name = "games/playerDetail.html"

def playRounds(request, pk):
    player = get_object_or_404(Player, id=pk)
    # "I" choose the rows
    myPayMatrix = [
        #C  D
        [3, 0], #C
        [5, 1]  #D
    ]
    theirPayMatrix = [
        [3, 5],
        [0, 1]
    ]
    stringToPayoffMap = {}
    stringToPayoffMap['C'] = 0
    stringToPayoffMap['D'] = 1
    payoffCalculator = TwoPlayerPayoffCalculator(myPayMatrix, theirPayMatrix, stringToPayoffMap)
    matchManager = MatchManager(player, payoffCalculator)
    matchManager.playRounds(10, 10, Player.objects.all())
    print("DONE")
    return HttpResponseRedirect(reverse("games:playerDetail", args=[pk]))