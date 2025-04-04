import requests
import os
import subprocess
import sys

VERSAO_ATUAL = "1.0.0"
URL_JSON = "https://gist.githubusercontent.com/elbiojuzao/1be4fee4cdb57cdb71b195221bc0933d/raw/versao.json"
NOME_NOVO_EXECUTAVEL = "AppTibia_novo.exe"

def verificar_atualizacao():
    try:
        response = requests.get(URL_JSON)
        if response.status_code == 200:
            dados = response.json()
            nova_versao = dados["version"]
            if nova_versao != VERSAO_ATUAL:
                return dados  # Tem atualização
        return None
    except:
        return None

def baixar_arquivo(url, caminho_destino):
    try:
        with requests.get(url, stream=True) as r:
            with open(caminho_destino, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return True
    except:
        return False

def iniciar_atualizador():
    subprocess.Popen(["python", "atualizador.py"])
    sys.exit(0)
