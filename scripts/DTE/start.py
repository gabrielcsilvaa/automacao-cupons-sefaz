from Interface.app_state import app_state
import time

from utils.driverFunctions import *

def startProcess(driver):
    
    driver.get('https://portal-dte.sefaz.ce.gov.br/#/index')
    
    time.sleep(5)
    
    certificadoDigital = locateByXpath(driver, 30, '/html/body/my-app/div/div/div/app-index/div/div/div[2]/div[1]/div/div/a[1]/div')
    certificadoDigital.click()
    
    time.sleep(3)
    
    #Só volta a executar quando finalizar de selecionar o certificado digital, ele aguarda o elemento da lista de empresas aparecerem.
    locateByXpath(driver, 200, '/html/body/my-app/div/div/div/app-perfil/div/div[1]/table/thead')
    
    #Seleciona a opção contador
    profile = locateByXpath(driver, 30, '/html/body/my-app/div/div/div/app-perfil/div/div[1]/table/tbody/tr/td[1]')
    profile.click()
        
    
    time.sleep(1)

    enterButton = locateByXpath(driver, 30, '/html/body/my-app/div/div/div/app-perfil/div/div[2]/button[2]')
    enterButton.click()