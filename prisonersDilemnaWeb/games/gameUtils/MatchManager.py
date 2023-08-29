

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
                if(opponent != self.player):
                    self.playMatch(opponent, numRounds)
                    numGames -= 1
        
        #some random matches at the end
        while(numGames > 0):
            opponent = random.choice(playerPool)
            if(opponent != self.player):
                self.playMatch(opponent, numRounds)
                numGames -= 1
    
    def playMatch(self, opponent, numRounds):
        #specific to 2 players
        allPlayers = [self.player, opponent]
        matchHistory = MatchSummary()
        matchHistory.save()
        matchHistory.players.add(self.player, opponent)
        allMoves = [[] for i in range(2)]
        #[
        # [myMoves]
        # [theirMoves]
        # ]
        #playing multiple rounds between the same players
        while(numRounds > 0):
            roundData = RoundData(match=matchHistory)
            roundData.save()

            #specific to 2 players
            theirMoves = allMoves[0]
            myMoves = allMoves[1]

            curMoves = [tempPlayer.getNextMove(theirMoves, myMoves) for tempPlayer in allPlayers]
            myMove = self.player.getNextMove(theirMoves, myMoves)
            theirMove = opponent.getNextMove(theirMoves, myMoves)
            #storing moves for later
            allMoves[0].append(myMove)
            allMoves[1].append(theirMove)

            players = [self.player, opponent]
            payoffs = self.payoffCalculator.getPayoffs([moves[-1] for moves in allMoves])

            for idx, player in enumerate(players):
                playerPointPair = PlayerPointPair(
                    round=roundData,
                    player = player,
                    points = payoffs[idx],
                    move = allMoves[idx][-1])
                playerPointPair.save()
                player.updateStats(playerPointPair)

            # playerPointPair2 = PlayerPointPair(round=roundData, player = opponent, points = roundInfos[1].myPayoff, move = roundInfos[1].myMove)
            # playerPointPair2.save()
            # roundData.save()
            
            # self.player.updateStats(roundInfos[0])
            # opponent.updateStats(roundInfos[1])

            numRounds -= 1
        matchHistory.save()


