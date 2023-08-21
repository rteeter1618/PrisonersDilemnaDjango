
from games.gameUtils.RoundInfo import RoundResultInfo


class PayoffCalculator:
    def __init__(self, myPayoff, theirPayoff, stringToPayoffMap) -> None:
        self.myPayoffGrid = myPayoff
        self.theirPayoffGrid = theirPayoff
        self.stringToPayoffMap = stringToPayoffMap
    
    def getRoundInfos(self, myMove, theirMove):
        myIntMove = self.stringToPayoffMap[myMove]
        theirIntMove = self.stringToPayoffMap[theirMove]
        

        myPayoff = self.myPayoffGrid[myIntMove][theirIntMove]
        theirPayoff = self.theirPayoffGrid[myIntMove][theirIntMove]

        roundInfos = [
            RoundResultInfo(myPayoff, myMove),
            RoundResultInfo(theirPayoff, theirMove)
        ]
        return roundInfos


