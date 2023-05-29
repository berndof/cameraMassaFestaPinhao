import pygame
import pygame.camera

import os
import time
import datetime
import sys

pygame.init()
pygame.camera.init()

class Capture():
    def __init__(self):

        self.clock = pygame.time.Clock()
        self.rate = 30

        self.camera_res = (913, 512)
        self.camera_full_res = (1280, 720)

        self.camera = pygame.camera.Camera(pygame.camera.list_cameras()[0], self.camera_res)
        self.camera2 = pygame.camera.Camera(pygame.camera.list_cameras()[0], self.camera_full_res)
        
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) # Inicia uma janela em tela cheia
        self.screen_res = self.screen.get_size() # Pega a resolução da janela = resolução máxima do monitor

        self.cam_overlay = pygame.image.load("assets//overlay.png").convert_alpha() # carrega o overlay da pasta overlay
        self.cam_overlay = pygame.transform.smoothscale(self.cam_overlay, self.screen_res)# redimennsiona para o tamanho da tela

        self.loadscreen = pygame.image.load("assets//loadscreen.png").convert() # carrega o overlay da pasta overlay
        self.loadscreen = pygame.transform.smoothscale(self.loadscreen, self.screen_res)

        self.overlay = pygame.image.load("assets//overlay2.png").convert_alpha() # carrega o overlay da pasta overlay
        self.overlay = pygame.transform.smoothscale(self.overlay, self.camera_full_res)

        self.snapshot = pygame.surface.Surface(self.screen_res, 0, self.screen)
        self.picture = pygame.surface.Surface(self.screen_res, 0, self.screen)

        self.animationTime = 250 #ms

    def close(self):
        self.camera.stop()
        self.camera2.stop()
        pygame.quit()
        sys.exit()

    def takePicture(self):
        self.connectCam2()
        self.filename = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S Massa-festa-pinhao.png" )
        self.picture = self.camera2.get_image()
        self.picture.blit(self.overlay, (0,0))

        pygame.image.save(self.picture, os.path.join("Fotos Massa", self.filename))
        self.screen.blit(pygame.transform.smoothscale(self.picture, self.screen_res), (0,0))

        pygame.display.flip()
        self.taked = True
        self.connectCam1()
        while self.taked == True:
            for event in pygame.event.get(): 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.video()
                    elif event.key == pygame.K_ESCAPE:
                        self.close()

    def animate(self):
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < self.animationTime:
            if pygame.time.get_ticks() % 100 < 50:
                self.screen.fill((255, 255, 255))
                pygame.display.flip()
            else:
                self.screen.fill((0, 0, 0))
                pygame.display.flip()
                
        self.screen.blit(self.loadscreen, (0,0))
        pygame.display.flip()
        time.sleep(2) 

    def connectCam1(self):
        self.camera2.stop()
        self.camera.start()

    def connectCam2(self):
        self.camera.stop()
        self.camera2.start()
        self.animate()

    def video(self):
            self.connectCam1()

            while True:
        
                self.snapshot = pygame.transform.smoothscale(self.camera.get_image(), self.screen_res)
                self.snapshot.blit(pygame.transform.smoothscale(self.cam_overlay, self.screen_res), (0,0))
        
                self.screen.blit(self.snapshot, (0,0))
        
                for event in pygame.event.get(): 
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.takePicture()
                        elif event.key == pygame.K_ESCAPE:
                            self.close()

                pygame.display.flip()
                self.clock.tick(self.rate)


if __name__ == "__main__":

    capture = Capture()  # Cria uma instância da classe Capture
    capture.video()
