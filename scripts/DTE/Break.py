from utils.driverFunctions import *

import keyboard, autoit, mouse


def passBreak(driver):
    
    # Aguarda até que a tecla Enter seja pressionada ou o botão esquerdo do mouse seja clicado
    while True:
        if keyboard.is_pressed("enter") or mouse.is_pressed("left"):
            break
    
    time.sleep(11)
    autoit.send('{ENTER}')
    time.sleep(5)
    autoit.send('{ENTER}')
    time.sleep(6)
    
    
    for window in driver.window_handles:
        
        driver.switch_to.window(window)
        print(f"Alterado para: {driver.title}")
    
    
    try:
        error = locateByXpath(driver,10,'//*[@id="modalMensagem"]/div/div/div[2]/div/div[2]/div/div/label')
        error.click()
    except:
        print('Sem avisos continuando')    
        