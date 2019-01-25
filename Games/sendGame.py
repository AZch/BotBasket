import time

class sendGame():
    def __init__(self, lstHome, lstAway, ks, elemFind):
        self.lstHome = lstHome
        self.lstAway = lstAway
        self.kf = ks
        self.startTime = time.time()
        self.elemFind = elemFind

    def checkEndTime(self):
        if time.time() - self.startTime > 60 * 10:
            return True
        else:
            return False
    # (I)[(1)12 - 24(2)] (II)
    def report(self, isHome):
        # count = 1
        # if self.kf[0] > self.kf[1]:
        #     if isHome:
        #         res = "Фаварит " + str(self.kf[0]) + "\n"
        #     else:
        #         res = "Аутсайдер " + str(self.kf[1]) + "\n"
        # else:
        #     if not isHome:
        #         res = "Фаварит " + str(self.kf[1]) + "\n"
        #     else:
        #         res = "Аутсайдер " + str(self.kf[0]) + "\n"
        res = ""
        if isHome:
            for game in self.lstHome:
                res += ' '.join(str(num) for num in game.formatScoreFirst) + "\n" + ' '.join(str(num) for num in game.formatScoreSec) + "\n---"
        else:
            for game in self.lstAway:
                res += ' '.join(str(num) for num in game.formatScoreFirst) + "\n" + ' '.join(
                    str(num) for num in game.formatScoreSec) + "\n---"
        return res


