# Classes
from classes.login import user_login
from classes.CFElist import cfe_list

# Utils
from utils.CompanyFormater import formatCompanyCode
from utils.csvReader import readCSV
from utils.xml_organizer import analisadorXmls, apagarCSV, organizarPastas

# Importando navegador
from config.browserConfig import Chrome

# Importando função de autenticação
from auth.validateAcess import authorize_access

# INTERFACE GRÁFICA
from Interface.front import startInterface
from Interface.errorWindow import error_message
from Interface.continueWindow import continue_message
from Interface.app_state import app_state

# Scripts todos os passos do DTE
from scripts.DTE.start import startProcess
from scripts.DTE.company_finder import companyFinder
from scripts.DTE.sigetWindow import enterSiget
from scripts.DTE.Break import passBreak

# Versão separada para CFE e NFC-e (CSV)
from scripts.DTE.searchCsvCfe import downloadCsvAut as downloadCsvAutCfe, downloadCsvCancel as downloadCsvCancelCfe
from scripts.DTE.searchCsvNfce import downloadCsvAut as downloadCsvAutNfce, downloadCsvCancel as downloadCsvCancelNfce

# Scripts todos os passos do Ambiente Seguro
from scripts.AmbienteSeguro.start import loginAmbienteSeguro
from scripts.AmbienteSeguro.enterFMeModule import enterMfeModule
from scripts.AmbienteSeguro.company_finder import company_finder_AmbSeg

# Versão separada para CFE e NFC-e (consulta XML)
from scripts.AmbienteSeguro.CfeQuery import cfeQuery as cfeQueryCfe
from scripts.AmbienteSeguro.nfceQuery import cfeQuery as cfeQueryNfce

# Scripts para puxar todos os XML
from scripts.PullXML.LinkAPI import LinkXML
from scripts.PullXML.GetXML import getXML, esperar_download_e_renomear

import time
import os


downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

acessValidator = authorize_access()  # True or False


def initialize():
    try:
        # Abre a interface (main.py) e só segue se o usuário clicou em EXECUTAR
        startInterface()

        if app_state.next is True:
            # Lê dados globais definidos na interface
            inscricao_estadual = app_state.inscricao_estadual
            mes = app_state.mes
            ano = app_state.ano
            # Novo campo: tipo de cupom (CFE ou NFCE)
            tipo_cupom = getattr(app_state, "tipo_cupom", "CFE")  # default CFE se não vier nada

            print(f"Inscrição: {inscricao_estadual} | Mês: {mes} | Ano: {ano} | Tipo cupom: {tipo_cupom}")

            driver = Chrome()

            # ---------------------------
            # 1) Fluxo DTE - gerar CSV
            # ---------------------------
            startProcess(driver)

            formatedCode = formatCompanyCode(inscricao_estadual)
            companyFinder(driver, formatedCode)

            enterSiget(driver)
            passBreak(driver)

            # Escolhe qual módulo de CSV usar baseado no tipo de cupom
            if tipo_cupom == "CFE":
                print("Baixando CSV de CFE (Autorizados / Cancelados)...")
                responseAut = downloadCsvAutCfe(driver)
            else:
                print("Baixando CSV de NFC-e (Autorizados / Cancelados)...")
                responseAut = downloadCsvAutNfce(driver)

            if responseAut is True:
                readCSV(downloads_path, "Autorizados")
                apagarCSV(downloads_path)

            if tipo_cupom == "CFE":
                responseCancel = downloadCsvCancelCfe(driver)
            else:
                responseCancel = downloadCsvCancelNfce(driver)

            if responseCancel is True:
                readCSV(downloads_path, "Cancelados")
                apagarCSV(downloads_path)

            # -----------------------------------
            # 2) Login Ambiente Seguro / MFE
            # -----------------------------------
            user = user_login.username
            password = user_login.password

            loginAmbienteSeguro(driver, user, password)
            enterMfeModule(driver)
            company_finder_AmbSeg(driver, inscricao_estadual)

            # -----------------------------------
            # 3) Primeira consulta para "abrir"
            #    (usa só o primeiro cupom da lista)
            # -----------------------------------
            if not cfe_list.totalList:
                error_message("Nenhum cupom encontrado na lista. Verifique o CSV gerado.")
                driver.quit()
                return

            primeira_chave = cfe_list.totalList[0]

            if tipo_cupom == "CFE":
                cfeQueryCfe(driver, primeira_chave)
            else:
                cfeQueryNfce(driver, primeira_chave)

            # -----------------------------------
            # 4) Filtrar o que ainda falta baixar
            # -----------------------------------
            filterList = analisadorXmls(cfe_list.totalList)

            if not filterList:
                continue_message(
                    "Nenhum XML pendente para download. Todos os cupons já possuem XML salvo."
                )
                driver.quit()
                return

            total_para_baixar = len(filterList)

            # Estimativa de tempo (ajuste o valor médio se quiser)
            # Exemplo: 5 segundos por cupom
            tempo_medio_por_cupom = 5  # segundos
            estimativa_segundos = total_para_baixar * tempo_medio_por_cupom

            minutos, segundos = divmod(estimativa_segundos, 60)
            horas, minutos = divmod(minutos, 60)

            if horas > 0:
                estimativa_str = f"{horas}h {minutos}min {segundos}s"
            elif minutos > 0:
                estimativa_str = f"{minutos}min {segundos}s"
            else:
                estimativa_str = f"{segundos}s"

            print(f"Serão baixados {total_para_baixar} cupons.")
            print(f"Estimativa de tempo total: {estimativa_str}")

            # Aqui é onde aparece o pop-up avisando que vai começar o download
            continue_message(
                f"Serão baixados {total_para_baixar} cupons.\n"
                f"Estimativa de tempo total: {estimativa_str}.\n\n"
                "O navegador será minimizado e você poderá usar o computador normalmente "
                "enquanto os XMLs são baixados em segundo plano."
            )

            # A PARTIR DAQUI: não precisa mais ver o navegador
            try:
                driver.minimize_window()
            except Exception:
                pass  # se der algum erro aqui, não é crítico

            # -----------------------------------
            # 5) Começar processo de download dos XMLs (via Selenium)
            # -----------------------------------
            try:
                baixados_com_sucesso = 0

                for index, xml in enumerate(filterList):
                    xml = xml.strip()
                    print(f"\n[INFO] Processando {index + 1} de {total_para_baixar} XMLs...")
                    print(f"Chave: {xml}")

                    try:
                        # Snapshot dos arquivos atuais da pasta Downloads
                        arquivos_antes = set(os.listdir(downloads_path))

                        # Dispara o fluxo normal de consulta + clique em Download,
                        # SEM mexer nos XPaths já existentes
                        if tipo_cupom == "CFE":
                            cfeQueryCfe(driver, xml)
                        else:
                            cfeQueryNfce(driver, xml)

                        # Espera o arquivo novo aparecer e renomeia para <chave>.xml
                        sucesso = esperar_download_e_renomear(downloads_path, arquivos_antes, xml)

                        if not sucesso:
                            print(f"[AVISO] O XML da chave {xml} pode não ter sido baixado corretamente.")
                        else:
                            baixados_com_sucesso += 1

                    except Exception as e_loop:
                        print(f"[AVISO] Falha ao processar a chave {xml}: {e_loop}")
                        continue

                time.sleep(2)

                continue_message(
                    f"Processo finalizado.\n"
                    f"{baixados_com_sucesso} XMLs foram baixados com sucesso de um total de {total_para_baixar} tentativas.\n"
                    "Verifique a pasta de Downloads ou as pastas organizadas pelo robô."
                )

            except Exception as e:
                print(f"[ERRO] Durante o loop de download: {e}")
                error_message(
                    "Ocorreu uma instabilidade no Ambiente Seguro. "
                    "Não foi possível baixar todos os cupons. "
                    "Por gentileza, reinicie o programa."
                )

            finally:
                try:
                    driver.quit()
                except Exception:
                    pass

        else:
            raise Exception("Programa encerrado...")

    except Exception as e:
        print(f"Erro: {e}")


initialize()
organizarPastas()
