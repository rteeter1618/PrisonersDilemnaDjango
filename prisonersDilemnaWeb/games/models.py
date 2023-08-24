from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
import random

from RestrictedPython import compile_restricted, safe_builtins, safe_globals
#from RestrictedPython.Guards import __getitem__
#from RestrictedPython import set_policy





# Create your models here.


class Player(models.Model):
    name=models.TextField(max_length=100, default="default")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    strategy = models.TextField(default="default")
    points = models.IntegerField(default=0)
    rounds_played = models.IntegerField(default=0)
    points_per_round = models.FloatField(default=0)
    #timesC = models.IntegerField(default=0)
    #timesD = models.IntegerField(default=0)
    #history = models.ExpressionList()

    def updateStats(self, myRoundInfo):
        self.points = F("points") + myRoundInfo.myPayoff
        self.rounds_played = F("rounds_played") + 1
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



