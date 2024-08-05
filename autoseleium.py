import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Configura o caminho para o ChromeDriver
chrome_driver_path = r'C:\Users\rafae\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'  # Caminho atualizado

# Configura o navegador
options = Options()
options.add_argument("--start-maximized")  # Maximiza a janela do navegador
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

driver.get('https://www.hitex.com.br/plataforma/index.php?p=gestor-administrativo&g=0')

time.sleep(5)

x1, y1 = -1866, 286

print("O script começará em 5 segundos...")
time.sleep(5)

# VER
pyautogui.click(x1, y1)

time.sleep(3)

try:
    # Espera até que o modal esteja visível
    modal_selector = 'modal-body'  # Substitua pelo seletor que corresponde ao modal
    driver.implicitly_wait(10)  # Espera implícita para o modal

    # Localiza o elemento do status no modal
    status_element = driver.find_element(By.CSS_SELECTOR, '.label-success')
    status = status_element.text
    print(f"Status do modal: {status}")

except Exception as e:
    print(f"Erro ao localizar o status: {e}")

# Fecha o navegador
driver.quit()
