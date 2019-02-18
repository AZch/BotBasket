import time
import traceback

def getElemsByXPath(XPath, driver):
    while True:
        try:
            elem = driver.find_elements_by_xpath(XPath)
            break
        except:
            continue
    return elem

def getElemByXPath(XPath, driver):
    timeStart = time.time()
    while True:
        try:
            elem = driver.find_element_by_xpath(XPath)
            break
        except:
            if time.time() - timeStart > 15:
                print('Ошибка:\n', traceback.format_exc())
                return False
            continue
    return elem

def clickGetElem(driver, get):
    startTime = time.time()
    while True:
        try:
            elem = driver.find_element_by_xpath(get)
            elem.click()
            break
        except:
            if time.time() - startTime > 5:
                #print('Ошибка:\n', traceback.format_exc())
                print('stop')
                return False
            continue
    return True

def clickElem(elem):
    startTime = time.time()
    while True:
        try:
            elem.click()
            break
        except:
            if time.time() - startTime > 5:
                print('Ошибка:\n', traceback.format_exc())
                return False
            continue

def getKF(driver):
    startTime = time.time()
    while True:
        try:
            kf = getElemByXPath("//div[@id='tab-prematch-odds']", driver)
            floatKfFirst = float(kf.text.split('\n')[1])
            floatKfSec = float(kf.text.split('\n')[3])
            print("kf " + kf.text.split('\n')[1] + " - " + kf.text.split('\n')[3])
            return [floatKfFirst, floatKfSec]
        except:
            if time.time() - startTime > 5:
                print('Ошибка:\n', traceback.format_exc())
                return False
