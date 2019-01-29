class LastGame():
    def __init__(self, currTeam, score):
        self.__currTeam = currTeam
        self.__score = score
        self.scoreF = score[0]
        self.scoreS = score[1]
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

    def getLstQuats(self, isFirstTeam, scoresByQuatr):
        i = 1
        countWin = 0
        while i < len(self.formatScoreFirst) and i < 5:
            if isFirstTeam and self.formatScoreFirst[i] > self.formatScoreSec[i]:
                countWin += 1
            elif not isFirstTeam and self.formatScoreSec[i] > self.formatScoreFirst[i]:
                countWin += 1
            else:
                scoresByQuatr[i - 1] = scoresByQuatr[i - 1] + 1
                return scoresByQuatr
            i += 1
        return scoresByQuatr


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