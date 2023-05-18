import pygame
import pygame.camera

import os
import time
import datetime
import sys

import xml.etree.ElementTree as ET
from PIL import Image

pygame.init()
pygame.camera.init()

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

# Carrega as configurações do arquivo XML
config_filename = "config.xml"
camera_index, camera_res, desired_fps, animation_time = read_config(config_filename)

"""for i in range(len(pygame.camera.list_cameras())):
    camera = pygame.camera.Camera(pygame.camera.list_cameras()[i], camera_res)
    try:
        camera.start()  # Tenta iniciar a camera
    except pygame.error:
        print("Failed to connect")
        continue
    
    print(f"Connected to camera {i}")
    break"""

camera = pygame.camera.Camera(pygame.camera.list_cameras()[camera_index], camera_res)
camera.start() 

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_res = screen.get_size()

cam_overlay = pygame.image.load("assets/overlay.png").convert_alpha()
cam_overlay = pygame.transform.scale(cam_overlay, screen_res)

def editImage(imagem, filename):
    save_path = "Fotos Massa//"
    imagem = Image.open(imagem)
    
    overlay = Image.open("assets/overlay2.png")
    overlay = overlay.resize(imagem.size)
    
    imagem.paste(overlay, (0, 0), overlay)
    imagem.save(save_path + filename)
    
    os.remove(os.path.join("temp", filename))
    
    imagem = pygame.image.load(save_path + filename).convert()
    
    return imagem, True

clock = pygame.time.Clock()

while True:
    clock.tick(desired_fps)

    capture = camera.get_image()
    scaled_capture = pygame.transform.scale(capture, screen_res)

    screen.blit(scaled_capture, (0, 0))
    screen.blit(cam_overlay, (0, 0))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                filename = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S Massa-festa-pinhao.png")
                pygame.image.save(capture, os.path.join("temp", filename))

                start_time = pygame.time.get_ticks()

                while pygame.time.get_ticks() - start_time < animation_time:
                    if pygame.time.get_ticks() % 100 < 50:
                        screen.fill((255, 255, 255))
                    else:
                        screen.fill((0, 0, 0))

                    pygame.display.flip()
                    pygame.time.wait(1)

                imagem, edited = editImage(imagem=os.path.join("temp", filename), filename=filename)

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

                                elif event.key == pygame.K_ESCAPE:
                                    camera.stop()
                                    pygame.quit()
                                    sys.exit()

            elif event.key == pygame.K_ESCAPE:
                camera.stop()
                pygame.quit()
                sys.exit()
