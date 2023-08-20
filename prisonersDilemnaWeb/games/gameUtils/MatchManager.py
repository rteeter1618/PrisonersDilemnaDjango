

import random


class MatchManager:

    def __init__(self, player, payoffCalculator) -> None:
        self.player = player
        self.payoffCalculator = payoffCalculator
    
    def playRounds(self, numGames, numRounds, playerPool):
        #play all players an equal number of times
        while(numGames > len(playerPool)):
            for opponent in playerPool:
                self.playMatch(opponent, numRounds)
            numRounds -= len(playerPool)
        
        #some random matches at the end
        while(numGames > 0):
            self.playMatch(random.choice(playerPool), numRounds)
            numGames -= 1
    
    def playMatch(self, opponent, numRounds):
        theirMoves = []
        myMoves = []
        while(numRounds > 0):
            myMove = self.player.getNextMove()
            myMoves.append(myMove)
            theirMove = opponent.getNextMove()
            theirMoves.append(theirMove)


            payoffs = self.payoffCalculator.getPayoffs([myMove, theirMove])
            self.player.updateStats
            numRounds -= 1


