import json
import os
from PIL import Image, ImageTk
import requests
import io
import customtkinter as ctk

BASE_URL_TIBIADATA = "https://api.tibiadata.com/v4/"

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
    
def load_json_config(config_file, default_config=None):
    if default_config is None:
        default_config = {}
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return default_config
    else:
        return default_config

def save_json_config(config_file, config_data):
    try:
        with open(config_file, "w") as f:
            json.dump(config_data, f, indent=4)
    except IOError as e:
        print(f"Erro ao salvar a configuração em {config_file}: {e}")

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