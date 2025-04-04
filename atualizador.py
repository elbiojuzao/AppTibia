import time
import shutil
import os

time.sleep(2)  # Espera o app fechar

try:
    shutil.move("AppTibia_novo.exe", "AppTibia.exe")
    os.startfile("AppTibia.exe")  # Executa o app atualizado
except Exception as e:
    print("Erro ao atualizar:", e)
    input("Pressione ENTER para sair.")
