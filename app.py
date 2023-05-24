import pygame
import pygame.camera

import os
import time
import datetime
import sys

#from PIL import Image
#import cv2

pygame.init()
pygame.camera.init()

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
camera2 = pygame.camera.Camera(pygame.camera.list_cameras()[i], (1280, 720))

#Define a resolução da camera
camera_full_res = (1280, 720)
camera_res = (800, 600)
    
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) # Inicia uma janela em tela cheia
screen_res = screen.get_size() # Pega a resolução da janela = resolução máxima do monitor

cam_overlay = pygame.image.load("assets//overlay.png").convert_alpha() # carrega o overlay da pasta overlay
cam_overlay = pygame.transform.scale(cam_overlay, screen_res)# redimennsiona para o tamanho da tela

overlay = pygame.image.load("assets//overlay2.png").convert_alpha() # carrega o overlay da pasta overlay
overlay = pygame.transform.scale(overlay, camera_full_res)# redimennsiona para o tamanho da tela

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
    capture = pygame.transform.scale(capture, screen_res)
    
    screen.blit(capture, (0,0))
    screen.blit(cam_overlay, (0,0))
    pygame.display.flip()
    
    for event in pygame.event.get(): # checa se acontecer o evento 
        if event.type == pygame.KEYDOWN: # se apressionar espaço 
            camera.stop()
            camera2.start()
            if event.key == pygame.K_SPACE:
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
                
                screen.blit(loadscreen, (0,0))
                pygame.display.flip()
                time.sleep(2)
                
                imagem = camera2.get_image()
                filename = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S Massa-festa-pinhao.png" )
                #pygame.image.save(capture , os.path.join("temp", filename))
                screen.blit(imagem, (0,0)
                screen.blit(overlay, (0,0)
                pygame.image.save(imagem , os.path.join("Fotos Massa", filename))
                screen = pygame.transform.scale(screen, screen_res)
                pygame.display.flip()                 
                camera2.stop()
                camera.start()
                edited == True
                
                #imagem, edited = editImage(imagem = os.path.join("temp", filename), filename = filename)
                #imagem = pygame.transform.scale(imagem, screen_res)
                #screen.blit(imagem, (0,0))
                #pygame.display.flip()
                while edited:
                    capture = camera.get_image()
                    for event in pygame.event.get(): # checa se acontecer o evento 
                        if event.type == pygame.KEYDOWN: # se apressionar espaço 
                             if event.key == pygame.K_SPACE:
           
                                    capture = pygame.transform.scale(capture, screen_res)
                                    screen.blit(capture, (0,0))
                                    screen.blit(cam_overlay, (0,0))
                                    pygame.display.flip()
                                    edited = False
                                    
                
            elif event.key == pygame.K_ESCAPE: #se pressionar esc
                camera.stop()
                pygame.quit()
                sys.exit()

