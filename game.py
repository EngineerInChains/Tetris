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

#Constants joc
HEIGHT = 600
SENSE_HEIGHT = 580
WIDTH = 360

#Crecio Board
b = board.board(WIDTH,HEIGHT,'Tetris')
#Primera Peça
b.create_piece()




#Bucle Principal del Joc(Aixo va tot el rato i d'aqui se surt a fer cusas)
while True:
    
    #Bucle per comprovar si la llibreria ha detectat algun event
    for event in pygame.event.get():
        
        #Tecles
        if event.type == KEYDOWN:
            
            #Left
            if event.key == K_LEFT:
                b.move_active('l')
            
            #Right
            elif event.key == K_RIGHT:
                b.move_active('r')
            
            #Down
            elif event.key == K_DOWN:
                b.move_active('d')
            
            #Space
            elif event.key== K_SPACE:
                b.move_active('dd')
            
            #R
            elif event.key == K_r:
                b.rotate_active()
                
        if event.type == QUIT:
            pygame.quit()
            exit()
            
    #Update Board(move down)
    b.update_board()
    
    #Draw Board
    b.draw_board()
    
    #Update Display
    pygame.display.update()
    
    #Difficulty setting
    diff = 0.0002
    delay = 0.3
    #Sleep perque no es torni locatis
    if b.get_score() != 0:
        score = b.get_score()**2
        time.sleep(delay-b.get_score()*diff)
    else:
        time.sleep(delay)
   
    

        
        
        