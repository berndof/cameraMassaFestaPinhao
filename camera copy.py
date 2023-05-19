import pygame
import pygame.camera

import os
import datetime
import sys

import xml.etree.ElementTree as ET
#from PIL import Image

import time





# Lê as configurações do arquivo XML
def read_config(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    # Lê a resolução da câmera do arquivo XML
    camera_resolution = root.find("camera_resolution")
    width = int(camera_resolution.get("width"))
    height = int(camera_resolution.get("height"))
    camera_res = width, height
    # Lê o desired_fps do arquivo XML
    desired_fps = int(root.findtext("desired_fps"))

    # Lê o animation_time do arquivo XML
    animation_time = int(root.findtext("animation_time"))

    camera_index = int(root.findtext("camera_index"))


    return camera_index, camera_res, desired_fps, animation_time

def editImage(imagem, overlay, filename, save_path):
    
    imagem.blit(overlay, (0, 0))
    pygame.image.save(imagem, os.path.join(save_path, filename))
    
    #os.remove(os.path.join("temp", filename))
    
    #imagem = pygame.image.load(save_path + filename).convert()
    return imagem, True




"""for i in range(len(pygame.camera.list_cameras())):
    camera = pygame.camera.Camera(pygame.camera.list_cameras()[i], camera_res)
    try:
        camera.start()  # Tenta iniciar a camera
    except pygame.error:
        print("Failed to connect")
        continue
    
    print(f"Connected to camera {i}")
    break"""

############################### Carrega as configurações do xml
camera_index, camera_res, desired_fps, animation_time = read_config("config.xml")
###############################

############################## Inicia pygame e a camera
pygame.init()
pygame.camera.init()
##############################
clock = pygame.time.Clock()
############################## seleciona a camera e starta
camera = pygame.camera.Camera(pygame.camera.list_cameras()[camera_index], camera_res)
camera.start() 
############################## Janela em fullscreen e resolução da janela
screen_res = (1920, 1080)
#screen = pygame.display.set_mode((0, 0), screen_res)
#screen_res = screen.get_size()pygame.FULLSCREEN)

screen = pygame.display.set_mode(screen_res, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.SCALED | pygame.NOFRAME)
pygame.display.set_mode(screen_res, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.SCALED | pygame.NOFRAME)
# ############################## Carrega o overlay da camera e redimensiona
cam_overlay = pygame.image.load("assets/overlay.png").convert_alpha()
#cam_overlay = pygame.transform.scale(cam_overlay, screen_res)
############################## Carrega o overlay da foto e redimensiona
overlay = pygame.image.load("assets/overlay2.png").convert_alpha()
#overlay = pygame.transform.scale(overlay, camera_res) # redimensiona para a resolução da camera, resolução da foto
################################################################
save_path="Fotos Massa/"

#pygame.display.set_caption("Camera Capture")
#screen = pygame.display.set_mode(screen_res, pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN)

overlay_surface = pygame.Surface(screen_res, pygame.SRCALPHA)
overlay_surface.blit(cam_overlay, (0, 0))

while True:
    clock.tick(desired_fps)

    scaled_capture = pygame.transform.scale(camera.get_image(), screen_res)
    
    screen.blit(scaled_capture, (0, 0))
    screen.blit(overlay_surface, (0, 0))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                filename = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S Massa-festa-pinhao.png")
                imagem, edited = editImage(camera.get_image(), overlay, filename, save_path)


                if edited:
                    
                    imagem = pygame.transform.scale(imagem, screen_res)

                    screen.blit(imagem, (0, 0))
                    pygame.display.flip()
                    
                    show_image = True
                    
                    while show_image == True:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    show_image = False
                                    break

                                elif event.key == pygame.K_ESCAPE:
                                    camera.stop()
                                    pygame.quit()
                                    sys.exit()

            elif event.key == pygame.K_ESCAPE:
                camera.stop()
                pygame.quit()
                sys.exit()
