class LastGame():
    def __init__(self, currTeam, score):
        self.__currTeam = currTeam
        self.__score = score
        self.formatScoreFirst = self.makeFormatScore(score[0])
        self.formatScoreSec = self.makeFormatScore(score[1])
        print(score)
        pass

    def makeFormatScore(self, score):
        scoreSplit = score.split()
        resList = list()
        for oneElemScore in scoreSplit:
            try:
                resList.append(int(oneElemScore))
            except:
                pass
        if len(resList) >= 5:
            return resList
        else:
            return False

    def isCleanScore(self, isFirstTeam):
        i = 1
        countWin = 0
        while i < len(self.formatScoreFirst):
            if isFirstTeam and self.formatScoreFirst[i] > self.formatScoreSec[i]:
                countWin += 1
            elif not isFirstTeam and self.formatScoreSec[i] > self.formatScoreFirst[i]:
                countWin += 1
            else:
                return False
            i += 1
        if countWin >= 4:
            return True
        else:
            return False