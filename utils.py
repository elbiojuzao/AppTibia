import json
import os
from PIL import Image, ImageTk
import requests
import io

BASE_URL_TIBIADATA = "https://api.tibiadata.com/v4/"

import json
import os

def save_settings(window, app_name):
    settings = {
        "geometry": window.geometry(),
        "alpha": window.attributes('-alpha')
    }
    config_dir = "config_apps"  
    os.makedirs(config_dir, exist_ok=True)
    filepath = os.path.join(config_dir, f"{app_name}_settings.json")
    try:
        with open(filepath, "w") as f:
            json.dump(settings, f)
    except Exception as e:
        print(f"Erro ao salvar configurações para {app_name}: {e}")

def load_settings(window, app_name):
    config_dir = "config_apps"
    filepath = os.path.join(config_dir, f"{app_name}_settings.json")
    try:
        with open(filepath, "r") as f:
            settings = json.load(f)
            if "geometry" in settings:
                window.geometry(settings["geometry"])
            if "alpha" in settings:
                window.attributes('-alpha', settings["alpha"])
    except FileNotFoundError:
        pass 
    except Exception as e:
        print(f"Erro ao carregar configurações para {app_name}: {e}")

def apply_settings(window, app_name):
    load_settings(window, app_name)

def requisicao_api(endpoint):
    url_completa = BASE_URL_TIBIADATA + endpoint
    try:
        response = requests.get(url_completa)
        response.raise_for_status()  # Lança uma exceção para códigos de status ruins (4xx ou 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição para {url_completa}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON de {url_completa}: {e}")
        return None
    
def load_json_config(filename, default_config=None):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        if default_config is not None:
            return default_config
        return {}
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON em {filename}. Retornando configuração padrão.")
        if default_config is not None:
            return default_config
        return {}

def save_json_config(filename, config_data):
    try:
        with open(filename, 'w') as f:
            json.dump(config_data, f, indent=4) 
    except IOError as e:
        print(f"Erro ao salvar configuração em {filename}: {e}")

def load_image_from_url(image_url, size=(80, 80)):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        image = image.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(image)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao carregar imagem de {image_url}: {e}")
        return None
    except Exception as e:
        print(f"Erro ao processar imagem de {image_url}: {e}")
        return None
    