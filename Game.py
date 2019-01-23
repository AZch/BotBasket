import datetime
from LastGame import LastGame

class Game():
    def __init__(self, timeMin, teams, ligue, idOnPage, day, month):
        self.__timeMin = timeMin
        hours = teams.split(' ')[0]
        teamsName = teams.replace(hours, '')
        self.teams = hours + " " + teamsName.replace(' ', '')
        self.teams = self.teams.replace('-', '     ')
        self.teams = self.teams.strip()
        self.day = day
        self.month = month
        self.idOnPage = idOnPage

        self.lstHome = list()
        self.lstAway = list()
        self.ligue = ligue
        self.kf = list()
        self.print = False
        #self.day = 0
        self.isLastUpdate = False
        self.currURL = ""

    def isPrint(self):
        return self.print

    def setPrint(self):
        self.print = True

    def setLastUpdate(self):
        self.isLastUpdate = True

    def checkLastUpdate(self):
        return self.isLastUpdate

    def checkTime(self, timePrint = 15):
        minNow = datetime.datetime.now().hour * 60 + datetime.datetime.now().minute
        check1 = datetime.datetime.now().day
        check2 = self.day
        check3 = self.__timeMin - minNow
        if self.__timeMin - minNow <= timePrint and datetime.datetime.now().day == self.day:
            return True
        else:
            return False

    def checkGame(self, kfHome = 0, kfAway = 0, kfMin = 1.4):
        countCleanHome = 0
        countCleanAway = 0
        try:
            if self.kf != False:
                kfHome = self.kf[0]
                kfAway = self.kf[1]
            else:
                return False
            if kfHome < 1.4 or kfAway < 1.4:
                return False
            if (kfHome >= kfMin and kfHome < kfAway):
                for homeGame in self.lstHome:
                    if homeGame.isCleanScore(isFirstTeam=True):
                        countCleanHome += 1
                        return False
                for awayGame in self.lstAway:
                    if awayGame.isCleanScore(isFirstTeam=True):
                        countCleanAway += 1
                        return False
            elif (kfAway >= kfMin and kfAway < kfHome):
                for homeGame in self.lstHome:
                    if homeGame.isCleanScore(isFirstTeam=False):
                        countCleanHome += 1
                        return False
                for awayGame in self.lstAway:
                    if awayGame.isCleanScore(isFirstTeam=False):
                        countCleanAway += 1
                        return False
            else:
                return False
            if countCleanAway + countCleanHome >= 1:
                return False
            return True
        except:
            return False

    def report(self):
        return str(self.day) + "." + str(self.month) + "\n" + self.ligue + "\n" + self.teams + "\n" + str(self.kf) + "\n" + self.currURL