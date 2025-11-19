import time
import autoit

from utils.driverFunctions import *

from Interface.app_state import app_state

from scripts.DTE.leaveSefaz import leaveSefazDte

from selenium.webdriver.support.ui import Select

import keyboard
import mouse

def downloadCsvAut(driver):
    
    NfeCfe = locateByXpath(driver, 30, '//*[@id="menu_indicadores_nfce"]')
    NfeCfe.click()
    
    time.sleep(8)
    
    selectMonth = findElementByXpath(driver, '//*[@id="mes_select"]')
    optionMonth = Select(selectMonth)
    optionMonth.select_by_index(int(app_state.mes) - 1)
    
    selectYear = findElementByXpath(driver, '//*[@id="ano_select"]')
    optionYear = Select(selectYear)
    optionYear.select_by_value(f'{app_state.ano}')
    
    time.sleep(2)
    
    buttonPesquisar = locateByXpath(driver, 30, '//*[@id="tab_emitidos"]/div[1]/div[1]/button') 
    buttonPesquisar.click()
    
    time.sleep(15)
    
    #ESPERA O LOADING PARAR
    WebDriverWait(driver, 100).until_not(
    EC.presence_of_element_located((By.CLASS_NAME, 'modal fade in'))
    )
    
    # VERIFICA SE EXISTE UM VALOR NA TABELA
    tableValue = findElementByXpath(driver, '//*[@id="tab_emitidos"]/table/tbody[1]/tr/td[3]/div')
    
    if(tableValue.text != '0,00'):
        
        valueLink = locateByXpath(driver, 500, '//*[@id="tab_emitidos"]/table/tbody[1]/tr/td[3]/div/a')
        time.sleep(2)          
        valueLink.click()

        time.sleep(10)
        
        downloadButton = locateByXpath(driver, 30, '//*[@id="ModalDet"]/div/div/div[2]/div[1]/div/div/button')
        time.sleep(2)          
        downloadButton.click()
        
        time.sleep(8)
        
        csvButton = locateByXpath(driver, 30, '//*[@id="ModalDet"]/div/div/div[2]/div[1]/div/div/ul/li[2]/a')
        csvButton.click()
        time.sleep(8)
        
        closeButton = locateByXpath(driver, 30, '//*[@id="ModalDet"]/div/div/div[1]/button')
        closeButton.click()                                    
        time.sleep(2)
        
        return True
    
    else:
        print('Essa empresa não tem cupons fiscais autorizados até o momento.')
        return False
    

def downloadCsvCancel(driver):
    cancelTable= locateByXpath(driver,30, '/html/body/app-root/div/app-nfce/div/div/section[2]/div/div/div/ul/li[2]/a')
    cancelTable.click()
    
    time.sleep(6)
             
    #SELECIONAR MES E ANO
    selectMonth = findElementByXpath(driver, '//*[@id="mes_select"]')
    optionMonth = Select(selectMonth)
    optionMonth.select_by_index(int(app_state.mes) - 1)
    
    selectAno = driver.find_element(By.XPATH, '//*[@id="ano_select"]')
    optionAno = Select(selectAno)
    optionAno.select_by_value(f'{app_state.ano}')
    
    time.sleep(2)
    
    buttonPesquisar = locateByXpath(driver, 30, '//*[@id="tab_emitidos_outros"]/div[1]/div[1]/button')
    buttonPesquisar.click()  
    
    time.sleep(15)
    
    #ESPERA O LOADING PARAR
    WebDriverWait(driver, 100).until_not(
    EC.presence_of_element_located((By.CLASS_NAME, 'modal fade in'))
    )
           
    
    tabelaValue = driver.find_element(By.XPATH, f'//*[@id="tab_emitidos_outros"]/table/tfoot/tr/td[3]')
    if(tabelaValue.text != '0,00'):

        valueLink = WebDriverWait(driver, 5000).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="tab_emitidos_outros"]/table/tbody/tr/td[3]/div/a'))
        ) 
        time.sleep(2)
        valueLink.click()
          
        time.sleep(10)
        
        downloadButton = locateByXpath(driver, 30, '//*[@id="Modal"]/div/div/div[2]/div[1]/div/div/button')
        downloadButton.click()  
        
        time.sleep(8)
        
        csvButton = locateByXpath(driver, 30, '//*[@id="Modal"]/div/div/div[2]/div[1]/div/div/ul/li[2]/a')
        csvButton.click()
        
        time.sleep(8)
        
        closeButton = locateByXpath(driver,30 , '//*[@id="Modal"]/div/div/div[1]/button')
        closeButton.click()
        time.sleep(2)
        
        leaveSefazDte(driver)
        
        return True
        
    else:
        
        print('Essa empresa não tem cupons fiscais de cancelamento até o momento')
        
        leaveSefazDte(driver)
        
        time.sleep(2)
        return False