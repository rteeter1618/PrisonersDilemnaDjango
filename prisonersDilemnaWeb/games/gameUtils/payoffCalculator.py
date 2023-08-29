


class TwoPlayerPayoffCalculator:
    def __init__(self, myPayoff, theirPayoff, stringToPayoffMap) -> None:
        self.myPayoffGrid = myPayoff
        self.theirPayoffGrid = theirPayoff
        self.stringToPayoffMap = stringToPayoffMap
    
    def getPayoffs(self, moves):
        myMove = moves[0]
        theirMove = moves[1]

        myIntMove = self.stringToPayoffMap[myMove]
        theirIntMove = self.stringToPayoffMap[theirMove]
        

        myPayoff = self.myPayoffGrid[myIntMove][theirIntMove]
        theirPayoff = self.theirPayoffGrid[myIntMove][theirIntMove]

        return [myPayoff, theirPayoff]


