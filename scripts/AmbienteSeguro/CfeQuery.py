from utils.driverFunctions import *

def cfeQuery(driver, cfe):    
    
    # Alternar para a última aba aberta
    driver.switch_to.window(driver.window_handles[-1])
    
    # Localização do elemento
    element_locator = (By.CSS_SELECTOR, "div.modal-backdrop.am-fade")

    # Aguarde até que a classe 'ng-hide' seja adicionada ao elemento
    try:
        WebDriverWait(driver, 150).until(
            lambda driver: "ng-hide" in driver.find_element(*element_locator).get_attribute("class")
        )
        print("")
    except Exception as e:
        print("Timeout: o elemento não adquiriu a classe 'ng-hide' dentro do tempo esperado.")
        
    time.sleep(3)
    # Encontre a quarta <li> dentro da ul com o id 'menulist_root'
    fourth_li = driver.find_element(By.XPATH, '//*[@id="menulist_root"]/li[3]') # agora achando a li do nfce 
    time.sleep(1)

    # Agora encontre o link <a> dentro desse quarto <li>
    link = fourth_li.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/div/div/ul/li[3]/a') # localizando o link <a> dentro da li nfce

    link.click()
    time.sleep(0.5)
    
    cfekey = locateByXpath(driver, 30 , '//*[@id="nfceKey"]')
    
    cfekey.clear()
    time.sleep(0.2)
    cfekey.send_keys(cfe)
    time.sleep(0.1)
    
    
    #Clica no botão consultar.
    queryButton = locateByXpath(driver, 30, '//*[@id="conteudo_central"]/div/div/div/div[3]/form/div[5]/div/div/button[1]')
    
    queryButton.click()
    
    # Tenta encontrar o link 'a' na coluna para selecionar o negocio azul da  nota da nfce 
    xmlLink = locateByXpath(driver, 30, '//*[@id="table-search-coupons"]/tbody/tr/td[4]')
    xmlLink.click()

    download = locateByXpath(driver, 30, '//*[@id="conteudo_central"]/div/div[2]/div/div/div[3]/button')
    download.click()
    
    fechar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'close'))
    )
    fechar.click() # tudo alterado