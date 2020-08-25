# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 21:27:37 2020

@author: Miki
@shadow :P : Kaviga
"""


#imports
import pygame
from pygame.locals import *
import board
import time
import random

#Funcio que em demanen que posi(la llibreria)
pygame.init()

HEIGHT = 800
SENSE_HEIGHT = 780
WIDTH = 600


b = board.board(WIDTH,HEIGHT,'Tetris')

b.create_piece()


#b.rotRight()zz

#Bucle Principal del Joc(Aixo va tot el rato i d'aqui se surt a fer cusas)
while True:
    
    #Bucle per comprovar si la llibreria ha detectat 
    # algun event(Aqui agafarem el fet que apretis una tecla, de moment nomes quit)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                b.move_active(0)
            elif event.key == K_RIGHT:
                b.move_active(1)
            elif event.key == K_DOWN:
                b.move_active(2)
            elif event.key== K_SPACE:
                b.move_active(3)
            if event.key == K_r:
                b.rotate_active() 
        if event.type == QUIT:
            pygame.quit()
            exit()
    b.update_board()
    b.draw_board()
    
    
    
    pygame.display.update()
    #Sleep perque no es torni locatis
    time.sleep(0.3)
   
    

        
        
        