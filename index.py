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
from scripts.PullXML.GetXML import getXML

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
            linkApi = LinkXML(driver)

            continue_message(
                "Processo iniciado, o navegador será fechado, "
                "o computador poderá ser utilizado normalmente enquanto os XMLs são baixados."
            )
            driver.quit()

            # -----------------------------------
            # 5) Começar processo de download dos XMLs (requests)
            # -----------------------------------
            try:
                print(filterList[:10])
                for index, xml in enumerate(filterList):
                    getXML(xml, linkApi)
                    print(f"Processando {index + 1} de {len(filterList)} Xmls...")
                    print(xml)

                time.sleep(2)

                continue_message(
                    f"Processo finalizado, {len(filterList)} XMLs foram baixados, verificar pasta."
                )

            except Exception:
                error_message(
                    "Ocorreu uma instabilidade no ambiente seguro, "
                    "não foi possível baixar todos os cupons, por gentileza, reinicie o programa."
                )

        else:
            raise Exception("Programa encerrado...")

    except Exception as e:
        print(f"Erro: {e}")


initialize()
organizarPastas()
