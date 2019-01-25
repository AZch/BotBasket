def findSendGame(elemFindTeam, lstSendGame):
    elemFind = elemFindTeam.split('|')
    for sGame in lstSendGame:
        if sGame.elemFind == elemFind[0]:
            if (elemFind[1] == 'Home'):
                return sGame.report(True)
            else:
                return sGame.report(False)
    return "not found"

def getScoreAllGame(lstGame):
    resStr = ""
    for game in lstGame:
        resStr += game.report() + "\n"
    return resStr