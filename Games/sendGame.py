import time

class sendGame():
    def __init__(self, lstHome, lstAway, ks, elemFind, link):
        self.lstHome = lstHome
        self.lstAway = lstAway
        self.kf = ks
        self.startTime = time.time()
        self.elemFind = elemFind
        self.link = link

    def checkEndTime(self):
        if time.time() - self.startTime > self.startTime + 60 * 10:
            return True
        else:
            return False
    # (I)[(1)12 - 24(2)] (II)
    # 0 быстрая аналитика
    # 1 игры дома
    # 2 игры гости
    def report(self, flagParse):
        if flagParse == 0:
            firstStat = "N"
            secStat = "N"
            isFirst = False
            if self.kf[0] > self.kf[1]:
                firstStat = "[OUT] " + str(self.kf[0])
                secStat = "[FAV] " + str(self.kf[1])
                isFirst = False
            else:
                firstStat = "[FAV] " + str(self.kf[0])
                secStat = "[OUT] " + str(self.kf[1])
                isFirst = True
            scoreQuatFirst = [0] * 4
            scoreQuatSec = [0] * 4
            for i in range(len(self.lstHome)):
                scoreQuatFirst = self.lstHome[i].getLstQuats(isFirstTeam=isFirst, scoresByQuatr=scoreQuatFirst)
                scoreQuatSec = self.lstAway[i].getLstQuats(isFirstTeam=isFirst, scoresByQuatr=scoreQuatSec)
            return firstStat + "\n" + ' '.join(str(num) for num in scoreQuatFirst) + "\n" + \
                  ' '.join(str(num) for num in scoreQuatSec) + "\n" + secStat + "\n (в какой четверти вин)"


        count = 1
        if self.kf[0] > self.kf[1]:
            if flagParse == 1:
                res = "Фаварит " + str(self.kf[0]) + "\n"
            else:
                res = "Аутсайдер " + str(self.kf[1]) + "\n"
        else:
            if not flagParse == 1:
                res = "Фаварит " + str(self.kf[1]) + "\n"
            else:
                res = "Аутсайдер " + str(self.kf[0]) + "\n"
        res = ""
        if flagParse == 1:
            for game in self.lstHome:
                res += ' '.join(str(num) for num in game.formatScoreFirst) + "\n" + ' '.join(str(num) for num in game.formatScoreSec) + "\n---\n"
        else:
            for game in self.lstAway:
                res += ' '.join(str(num) for num in game.formatScoreFirst) + "\n" + ' '.join(
                    str(num) for num in game.formatScoreSec) + "\n---\n"
        return res


