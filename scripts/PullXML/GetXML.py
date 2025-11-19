from urllib.parse import urlparse, parse_qs, urlunparse, urlencode
import requests
import os

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
        raise Exception(f"Erro ao baixar os cupons: {e}")
        