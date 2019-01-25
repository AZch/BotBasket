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
                res += game.scoreF + "\n" + game.scoreS + "\n"
        else:
            for game in self.lstAway:
                res += game.scoreF + "\n" + game.scoreS + "\n"
        return res


