from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


def fecharPopupDTE(driver):
    print("[POPUP DTE] Verificando se existe popup do DTE...")

    try:
        # Espera o overlay do popup aparecer (se aparecer)
        popup = WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.popup-overlay")
            )
        )

        print("[POPUP DTE] Popup visível. Procurando botão 'Fechar'...")

        # Dentro desse popup, acha o botão Fechar
        botao_fechar = popup.find_element(
            By.XPATH,
            ".//div[contains(@class, 'popup-footer')]//button[normalize-space()='Fechar']"
        )

        botao_fechar.click()
        time.sleep(1)
        print("[POPUP DTE] Popup fechado com sucesso.")

    except TimeoutException:
        print("[POPUP DTE] Nenhum popup DTE encontrado (segue o fluxo).")
    except Exception as e:
        print(f"[POPUP DTE] Erro ao tentar fechar popup: {e}")


def fecharPopupAmbienteSeguro(driver):
    print("[POPUP AS] Verificando se existe popup do Ambiente Seguro...")

    try:
        botao_fechar = WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'close')]")
            )
        )
        print("[POPUP AS] Botão 'X' encontrado. Clicando...")
        botao_fechar.click()
        time.sleep(1)
        print("[POPUP AS] Popup fechado com sucesso.")
    except TimeoutException:
        print("[POPUP AS] Nenhum popup encontrado (segue o fluxo).")
    except Exception as e:
        print(f"[POPUP AS] Erro ao tentar fechar popup: {e}")
