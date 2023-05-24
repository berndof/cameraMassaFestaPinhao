import pygame
import pygame.camera

import os
import time
import datetime
import sys

from PIL import Image
#import cv2

pygame.init()
pygame.camera.init()

pygame.camera.list_cameras()

for i in range(len(pygame.camera.list_cameras())):
    camera = pygame.camera.Camera(pygame.camera.list_cameras()[i], (800, 600))
    try:
        camera.start()  # Tenta iniciar a camera
    except pygame.error:
        print("Failed to connect")
        # Se não startar, vai pra proxima camera da lista
        continue
    print(f"Connected to camera {i}")
    break  # Se startar quebra o loop 


#Define a resolução da camera
camera_res = (913, 512)
    
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) # Inicia uma janela em tela cheia
screen_res = screen.get_size() # Pega a resolução da janela = resolução máxima do monitor

cam_overlay = pygame.image.load("assets//overlay.png").convert_alpha() # carrega o overlay da pasta overlay
cam_overlay = pygame.transform.scale(cam_overlay, screen_res)# redimennsiona para o tamanho da tela

loadscreen = pygame.image.load("assets//loadscreen.png").convert() # carrega o overlay da pasta overlay
loadscreen = pygame.transform.scale(loadscreen, screen_res)


def editImage(imagem, filename):
    save_path = "Fotos Massa//" # caminho para salvar

    imagem = Image.open(imagem) # carrega a imagem
    
    #carrega o ovelay aplicado na foto e redimensiona
    overlay = Image.open("assets//overlay2.png") 
    overlay = overlay.resize((imagem.size))
    
    #cola a sobreposição e salva
    imagem.paste(overlay, (0,0), overlay)
    imagem.save(save_path + filename)
    
    
    #apaga a foto temporaria
    os.remove(os.path.join("temp", filename))
    
    imagem = pygame.image.load(save_path + filename)
    
    return imagem, True


while True:

    capture = camera.get_image()
    
    scaled_capture = pygame.transform.scale(capture, screen_res)
    
    screen.blit(scaled_capture, (0,0))
    screen.blit(cam_overlay, (0,0))
    
    pygame.display.flip()
    
    for event in pygame.event.get(): # checa se acontecer o evento 
        if event.type == pygame.KEYDOWN: # se apressionar espaço 
            if event.key == pygame.K_SPACE:
                screen.blit(loadscreen, (0,0))
                pygame.display.flip()
                
                camera.stop()
                camera = None    
                camera = pygame.camera.Camera(pygame.camera.list_cameras()[0], (1280, 720))
                camera.start()
                
                capture = camera.get_image()
                filename = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S Massa-festa-pinhao.png" )
                pygame.image.save(capture , os.path.join("temp", filename))

                start_time = pygame.time.get_ticks()
                # Define o tempo da animação
                animation_time = 150
                while pygame.time.get_ticks() - start_time < animation_time:
                    # Alterna entre preto e branco
                    if pygame.time.get_ticks() % 100 < 50:
                        screen.fill((255, 255, 255))
                        pygame.display.flip()
                    else:
                        screen.fill((0, 0, 0))
                        pygame.display.flip()

                camera.stop()
                camera = None
                camera = pygame.camera.Camera(pygame.camera.list_cameras()[0], (913, 512))
                camera.start()

                
                imagem, edited = editImage(imagem = os.path.join("temp", filename), filename = filename)
                imagem = pygame.transform.scale(imagem, screen_res)
                screen.blit(imagem, (0,0))
                pygame.display.flip()
                while edited:
                    capture = camera.get_image()
                    for event in pygame.event.get(): # checa se acontecer o evento 
                        if event.type == pygame.KEYDOWN: # se apressionar espaço 
                             if event.key == pygame.K_SPACE:
                                    
                                    scaled_capture = pygame.transform.scale(capture, screen_res)
                                    screen.blit(scaled_capture, (0,0))
                                    screen.blit(cam_overlay, (0,0))
                                    edited = False
                                    
                
            elif event.key == pygame.K_ESCAPE: #se pressionar esc
                camera.stop()
                pygame.quit()
                sys.exit()

