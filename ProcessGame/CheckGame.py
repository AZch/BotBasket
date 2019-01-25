import time
from Constants import XPath
import traceback
from ProcessData import ParseData, ExecReq


def checkSendGame(lstSendGame):
    print('check send')
    for sGame in lstSendGame:
        if sGame.checkEndTime():
            try:
                lstSendGame.remove(sGame)
            except:
                print('Ошибка:\n', traceback.format_exc())

def checkGame(game, seasonYearStart, seasonYearEnd):
    print(game.teams)
    driver = ParseData.driverForPlayDay(game.dayFind, game.month)
    try:
        ExecReq.clickGetElem(driver, "//*[contains(text(), 'Agree')]")
        ExecReq.clickGetElem(driver, "//*[contains(text(), 'Scheduled')]")
        # elems = ExecReq.getElemsByXPath(XPath.allGame, driver)
        ExecReq.clickElem(ParseData.getElemGame(driver, game.elemFind))
        driver.switch_to.window(driver.window_handles[1])
        startTime = time.time()
        while True:
            if time.time() - startTime > 90:
                break
            if ExecReq.getElemByXPath("//*[contains(text(), 'Match Summary')]", driver) == False:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                ExecReq.clickElem(ParseData.getElemGame(driver, game.elemFind))
                driver.switch_to.window(driver.window_handles[1])
            else:
                break
        game.currURL = driver.current_url

        ''' Получение коэффициента '''
        kf = ExecReq.getKF(driver)
        if kf == False or (kf[0] < 1.4 or kf[1] < 1.4):
            raise ValueError()
        elif kf[0] > kf[1]:
            isFirstTeam = False
        elif kf[1] > kf[0]:
            isFirstTeam = True
        else:
            isFirstTeam = True
            print("kf team equel")

        ''' Получить домашние игры '''
        ExecReq.clickGetElem(driver, XPath.clickH2H)
        ExecReq.clickGetElem(driver, XPath.clickHomeGame)
        while ExecReq.clickGetElem(driver, XPath.clickMoreHomeGame):
            pass
        elem = ExecReq.getElemsByXPath(XPath.homeGame, driver)
        home = ParseData.parseLastCntWin(elems=elem, isFirstTeam=isFirstTeam, driver=driver,
                                         seasonYearStart=seasonYearStart, seasonYearEnd=seasonYearEnd)
        if home == False:
            raise ValueError()
        ''''''
        ''' Получить игры гостей '''
        print('away')
        ExecReq.clickGetElem(driver, XPath.clickAwayGame)
        while ExecReq.clickGetElem(driver, XPath.clickMoreAwayGame):
            pass

        elem = ExecReq.getElemsByXPath(XPath.awayGame, driver)
        away = ParseData.parseLastCntWin(elems=elem, isFirstTeam=isFirstTeam, driver=driver,
                                         seasonYearStart=seasonYearStart, seasonYearEnd=seasonYearEnd)
        if away == False:
            raise ValueError()
        ''''''
        game.kf = kf
        game.lstHome = home
        game.lstAway = away
    except:
        # self.game.print = False
        print('Ошибка:\n', traceback.format_exc())
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.close()
        return False
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.close()
    return True