# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 15:45:16 2020

@author: Miki
"""

import random
import pygame
from Peca import *
class board():
    def __init__(self,sizeX,sizeY,caption):
        
        
        self.sizeX = sizeX
        self.sizeY = sizeY
        #Creacio superficie on es pinta (anchura i altura) 
        self.displaysurface = pygame.display.set_mode((sizeX, sizeY))
        #Titol de la pantalla
        pygame.display.set_caption(caption)
        self.lim_z = sizeY-20
        #self.lim_x_min = 0+20
        #self.lim_x_max = sizeX-20*9
        self.lim_x_min = {'li':0+20,'sq':0+20,'J':0+20,'L':0+20,'S':0+20,'Z':0+20,'T':0+20}
        self.lim_x_max = {'li':sizeX-20*9,'sq':sizeX-20*9,'J':sizeX-20*9,'L':sizeX-20*9,'S':sizeX-20*9,'Z':sizeX-20*9,'T':sizeX-20*9}
        self.pieces = []
        self.score = 0
        self.active_p = -1
        self.stopped = {}
       
        
    def create_piece(self):
           
     
        typ = random.choice(["sq",'li','T','S','Z','L','J'])     
        #typ='li'
        
        if typ == 'sq' or typ == 'li' :
            posX = 200
            posY = 200
        else :
            posX = 210
            posY=190
        
        angle = 0
        color = random.choice(
            [(200, 0, 200),
            (0, 0, 200),
            (0, 200, 200),
            (0, 200, 0),
            (200,200,0),
            (200, 0, 0)])
        
        
        self.pieces.append(piece(typ,posX,posY,angle,color,self.lim_z,self.lim_x_min[typ],self.lim_x_max[typ]))
        self.active_p = self.active_p + 1
        
    def rotate_active(self):
        self.pieces[self.active_p].rotRight()
    
    def move_active(self,dir):
        r = True
        if dir==0:
            r = self.pieces[self.active_p].moveLeft(20)
        elif dir==1:
            r =self.pieces[self.active_p].moveRight(20)
        elif dir==2:
            r =self.pieces[self.active_p].moveDown(20)
        elif dir==3:
            r=self.pieces[self.active_p].moveDown(40)
        return r
        
    def update_board(self):
        #Per cada peça
        
            #Si no ha arribat avall
            if not self.pieces[self.active_p].is_stop():
                r = self.pieces[self.active_p].moveDown(20)
            else:
                self.create_piece()
                
                
    def into_board(self)      :   
        
        if self.pieces[self.active_p].is_stop():
            
                
            
                
                
                
    def draw_board(self):
        self.displaysurface.fill((0,0,0))
        size = 20
        pygame.draw.line(self.displaysurface,(150,150,150),(size/2-1,0),(size/2-1,self.sizeY-size),size+1)
        pygame.draw.line(self.displaysurface,(150,150,150),(0,self.sizeY-size/2),(self.sizeX,self.sizeY-size/2),size)
        ol_size = size
        size = size *7
        pygame.draw.line(self.displaysurface,(150,150,150),(self.sizeX-size/2,self.sizeY-ol_size),(self.sizeX-size/2,0),size)
        
        pygame.draw.rect(self.displaysurface,(0,0,0),pygame.Rect(self.sizeX-20-100,0+20,100,70))
        
        for p in self.pieces:
            p.draw(self.displaysurface)
        
        #Funcio que realment fa els canvis a la pantalla(com un enviar)
        