import pygame
import pygame.camera

import os
import time
import datetime

from PIL import Image
#import cv2

pygame.init()
pygame.camera.init()

pygame.camera.list_cameras()

for i in range(len(pygame.camera.list_cameras())):
    camera = pygame.camera.Camera(pygame.camera.list_cameras()[i])
    try:
        camera.start()  # try to start the camera
    except pygame.error:
        print("Failed to connect")
        # if starting the camera raises a pygame.error exception, continue to the next camera
        continue
    print(f"Connected to camera {i}")
    break  # if camera is successfully started, break out of the loop

camera_res = (1280, 720)

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen_res = screen.get_size()

cam_overlay = pygame.image.load("overlay\overlay.png").convert_alpha()
cam_overlay = pygame.transform.scale(cam_overlay, screen_res)

def editImage(imagem, filename):
    save_path = "edited\\"

    imagem = Image.open(imagem)
    
    overlay = Image.open("overlay\overlay2.png")
    overlay = overlay.resize((imagem.size))
    
    imagem.paste(overlay, (0,0), overlay)
    imagem.save(save_path + f"edited-{filename}")
    
    os.remove(os.path.join("pictures", filename))
    
    imagem = pygame.image.load(save_path + f"edited-{filename}")
    
    return imagem, True


while True:

    capture = camera.get_image()

    
    scaled_capture = pygame.transform.scale(capture, screen_res)
    
    screen.blit(scaled_capture, (0,0))
    screen.blit(cam_overlay, (0,0))
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                filename = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S Massa-festa-pinhao.png" )
                pygame.image.save(capture , os.path.join("pictures", filename))
                
                # Save the current time in milliseconds
                start_time = pygame.time.get_ticks()
                # Define the total time for the animation in milliseconds
                animation_time = 150
                # Create a loop that runs while the animation time hasn't elapsed
                while pygame.time.get_ticks() - start_time < animation_time:
                    # Alternate between displaying a white and black screen
                    if pygame.time.get_ticks() % 100 < 50:
                        screen.fill((255, 255, 255))
                    else:
                        screen.fill((0, 0, 0))
                    pygame.display.flip()
                    pygame.time.wait(50)
                
                imagem, edited = editImage(imagem = os.path.join("pictures", filename), filename = filename)
                if edited:
                    
                    imagem = pygame.transform.scale(imagem, screen_res)
                    screen.blit(imagem, (0,0))
                    pygame.display.flip()
                    time.sleep(4)
                    
                
                    if event.key == pygame.K_ESCAPE:
                        camera.stop()
                        pygame.quit()
                        exit()
                
                
                
                
            elif event.key == pygame.K_ESCAPE:
                camera.stop()
                pygame.quit()
                exit()