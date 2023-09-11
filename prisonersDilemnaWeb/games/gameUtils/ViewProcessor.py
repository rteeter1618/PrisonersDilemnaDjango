from games.models import MatchSummary


class ViewProcessor:
    def matchDetailContext(game_id):
        match = MatchSummary.objects.get(pk=game_id)
        #p1      p2 p3..
        #ppplist...
        #||
        #\/
        playersOrderMap = {}
        playerPointPairs = []
        # filling up player map so we know all positions,
        #  initializing player point pair with correct number of inner lists
        for idx, player in enumerate(match.players.all()):
            playersOrderMap [player] = idx
            playerPointPairs.append([])
        
        for round in match.rounds.all():
            #each round has one player point pair for each player
            for playerPointPair in round.playerPointPairs.all():
                curPlayer = playerPointPair.player
                playerPos = playersOrderMap[curPlayer]
                playerPointPairs[playerPos].append(playerPointPair)
        
        #transposing the 2d list so that each row contains 
        finalPairs = []
        for i in range(0, len(playerPointPairs[0])):
            roundI=[]
            for pairList in playerPointPairs:
                roundI.append(pairList[i])
            finalPairs.append(roundI)
        
        context = {
            "roundData":finalPairs,
            "match":match,
            "players":match.players.all()
        }
        return context