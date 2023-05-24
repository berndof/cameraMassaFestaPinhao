import pygame
import pygame.camera

import os
import time
import datetime
import sys

pygame.init()
pygame.camera.init()


camera = pygame.camera.Camera(pygame.camera.list_cameras()[0], (800, 600))
camera2 = pygame.camera.Camera(pygame.camera.list_cameras()[0], (1280, 720))


#Define a resolução da camera
camera_res = (800, 600)
camera_full_res = (1280, 720)
    
screen = pygame.display.set_mode((1280,720), pygame.FULLSCREEN) # Inicia uma janela em tela cheia
screen_res = screen.get_size() # Pega a resolução da janela = resolução máxima do monitor

cam_overlay = pygame.image.load("assets//overlay.png").convert_alpha() # carrega o overlay da pasta overlay
cam_overlay = pygame.transform.scale(cam_overlay, screen_res)# redimennsiona para o tamanho da tela

loadscreen = pygame.image.load("assets//loadscreen.png").convert() # carrega o overlay da pasta overlay
loadscreen = pygame.transform.scale(loadscreen, screen_res)

overlay = pygame.image.load("assets//overlay2.png").convert_alpha() # carrega o overlay da pasta overlay
overlay = pygame.transform.scale(overlay, camera_full_res)

while True:
    capture = camera.get_image()
    scaled_capture = pygame.transform.scale(capture, screen_res)
    screen.blit(scaled_capture, (0,0))
    screen.blit(cam_overlay, (0,0))
    pygame.display.flip()
    for event in pygame.event.get(): 
        if event.type == pygame.KEYDOWN:
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
                time.sleep(1.3)
                capture = camera2.get_image()
                screen.blit(loadscreen, (0,0))
                pygame.display.flip()

                filename = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S Massa-festa-pinhao.png" )
                screen.blit(capture, (0,0))
                screen.blit(overlay, (0,0))
                pygame.display.flip()
                camera2.stop()
                pygame.image.save(screen, os.path.join("Fotos Massa", filename))
                #screen = pygame.transform.scale(screen, screen_res)
                #screen.blit(screen, (0,0))
                #camera2.stop()
                try:
                    camera.start()  # Tenta iniciar a camera
                except pygame.error:
                    print("Failed to connect")
                    # Se não startar, vai pra proxima camera da lista
                    continue
                print(f"Connected to camera ")
                while True :
                    capture = camera.get_image()
                    for event in pygame.event.get(): # checa se acontecer o evento 
                        if event.type == pygame.KEYDOWN: # se apressionar espaço 
                             if event.key == pygame.K_SPACE: 
                                scaled_capture = pygame.transform.scale(capture, screen_res)
                                screen.blit(scaled_capture, (0,0))
                                screen.blit(cam_overlay, (0,0))
                                pygame.display.flip()
                                break
            elif event.key == pygame.K_ESCAPE: #se pressionar esc
                camera.stop()
                pygame.quit()
                sys.exit()

