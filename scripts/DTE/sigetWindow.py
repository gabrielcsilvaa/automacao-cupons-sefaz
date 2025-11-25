from utils.driverFunctions import *
from utils.popupHandler import *

import time

def enterSiget(driver):
    try:

        fecharPopupDTE(driver)

        siget = locateByXpath(driver,30, '/html/body/my-app/div/div/div/app-home/section/div/div[2]/div/ul/li[1]')
        time.sleep(10)        
        siget.click()
        
        WebDriverWait(driver, 50).until_not(
        EC.presence_of_element_located((By.XPATH, '/html/body/my-app/div/div/div/app-home/section/div[2]'))
        )
        
    except:
        try:
            print('Possivel carregamento infinito siget, tentando novamente...')
            driver.refresh()
            time.sleep(5)
            siget = locateByXpath(driver,30, '/html/body/my-app/div/div/div/app-home/section/div/div[2]/div/ul/li[1]')
            time.sleep(10)        
            siget.click()
            time.sleep(3)
            
            WebDriverWait(driver, 50).until_not(
            EC.presence_of_element_located((By.XPATH, '/html/body/my-app/div/div/div/app-home/section/div[2]'))
            )
            
        except:
            raise Exception('O DTE está instável. tentar novamente mais tarde...')