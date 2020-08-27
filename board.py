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
        self.lim_z = sizeY
        #self.lim_x_min = 0+20
        #self.lim_x_max = sizeX-20*9
        self.lim_x_min = 0
        self.lim_x_max = sizeX-20*8
        self.pieces = []
        self.score = 0
        self.active_p = -1
        self.font = pygame.font.SysFont(None, 24)
        self.stopped = {}
        self.extra_blocks = np.array([[-100,-100,-1]])
        self.colors = {0: (242, 242, 82),1: (114, 230, 232),2: (171, 64, 237),3: (64, 237, 73),
                  4: (235, 48, 23),5: (235, 150, 23),6: (27, 23, 235)}
        self.types = ["sq",'li','T','S','Z','L','J']
        self.lost = False
        
    def create_piece(self):
           
        
        typ = random.choice(self.types)     
        #typ='sq'
        
        if typ == 'sq' or typ == 'li' :
            posX = 140
            posY = 20
        else :
            posX = 150
            posY=10
        
        angle = 0
        d = {"sq":0,'li':1,'T':2,'S':3,'Z':4,'L':5,'J':6}
        color = self.colors[d[typ]]
        
        
        self.pieces.append(piece(typ,posX,posY,angle,color,self.lim_z,self.lim_x_min,self.lim_x_max,self.extra_blocks))
        self.active_p = self.active_p + 1
        
    def rotate_active(self):
        self.pieces[self.active_p].rot()
    
    def move_active(self,side):
        r = False
        if side!='d' and side != 'dd':
            r = self.pieces[self.active_p].moveside(side,20)
        elif side == 'd':
            r = self.pieces[self.active_p].moveDown(20)
        elif side=='dd':
            r=self.pieces[self.active_p].moveDown(40)
        return r
    def get_score(self):
        return self.score
        
    def update_board(self):
        #Per cada peça
        
            #Si no ha arribat avall
            if self.pieces[self.active_p].is_lost():
                print("LOST GAME")
                self.lost =True
            if not self.pieces[self.active_p].is_stop():
                r = self.pieces[self.active_p].moveDown(20)
            else:
                lines,b = self.pieces[self.active_p].is_line(self.sizeY,20)
                
                blocks = self.pieces[self.active_p].get_blocks()
                if b:
                    for line in lines:
                        self.score = self.score + 10
                        blocks = blocks[blocks[:,1] != line]
                        aux_blocks = blocks[:,1]<= line
                        self.extra_blocks = self.extra_blocks[self.extra_blocks[:, 1] != line]
                        aux_extra = self.extra_blocks[:,1]<= line
                        blocks[aux_blocks,1]= blocks[aux_blocks,1]+20
                        self.extra_blocks[aux_extra,1] = self.extra_blocks[aux_extra,1]+20
                        
                self.extra_blocks = np.vstack((self.extra_blocks,blocks))
                self.create_piece()
            
                
                
                
    def draw_board(self):
        self.displaysurface.fill((0,0,0))
        if not self.lost:
            size = 20
            pygame.draw.line(self.displaysurface,(150,150,150),(size/2-1,0),(size/2-1,self.sizeY-size),size+1)
            pygame.draw.line(self.displaysurface,(150,150,150),(0,self.sizeY-size/2),(self.sizeX,self.sizeY-size/2),size)
            ol_size = size
            size = size *7
            pygame.draw.line(self.displaysurface,(150,150,150),(self.sizeX-size/2,self.sizeY-ol_size),(self.sizeX-size/2,0),size)
            
            pygame.draw.rect(self.displaysurface,(0,0,0),pygame.Rect(self.sizeX-20-100,0+20,80,25))
            
            
            img = self.font.render(str(self.score), True, (255,255,255))
            self.displaysurface.blit(img, (self.sizeX-20-95,0+25))
            
            for b in self.extra_blocks[1:]:
                x = b[0]
                y = b[1]
                r1 = pygame.Rect(x,y,block_side,block_side)
                r2 = pygame.Rect(x+2,y+2,block_border_side,block_border_side)
                pygame.draw.rect(self.displaysurface,self.colors[b[2]],r1)
                #Borde Negre de tamany 2
                pygame.draw.rect(self.displaysurface,(0,0,0),r2,3)
            
            self.pieces[self.active_p].draw(self.displaysurface)
        else:
            img = self.font.render("YOU LOST", True, (255,255,255))
            self.displaysurface.blit(img, (self.sizeX/2,self.sizeY/2))
        
        #Funcio que realment fa els canvis a la pantalla(com un enviar)
        