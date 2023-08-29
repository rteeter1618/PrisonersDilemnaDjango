from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
import random

from RestrictedPython import compile_restricted, safe_builtins, safe_globals
#from RestrictedPython.Guards import __getitem__
#from RestrictedPython import set_policy




class Game(models.Model):
    name = models.TextField()


# Create your models here.

class Player(models.Model):
    name = models.TextField(max_length=100, default="default")
    user = models.ForeignKey(User, related_name="players", on_delete=models.CASCADE)
    strategy = models.TextField(default="default")
    points = models.IntegerField(default=0)
    rounds_played = models.IntegerField(default=0)
    points_per_round = models.FloatField(default=0)
    game = models.ForeignKey(Game, related_name= 'players', on_delete=models.CASCADE)

    def updateStats(self, matchSummary):

        self.points = F("points") + matchSummary.getTotalPoints(self)
        self.rounds_played = F("rounds_played") + len(matchSummary.rounds.all())
        self.points_per_round = F("points") / F("rounds_played")
        self.save()
        self.refresh_from_db()
        num = self.points / self.rounds_played
        self.points_per_round = (self.points / self.rounds_played)
        self.save()

        

    def getNextMove(self, theirPrevMoves, myPrevMoves):
        #set_policy(lambda obj, item: True)
        # Add the custom import function to the safe builtins
        safe_builtins['__import__'] = _import
        safe_builtins['_getitem_'] = _getitem_
        #safe_globals['_getitem_'] = guarded_getitem
        #safe_globals['__builtins__'] = safe_builtins
        

        # Define the source code to be executed
        source_code = self.strategy

        # Compile the source code in restricted mode
        byte_code = compile_restricted(source_code, '<string>', 'exec')

        # Define the global and local variables for the execution
        global_vars = {'__builtins__': safe_builtins, 'random': random}
        local_vars = {}

        # Execute the compiled code# Execute the compiled code
        try:
            exec(byte_code, global_vars, local_vars)
        except Exception as e:
            print(f'Error: {e}')

        

        # Retrieve the result from the local variables
        function = local_vars['nextMove']


        return function(theirPrevMoves, myPrevMoves)


# Define a custom function to allow importing only specific modules
def _import(name, globals=None, locals=None, fromlist=(), level=0):
    allowed_modules = ['math', 'random']
    if name in allowed_modules:
        #print(name)
        return __import__(name, globals, locals, fromlist, level)
    else:
        raise ImportError(f'Importing module {name} is not allowed')

def _getitem_(obj, item):
  return obj[item]



#a match is made up of many rounds
class MatchSummary(models.Model):
    players = models.ManyToManyField(Player, related_name='matches')

    #gets the total amount of points scored by the given player in the match

    def getTotalPoints(self, player):
        total = 0
        for round in self.rounds.all():
            for playerPointPair in round.playerPointPairs.all():
                if(player == playerPointPair.player):
                    total += playerPointPair.points
        return total

#a round consists of each player playing a certain move and scoring a certain number of points   
class RoundData(models.Model):
    match = models.ForeignKey(MatchSummary, related_name='rounds', on_delete=models.CASCADE)

class PlayerPointPair(models.Model):
    round = models.ForeignKey(RoundData, related_name='playerPointPairs', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    move = models.TextField()

