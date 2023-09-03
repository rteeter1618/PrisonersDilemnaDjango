


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


class PayoffCalculatorData:
    def getPayoffCalculator(self, game_id):
        #Prisoners Dilemma
        if(game_id == 1):
            # "I" choose the rows
            myPayMatrix = [
                #C  D
                [3, 0], #C
                [5, 1]  #D
            ]
            theirPayMatrix = [
                [3, 5],
                [0, 1]
            ]
            stringToPayoffMap = {}
            stringToPayoffMap['C'] = 0
            stringToPayoffMap['D'] = 1
            return TwoPlayerPayoffCalculator(myPayMatrix, theirPayMatrix, stringToPayoffMap)
        #Chicken
        elif(game_id == 2):
            # "I" choose the rows
            myPayMatrix = [
                #S  D
                [3, 1], #S
                [5, 0]  #D
            ]
            theirPayMatrix = [
                [3, 5],
                [1, 0]
            ]
            stringToPayoffMap = {}
            stringToPayoffMap['S'] = 0
            stringToPayoffMap['D'] = 1
            return TwoPlayerPayoffCalculator(myPayMatrix, theirPayMatrix, stringToPayoffMap)
    


