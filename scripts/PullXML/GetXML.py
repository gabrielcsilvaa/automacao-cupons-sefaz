from urllib.parse import urlparse, parse_qs, urlunparse, urlencode
import requests
import os
import time  # <- NOVO

def getXML(xml, url):
    try:
        xml = xml.strip()  # tira espaços / quebras de linha só por segurança

        # Parse da URL original (capturada pelo LinkXML)
        parsed_url = urlparse(url)

        # Mantém o path original (não mexe no ID interno!)
        new_path = parsed_url.path

        # Lê a query string e troca apenas a chaveAcesso
        query_dict = parse_qs(parsed_url.query)
        # garante que existe o parâmetro
        query_dict["chaveAcesso"] = [xml]

        new_query = urlencode(query_dict, doseq=True)

        # Remonta a URL com a mesma base, mesmo path, mas chaveAcesso trocada
        new_url = urlunparse(
            (
                parsed_url.scheme,
                parsed_url.netloc,
                new_path,
                parsed_url.params,
                new_query,
                parsed_url.fragment,
            )
        )

        print("Baixando XML da chave:", xml)
        print("URL usada:", new_url)

        # Pasta Downloads
        downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        nome_arquivo = f"{xml}.xml"
        caminho_arquivo = os.path.join(downloads_dir, nome_arquivo)

        # Faz o download
        response = requests.get(new_url, stream=True, timeout=120, verify=False)

        if response.status_code == 200:
            with open(caminho_arquivo, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
        else:
            print(
                f"Erro ao baixar o arquivo da chave {xml}. "
                f"Código de status: {response.status_code}"
            )

    except Exception as e:
        print(f"[AVISO] Falha ao baixar {xml}: {e}")
        return False  # <- NÃO LEVANTA ERRO, SÓ CONTINUA


# ============================
# NOVO: helpers para Selenium
# ============================

def _esperar_novo_arquivo(downloads_dir, arquivos_antes, timeout=120):
    """
    Fica monitorando a pasta de Downloads até aparecer um arquivo novo
    (ignorando .crdownload). Retorna o caminho completo do novo arquivo.
    """
    inicio = time.time()

    while time.time() - inicio < timeout:
        arquivos_atual = set(os.listdir(downloads_dir))
        novos = arquivos_atual - arquivos_antes

        # Ignora arquivos temporários de download
        candidatos = [f for f in novos if not f.endswith(".crdownload")]

        if candidatos:
            caminhos = [os.path.join(downloads_dir, f) for f in candidatos]
            # pega o mais recente
            mais_recente = max(caminhos, key=os.path.getmtime)
            return mais_recente

        time.sleep(1)

    return None


def esperar_download_e_renomear(downloads_dir, arquivos_antes, chave_xml):
    """
    Depois de clicar no botão de download via Selenium, chama essa função:
    - espera um novo arquivo aparecer na pasta de Downloads
    - renomeia para <chave_xml>.xml (se ainda não existir)
    """
    try:
        novo_arquivo = _esperar_novo_arquivo(downloads_dir, arquivos_antes, timeout=180)

        if not novo_arquivo:
            print(f"[AVISO] Não detectei download para a chave {chave_xml} dentro do tempo limite.")
            return False

        destino = os.path.join(downloads_dir, f"{chave_xml}.xml")

        if os.path.exists(destino):
            # Em tese o analisadorXmls já evita duplicidade,
            # mas deixei essa segurança extra.
            print(f"[INFO] XML da chave {chave_xml} já existe. Mantendo arquivo atual.")
            return True

        os.rename(novo_arquivo, destino)
        print(f"[OK] Download concluído e renomeado para {chave_xml}.xml")
        return True

    except Exception as e:
        print(f"[ERRO] Falha ao renomear arquivo da chave {chave_xml}: {e}")
        return False