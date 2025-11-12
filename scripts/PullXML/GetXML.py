from urllib.parse import urlparse, parse_qs, urlunparse
import requests
import os


# Obtém a pasta Downloads do usuário


def getXML(xml, url):
    try:
        xml = xml.rstrip()

        # Parse da URL
        parsed_url = urlparse(url)

        # Divide o caminho da URL e substitui o último segmento (a numeração)
        path_parts = parsed_url.path.split("/")
        path_parts[-1] = xml  # Substitui o último segmento pelo novo número
        new_path = "/".join(path_parts)

        # Remonta a URL com o novo número no XML
        new_url = urlunparse(
            (
                parsed_url.scheme,
                parsed_url.netloc,
                new_path,
                parsed_url.params,
                parsed_url.query,
                parsed_url.fragment,
            )
        )

        # Nome do arquivo para salvar
        downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        nome_arquivo = f"{xml}.xml"
        caminho_arquivo = os.path.join(downloads_dir, nome_arquivo)

        # Fazer o download do arquivo
        response = requests.get(new_url, stream=True, timeout=120, verify=False)
        # Verifica se o download foi bem-sucedido (código 200)
        if response.status_code == 200:
            with open(caminho_arquivo, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            # print(f"Download concluído! Arquivo salvo como: {nome_arquivo}")
        else:
            print(f"Erro ao baixar o arquivo. Código de status: {response.status_code}")
    except Exception as e:
        raise Exception(f"Erro ao baixar os cupons: {e}")