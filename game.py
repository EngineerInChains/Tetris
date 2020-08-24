# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 21:27:37 2020

@author: Miki
"""


#imports
import pygame
from pygame.locals import *
from Peca import piece
import time

#Funcio que em demanen que posi(la llibreria)
pygame.init()

HEIGHT = 450
SENSE_HEIGHT = 430
WIDTH = 400

#Creacio superficie on es pinta (anchura i altura) 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
#Titol de la pantalla
pygame.display.set_caption("Tetris")

pieces = []
#Creo dos peces random per provar
a = piece("example",200,20,0,(255,0,0))
pieces.append(a)
b = piece('li',100,100,0,(5,200,0))
pieces.append(b)


#TODO: Definir una altra que sigui una T per exemple

#b.rotRight()

#Bucle Principal del Joc(Aixo va tot el rato i d'aqui se surt a fer cusas)
while True:
    
    #Bucle per comprovar si la llibreria ha detectat 
    # algun event(Aqui agafarem el fet que apretis una tecla, de moment nomes quit)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
            
    #Neteja Pantalla abans de dibuixar(Si no ho fes i un objecte es 
    # mogues, es dibuixaria 2 cops)
    displaysurface.fill((0,0,0))
    
    #Per cada peça
    for p in pieces:
        #Si no ha arribat avall
        if not p.is_bottom(SENSE_HEIGHT):
            #Es mou avall i rota(perque em don la gana)
            p.moveDown(10)
            p.rotRight()
    
        p.draw(displaysurface)
    
    #Funcio que realment fa els canvis a la pantalla(com un enviar)
    pygame.display.update()
    #Sleep perque no es torni locatis
    time.sleep(1)
   
    

        
        
        