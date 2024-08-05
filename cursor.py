import pyautogui
import time

time.sleep(3)

# Obter a posição atual do cursor
posicao_cursor = pyautogui.position()

# Imprimir a posição do cursor no terminal
print(f"A posição atual do cursor é: {posicao_cursor}")


