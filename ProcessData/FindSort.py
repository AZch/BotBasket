def findSendGame(elemFindTeam, lstSendGame):
    elemFind = elemFindTeam.split('|')
    for sGame in lstSendGame:
        if sGame.elemFind == elemFind[0]:
            if elemFind[1] == 'Home':
                return sGame.report(1)
            elif elemFind[1] == 'Away':
                return sGame.report(2)
            elif elemFind[1] == 'Anal':
                return sGame.report(0)
    return "not found"

def findSendLink(elemFind, lstSendGame):
    for sGame in lstSendGame:
        if sGame.elemFind == elemFind[0]:
            return sGame.link

def getScoreAllGame(lstGame):
    resStr = ""
    for game in lstGame:
        resStr += game.report() + "\n"
    return resStr