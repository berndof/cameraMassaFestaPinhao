import cv2
import numpy as np

# Definir a resolução desejada
resolution = (1920, 1080)

# Criar a janela
window_name = "My Window"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, *resolution)

# Abrir a câmera
camera = cv2.VideoCapture(0)  # Use o índice correto se houver várias câmeras conectadas


while True:
    # Capturar um frame da câmera
    ret, frame = camera.read()
    if not ret:
        break
    
    # Redimensionar o frame para a resolução desejada
    frame = cv2.resize(frame, resolution)
    
    # Aplicar qualquer processamento necessário ao frame
    
    # Exibir o frame na janela
    cv2.imshow(window_name, frame)
    
    # Verificar se a tecla Esc foi pressionada para sair do loop
    if cv2.waitKey(1) == 27:
        break

# Liberar recursos e fechar a janela
camera.release()
cv2.destroyAllWindows()
