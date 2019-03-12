import datetime
from WorkWithTG import SendMsg

class Game():
    def __init__(self, timeMin, teams, ligue, idOnPage, day, month, elemFind, dayFind):
        self.__timeMin = timeMin
        #elemFind = elemFind.split('\'')[0]
        #print(elemFind)
        self.hours = teams.split(' ')[0]
        teamsName = teams.replace(self.hours, '')
        self.teams = self.hours + " " + teamsName.replace(' ', '')
        self.teams = self.teams.replace('-', '     ')
        self.teamHome = self.teams.split('     ')[0]
        self.teamHome = self.teamHome.replace(self.hours + " ", '')
        self.teamAway = self.teams.split('     ')[1]
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
        self.currURL = "https://www.soccerstand.com/basketball/"
        self.elemFind = elemFind
        self.dayFind = dayFind
        self.isAppendData = False
        self.isValdateData = False
        self.isSendData = False
        self.isCheck = False

    def isPrint(self):
        return self.print

    def setPrint(self):
        self.print = True

    def setLastUpdate(self):
        self.isLastUpdate = True

    def checkLastUpdate(self):
        return self.isLastUpdate

    def gameIsAppendData(self):
        return self.isAppendDAta

    def isValidData(self):
        return self.isValidateData

    def checkTime(self, timePrint = 27):
        minNow = datetime.datetime.now().hour * 60 + datetime.datetime.now().minute
        check1 = datetime.datetime.now().day
        check2 = self.day
        check3 = self.__timeMin - minNow
        if self.__timeMin - minNow <= timePrint and datetime.datetime.now().day == self.day:
            return True
        else:
            return False

    def checkTimeAfter(self):
        minNow = datetime.datetime.now().hour * 60 + datetime.datetime.now().minute
        check1 = datetime.datetime.now().day
        check2 = self.day
        check3 = self.__timeMin - minNow
        if self.__timeMin - minNow < 0 and datetime.datetime.now().day == self.day:
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
            if (self.teamAway == 'IllawarraHawks' or self.teamAway == 'SonicBoom' or self.teamAway == 'TecnycontaZaragoza' or self.teamAway == 'BarcelonaB'):
                SendMsg.sendSimpleMsg(chatId=281265894, text=self.report())
                SendMsg.sendSimpleMsg(chatId=281265894, text='bad team zaragoza, barcelona')
                return False
            if (self.teamHome == 'IllawarraHawks' or self.teamHome == 'SonicBoom' or self.teamHome == 'TecnycontaZaragoza' or self.teamHome == 'BarcelonaB'):
                SendMsg.sendSimpleMsg(chatId=281265894, text=self.report())
                SendMsg.sendSimpleMsg(chatId=281265894, text='bad team zaragoza, barcelona')
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
        try:
            if self.kf[0] > self.kf[1]:
                resPrint = 'Фора на ' + self.teamHome + ' в четвертях'
            else:
                resPrint = 'Фора на ' + self.teamAway + ' в четвертях'
        except:
            resPrint = ""
        return str(self.day) + "." + str(self.month) + " в " + self.hours + "\n" + self.ligue + "\n" + self.teamHome + " - " + self.teamAway + "\n" + resPrint