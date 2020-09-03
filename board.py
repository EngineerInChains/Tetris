# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 15:45:16 2020

@author: Miki
"""

import random
import pygame
from Peca import *



class board():
    def __init__(self,sizeX,sizeY,caption,silent):
        
        
        self.sizeX = sizeX
        self.sizeY = sizeY
        if not silent:
            #Creacio superficie on es pinta (anchura i altura) 
            self.displaysurface = pygame.display.set_mode((sizeX, sizeY))
            
            
            #Titol de la pantalla
            pygame.display.set_caption(caption)
        
        
        self.lim_z = sizeY
        
        self.lim_x_min = 0
        self.lim_x_max = sizeX-20*8
        
        self.score = 0
        self.active_p = ""
        
        self.font = pygame.font.SysFont(None, 24)
        self.stop_active = False
        self.stop_active_space = False
        
        self.extra_blocks = np.array([[-100,-100,-1]])
        
        self.colors = {0: (242, 242, 82),1: (114, 230, 232),2: (171, 64, 237),3: (64, 237, 73),
                  4: (235, 48, 23),5: (235, 150, 23),6: (27, 23, 235)}
        
        self.next_piece_pos = {"sq": [self.sizeX-20-50,115],'li': [self.sizeX-20-50,135],'T': [self.sizeX-20-50,125],'S': [self.sizeX-20-50,105],'Z': [self.sizeX-20-50,105],'L': [self.sizeX-20-50,110],'J': [self.sizeX-20-50,110]}
        self.types = ["sq",'li','T','S','Z','L','J']
        self.next_p = random.choice(self.types)
        self.lost = False
        self.next_p_draw = ""
    def create_piece(self):
           
        self.stop_active = False
        self.stop_active_space = False
        typ = self.next_p
        self.next_p = random.choice(self.types)
        
        while self.next_p == typ:
            self.next_p = random.choice(self.types)
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
        
        self.next_p_draw = piece(self.next_p,self.next_piece_pos[self.next_p][0],self.next_piece_pos[self.next_p][1],angle,self.colors[d[self.next_p]],self.lim_z,self.lim_x_min,self.lim_x_max)
        self.active_p = piece(typ,posX,posY,angle,color,self.lim_z,self.lim_x_min,self.lim_x_max)
        
    def rotate_active(self):
        if not self.stop_active:
            self.active_p.rot(False)
            if self.touch_side('l') or self.touch_side('r') or self.touch_piece() or self.touch_down():
                self.active_p.rot(True)
            
    
    def move_active(self,side):
        if not self.stop_active:
            if side=='l':
                self.active_p.moveside(side,20)
                if self.touch_side(side) or self.touch_piece():
                    self.active_p.moveside('r',20)
                    
            elif side=='r':
                self.active_p.moveside(side,20)
                if self.touch_side(side) or self.touch_piece():
                    self.active_p.moveside('l',20)
                    
            elif side == 'd':
                self.active_p.moveDown(20)
                down = self.touch_down()
                if down or self.touch_piece():
                    
                    self.active_p.moveUp(20)
                    self.stop_active = True
                    
            elif side=='dd':
                if not self.stop_active_space:
                    self.active_p.moveDown(40)
                    down = self.touch_down()
                    if down or self.touch_piece():
                        
                        self.active_p.moveUp(40)
                        if down:
                            self.stop_active_space = True
                   
    def get_piece_type(self):
        d = {"sq":0,'li':1,'T':2,'S':3,'Z':4,'L':5,'J':6}
        return d[self.active_p.type]
                        
    def get_piece_pos(self):
        return self.active_p.get_center()
    def get_extra_blocks(self):
        return self.extra_blocks
    def get_piece_angle(self):
        return self.active_p.get_angle()
            
    def get_piece_blocks(self):
        return self.active_p.get_blocks()
        
    def get_score(self):
        return self.score
        
    def update_board(self):
        #Per cada peça
        
            
           
            if not self.stop_active:
                self.move_active('d')
            else:
                lines,b = self.is_line(self.sizeY)
                
                blocks = self.active_p.get_blocks()
                
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
    
    #Comprovo si algun dels blocks ha arribat al limit que es passa per parametre
    #Esquema de bucle de cerca caca avorrida.
    #Actualitza la variable stop per a saber despres si ta parao
    def is_lost(self):
        if self.active_p != "" and len(self.extra_blocks) >1:
            b = self.active_p.get_blocks()
            aux = np.any(b[:,1]<20)
            aux2 = self.touch_piece()
            return aux and aux2
        else:
            return False
    def touch_down(self):
        i = 0
        
        
        blocks = self.active_p.get_blocks()
        
        b = np.any((blocks[:,1]+block_side)>=self.lim_z)
        return b
             
    
    def touch_piece(self):
        blocks = self.active_p.get_blocks()
        touch = False
        i = 0
        while not touch and i < len(blocks):
            j = 1
            while not touch and j <len(self.extra_blocks):
                if blocks[i][0] == self.extra_blocks[j][0] and blocks[i][1] == self.extra_blocks[j][1]:
                    touch = True
                else:
                    j = j+1
           
            i = i+1
        return touch
    
    def is_line(self,height):
        lines = []
        b = False
        blocks = self.active_p.get_blocks()
        if len(self.extra_blocks)>0:
            for line in range(0,height,block_side):
                b1_line = blocks[blocks[:,1]==line]
                b2_line = self.extra_blocks[self.extra_blocks[:,1]==line]
                if len(b1_line)+len(b2_line)==10:
                    b = True
                    lines.append(line)
        
        return lines,b 
    
    def touch_side(self,side):
        
        blocks = self.active_p.get_blocks()
        if side == 'l':
            is_bad = np.any(blocks[:,0]<=self.lim_x_min)
        else:
            is_bad = np.any(blocks[:,0]>self.lim_x_max)
            
        return is_bad    
                
                
    def draw_board(self):
        self.displaysurface.fill((0,0,0))
        self.grid_draw()
        if not self.is_lost():
            size = 20
            pygame.draw.line(self.displaysurface,(150,150,150),(size/2-1,0),(size/2-1,self.sizeY-size),size+1)
            pygame.draw.line(self.displaysurface,(150,150,150),(0,self.sizeY-size/2),(self.sizeX,self.sizeY-size/2),size)
            ol_size = size
            size = size *7
            pygame.draw.line(self.displaysurface,(150,150,150),(self.sizeX-size/2,self.sizeY-ol_size),(self.sizeX-size/2,0),size)
            
            pygame.draw.rect(self.displaysurface,(0,0,0),pygame.Rect(self.sizeX-20-100,0+20,80,25))
            
            
            img = self.font.render(str(self.score), True, (255,255,255))
            self.displaysurface.blit(img, (self.sizeX-20-95,0+25))
            
            img = self.font.render("Next Piece:", True, (0,0,0))
            self.displaysurface.blit(img, (self.sizeX-20-100,0+60))
            
            pygame.draw.rect(self.displaysurface,(0,0,0),pygame.Rect(self.sizeX-20-100,0+80,100,80))
            self.next_p_draw.draw(self.displaysurface)
            
            for b in self.extra_blocks[1:]:
                x = b[0]
                y = b[1]
                r1 = pygame.Rect(x,y,block_side,block_side)
                r2 = pygame.Rect(x+2,y+2,block_border_side,block_border_side)
                pygame.draw.rect(self.displaysurface,self.colors[b[2]],r1)
                #Borde Negre de tamany 2
                pygame.draw.rect(self.displaysurface,(0,0,0),r2,3)
            
            self.active_p.draw(self.displaysurface)
        else:
            img = self.font.render("YOU LOST", True, (255,255,255))
            self.displaysurface.blit(img, (self.sizeX/2,self.sizeY/2))
        
        #Funcio que realment fa els canvis a la pantalla(com un enviar)
             
            
    def grid_draw(self):
        grid_color = (70, 70, 70)
        for i in range(11):
            x=block_side * i
            pygame.draw.line(self.displaysurface,grid_color,(x,0),(x,600))
        
        for i in range(30):
            y=block_side * i
            pygame.draw.line(self.displaysurface,grid_color,(0,y),(360,y))
            
        