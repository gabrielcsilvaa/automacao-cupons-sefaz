from utils.driverFunctions import *

def company_finder_AmbSeg(driver, companyCode):
    
    try:
        # Aguarde a tabela carregar
        WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="form1"]/table'))
        )
    
    except:
        print('O ambiente seguro está instável, tente novamente mais tarde...')
        return    

    #Lista das linhas
    lines = findElementsByXpath(driver, '//*[@id="form1"]/table/tbody/tr')
    
    for line in lines:
        cell = line.find_element(By.XPATH, './td[1]')
        cellName = line.find_element(By.XPATH, './td[2]') # Ajustar índice conforme necessário
        textName = cellName.text
        cellText = cell.text
        inscricaoEstadual = companyCode.lstrip('0')

        if(cellText == inscricaoEstadual):
            cell.click()
            print('Inscrição estadual: ',cellText,' Empresa: ', textName)
            break
    
    time.sleep(2)