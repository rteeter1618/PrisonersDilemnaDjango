from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from games.gameUtils.MatchManager import MatchManager
from games.gameUtils.ViewProcessor import ViewProcessor
from games.gameUtils.payoffCalculator import TwoPlayerPayoffCalculator

from games.models import Game, MatchSummary, Player




def addPlayerUpdater(request, game_id):
    code = request.POST["code"]
    playerName = request.POST['playerName']
    player = Player(user=request.user, strategy=code, name=playerName, game=Game.objects.get(pk=game_id))
    player.save()
    player.getNextMove([], [])

    return HttpResponseRedirect(reverse("games:gameHome", args=[game_id]))

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

def matchDetail(request, match_id):
    context = ViewProcessor.matchDetailContext(match_id)
    
    template_name = 'games/matchDetail.html'
    return render(request, template_name, context)

def playRounds(request, pk):
    player = get_object_or_404(Player, id=pk)
    payoffCalculator = player.game.getPayoffCalculator()
    matchManager = MatchManager(player, payoffCalculator)
    matchManager.playRounds(10, 10, Player.objects.filter(game=player.game))
    print("DONE")
    return HttpResponseRedirect(reverse("games:playerDetail", args=[pk]))

def leaderboard(request, game_id):
    game = Game.objects.get(pk=game_id)
    players = game.players.order_by("-points_per_round")
    myPlayers = game.players.filter(user=request.user)
    context = {"game": game,
               "players":players,
               "myPlayers":myPlayers}
    return render(request, "games/leaderboard.html", context)