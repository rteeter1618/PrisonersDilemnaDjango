

import random

from games.models import MatchSummary, PlayerPointPair, RoundData


class MatchManager:

    def __init__(self, player, payoffCalculator) -> None:
        self.player = player
        self.payoffCalculator = payoffCalculator
    
    def playRounds(self, numGames, numRounds, playerPool):
        #play all players an equal number of times
        while(numGames > len(playerPool)):
            for opponent in playerPool:
                self.playMatch(opponent, numRounds)
            numGames -= len(playerPool)
        
        #some random matches at the end
        while(numGames > 0):
            self.playMatch(random.choice(playerPool), numRounds)
            numGames -= 1
    
    def playMatch(self, opponent, numRounds):
        
        matchHistory = MatchSummary()
        matchHistory.save()
        matchHistory.players.add(self.player, opponent)
        theirMoves = []
        myMoves = []
        while(numRounds > 0):
            roundData = RoundData(match=matchHistory)
            roundData.save()

            myMove = self.player.getNextMove(theirMoves, myMoves)
            theirMove = opponent.getNextMove(theirMoves, myMoves)
            myMoves.append(myMove)
            theirMoves.append(theirMove)
            
            # print(numRounds)
            # print(opponent.name)
            # print(myMove)
            # print(theirMove)
            # print("-")

            roundInfos = self.payoffCalculator.getRoundInfos(myMove, theirMove)

            playerPointPair1 = PlayerPointPair(round=roundData, player = self.player, points = roundInfos[0].myPayoff, move = roundInfos[0].myMove)
            playerPointPair2 = PlayerPointPair(round=roundData, player = opponent, points = roundInfos[1].myPayoff, move = roundInfos[1].myMove)
            playerPointPair1.save()
            playerPointPair2.save()
            roundData.save()
            
            self.player.updateStats(roundInfos[0])
            opponent.updateStats(roundInfos[1])

            numRounds -= 1
        matchHistory.save()


