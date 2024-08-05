import time
import pyautogui
import requests
from bs4 import BeautifulSoup

# Número de capturas de tela que deseja tirar
num_capturas = 5

# Pausar para permitir que você abra a janela correta
print("O script começará em 5 segundos...")
time.sleep(5)

x1, y1 = -1882, 301

for i in range(1, num_capturas + 1):

    # Rolar a página para baixo (opcional)
    # Substitua -500 pelo número de cliques de rolagem necessários
    # pyautogui.scroll(-1000)

    time.sleep(3)

    # VER
    pyautogui.click(x1, y1)

    time.sleep(3)

    screenshot = pyautogui.screenshot()
    filename = f"dados_basicos_grande_oeste{i}.png"
    screenshot.save(filename)
    
    time.sleep(3)
    
    # ENDERECO
    x, y = -1511, 451
    pyautogui.click(x, y)
    
    time.sleep(3)
    
    screenshot = pyautogui.screenshot()
    filename = f"dados_basicos_endereco{i}.png"
    screenshot.save(filename)
    
    time.sleep(3)
    
    # CONTATO
    x, y = -1511, 453
    pyautogui.click(x, y)

    time.sleep(3)
    
    screenshot = pyautogui.screenshot()
    filename = f"dados_basicos_contato{i}.png"
    screenshot.save(filename)
    
    time.sleep(3)
    
    # OBS
    x, y = -1511, 530
    pyautogui.click(x, y)

    time.sleep(3)
    
    screenshot = pyautogui.screenshot()
    filename = f"dados_basicos_obs{i}.png"
    screenshot.save(filename)
    
    time.sleep(3)
    
    # INTERNO
    x, y = -1511, 567
    pyautogui.click(x, y)

    time.sleep(3)
    
    screenshot = pyautogui.screenshot()
    filename = f"dados_basicos_interno{i}.png"
    screenshot.save(filename)

    time.sleep(3)
    
    # FECHA
    x, y = -600, 243
    pyautogui.click(x, y)
    
    time.sleep(3)

    y1 = y1 + 3