from django.db import models
from django.contrib.auth.models import User

from RestrictedPython import compile_restricted, safe_builtins

# Create your models here.


class Player(models.Model):
    name=models.TextField(max_length=100, default="default")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    strategy = models.TextField(default="default")
    points = models.IntegerField(default=0)
    rounds_played = models.IntegerField(default=0)
    pointsPerRound = models.FloatField(default=0)
    timesC = models.IntegerField(default=0)
    timesD = models.IntegerField(default=0)

    def getNextMove(self, theirPrevMoves, myPrevMoves):
        # Add the custom import function to the safe builtins
        safe_builtins['__import__'] = _import

        # Define the source code to be executed
        source_code = self.strategy

        # Compile the source code in restricted mode
        byte_code = compile_restricted(source_code, '<string>', 'exec')

        # Define the global and local variables for the execution
        global_vars = {'__builtins__': safe_builtins}
        local_vars = {}

        # Execute the compiled code
        exec(byte_code, global_vars, local_vars)

        # Retrieve the result from the local variables
        function = local_vars['nextMove']


        print(function(theirPrevMoves, myPrevMoves))




# Define a custom function to allow importing only specific modules
def _import(name, globals=None, locals=None, fromlist=(), level=0):
    allowed_modules = ['math']
    if name in allowed_modules:
        return __import__(name, globals, locals, fromlist, level)
    else:
        raise ImportError(f'Importing module {name} is not allowed')


