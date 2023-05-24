import cv2
import pygame
import numpy as np
import sys 

from PIL import Image
import os
import datetime

screen_res = (1280, 720)

# Pygame
pygame.init()
screen = pygame.display.set_mode((screen_res[0],screen_res[1]), pygame.FULLSCREEN)
clock = pygame.time.Clock()
######################################

######################################
# Camera
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 913)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)
cam.set(cv2.CAP_PROP_FPS, 30)
######################################

######################################
# Carregando overlays 
cam_overlay = pygame.image.load("assets//overlay.png").convert_alpha()
cam_overlay = pygame.transform.scale(cam_overlay, screen_res)

loadscreen = pygame.image.load('assets//loadscreen.png')
loadscreen = pygame.transform.scale(loadscreen, screen_res)
######################################

######################################
def editImage(imagem, filename, screen_res = screen_res):

    imagem = Image.open(os.path.join("temp", filename))
    
    overlay = Image.open('assets//overlay2.png')
    overlay = overlay.resize(imagem.size)
    
    imagem.paste(overlay, (0, 0), overlay)
    imagem.save("Fotos Massa//" + filename)
    
    os.remove(os.path.join("temp", filename))
    
    imagem_py = pygame.image.load(os.path.join("Fotos Massa", filename)).convert()
    imagem_py = pygame.transform.scale(imagem_py, screen_res)

    return imagem_py, True

def frameProcess(frame, screen_res = screen_res):

    frame = cv2.resize(frame, screen_res, interpolation=cv2.INTER_AREA)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    frame = pygame.transform.flip(frame, True, False)
    screen.blit(frame, (0,0))
    screen.blit(cam_overlay, (0, 0))
    pygame.display.flip()

def checkClick():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                key = "space"
            elif event.key == pygame.K_ESCAPE:
                key = "esc"
            return key

ret, frame = cam.read()

if ret:
    while True:

        frameProcess(frame)

        clock.tick(30)
            
        ret, frame = cam.read()

        if checkClick() == "space":
            
            filename = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S Massa-festa-pinhao.png")
            
            start_time = pygame.time.get_ticks()

            while pygame.time.get_ticks() - start_time < 150:

                screen.fill((0, 0, 0))
                pygame.display.flip()
                pygame.time.wait(40)
                screen.fill((255, 255, 255))
                pygame.display.flip()
                pygame.time.wait(40)

                screen.blit(loadscreen,(0,0))
                pygame.display.flip()


                cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

                ret, imagem = cam.read()

                if ret:
                    cv2.imwrite(os.path.join("temp", filename), imagem)
                    imagem, show_image = editImage(imagem, filename)
                    screen.blit(imagem, (0,0))
                    pygame.display.flip()

                    while show_image == True:
                        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 913)
                        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)
                        if checkClick() == "space":
                            ret, frame = cam.read()
                            frameProcess(frame)
                            show_image = False

                        elif checkClick() == "esc":
                            cam.release()
                            pygame.quit()
                            sys.exit()

                elif checkClick() == "esc":
                    cam.release()
                    pygame.quit()
                    sys.exit()