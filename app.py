import cv2
import pygame
import numpy as np
import sys 

from PIL import Image
import os
import datetime

######################################
#Configurações
import configparser
######################################
config = configparser.ConfigParser()
config.read('config.ini')
######
cam_index = config.get('Config', 'cam_index')

altura = config.get('Config', 'screen_altura')
largura = config.get('Config', 'screen_largura')
screen_res = altura, largura

altura = config.get('Config', 'cam_altura')
largura = config.get('Config', 'cam_largura')
cam_res = altura, largura

cam_overlay_path = ('Paths', 'cam_overlay_path')
loadscreen_path = ('Paths', 'loadscreen_path')

framerate = config.get('Config', 'framerate')
animation_time = config.get('Config', 'animation_time')
######################################

######################################
# Pygame
import pygame
pygame.init()
screen = pygame.display.set_mode((screen_res[0],screen_res[1]), pygame.FULLSCREEN)
clock = pygame.time.Clock()
######################################

######################################
# Camera
cam = cv2.VideoCapture(cam_index)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, cam_res[0])
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_res[1])
cam.set(cv2.CAP_PROP_FPS, 30)
######################################

######################################
# Carregando overlays 
cam_overlay = pygame.image.load(cam_overlay_path).convert_alpha()
cam_overlay = pygame.transform.scale(cam_overlay, screen_res)
cam_overlay = pygame.transform.flip(cam_overlay, True, False)

loadscreen = pygame.image.load(loadscreen_path)
loadscreen = pygame.transform.scale(loadscreen, screen_res)
######################################

######################################
def editImage(imagem, filename, screen_res = screen_res):
    save_path = "Fotos Massa//"
    imagem = Image.open(os.path.join("temp", filename))
    
    overlay = Image.open("assets/overlay2.png")
    overlay = overlay.resize(imagem.size)
    
    imagem.paste(overlay, (0, 0), overlay)
    imagem.save(save_path + filename)
    
    os.remove(os.path.join("temp", filename))
    
    imagem_py = pygame.image.load(os.path.join("Fotos Massa", filename)).convert()
    imagem_py = pygame.transform.scale(imagem_py, screen_res)

    return imagem_py, True

ret, frame = cam.read()
if ret:
    while True:

        clock.tick(framerate)

        frame = cv2.resize(frame, screen_res, interpolation=cv2.INTER_AREA)
        imagem = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imagem = np.rot90(imagem)

        imagem = pygame.surfarray.make_surface(imagem)
        imagem = pygame.transform.flip(imagem, True, False)

        screen.blit(imagem, (0,0))
        screen.blit(cam_overlay, (0, 0))
        pygame.display.flip()

        ret, frame = cam.read()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:

                    filename = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S Massa-festa-pinhao.png")
                    
                    start_time = pygame.time.get_ticks()
                    while pygame.time.get_ticks() - start_time < animation_time:

                        screen.fill((0, 0, 0))
                        pygame.display.flip()
                        pygame.time.wait(40)
                        screen.fill((255, 255, 255))
                        pygame.display.flip()
                        pygame.time.wait(40)

                    screen.blit(cachorro,(0,0))
                    pygame.display.flip()


                    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                    ret, frame = cam.read()
                    if ret:
                        cv2.imwrite(os.path.join("temp", filename), frame)

                        cam.set(cv2.CAP_PROP_FRAME_WIDTH, cam_res[0])
                        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_res[1])

                        imagem, show_image = editImage(frame, filename)
                        screen.blit(imagem, (0,0))
                        pygame.display.flip()

                        while show_image == True:
                            ret, frame = cam.read()
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_SPACE:
                                        screen.blit(imagem, (0,0))
                                        screen.blit(cam_overlay, (0, 0))
                                        pygame.display.flip()
                                        show_image = False
                                    elif event.key == pygame.K_ESCAPE:
                                        cam.release()
                                        pygame.quit()
                                        sys.exit()

                elif event.key == pygame.K_ESCAPE:
                    cam.release()
                    pygame.quit()
                    sys.exit()
