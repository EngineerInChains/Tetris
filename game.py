# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 21:27:37 2020

@author: Miki
"""
import pygame
from pygame.locals import *
from Peca import piece

pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional
 
HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")


a = piece("sq")
a.gen_piece(200,0)

 
while True:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            
        
    
    displaysurface.fill((0,0,0))
    a.draw(displaysurface)
    
 
    pygame.display.update()
    FramePerSec.tick(FPS)
    

        
        
        