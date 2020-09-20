# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 21:42:04 2020

@author: Miki
"""
#imports tontos
import pygame
import numpy as np
from pygame.math import Vector2
from dibuixos_peces import get_piece_pos

block_side = 20

block_border_side = 15


        
        
#Peça de Tetris!! :)
class piece:
    #Inicialitzacio, se li passa: 
    #   -El tipus de la peça(quadrat,linia,....)
    #   -El centre de rotacio en X
    #   -El centre de rotacio en Y
    #   -L'angle inicial
    #   -Colorsito(RGB)
    def __init__(self,typ,rotX,rotY,initangle,color,limit_z,lim_x_min,lim_x_max):
        
        #Res interessant son tot assignacions
        self.color =color
        
        self.type = typ
        
        self.d = {"sq":0,'li':1,'T':2,'S':3,'Z':4,'L':5,'J':6}
        
        
        self.rot_center_X = rotX
        self.rot_center_Y = rotY
        
        self.angle = initangle
        
        self.lim_z = limit_z
        self.lim_x_min = lim_x_min
        self.lim_x_max = lim_x_max
        
        
        self.blocks = get_piece_pos(self.type,self.rot_center_X,self.rot_center_Y,self.angle)
            

        
    def get_blocks(self):
        return self.blocks
    def get_angle(self):
        return self.angle
    def get_center(self):
        return [self.rot_center_X,self.rot_center_Y]
    
    
    def moveside(self,side,desp):
                  
        if side=='l':
            self.rot_center_X = self.rot_center_X-desp
            
            for i in range(len(self.blocks)):
                self.blocks[i][0] = self.blocks[i][0]-desp
            
        else:
            self.rot_center_X = self.rot_center_X+desp
            
            for i in range(len(self.blocks)):
                self.blocks[i][0] = self.blocks[i][0]+desp
               
    
    #Si t'has llegit aixo despres del update crec que no sera problema :)
    #Se li dona un desplaçament i canvia el centre de rotacio cap avajo i 
    # passa per cadascun dels blocks moventlos tambe
    def moveDown(self,desp):
                    
            self.rot_center_Y = self.rot_center_Y+desp
            
            for i in range(len(self.blocks)):
                    self.blocks[i][1] = self.blocks[i][1]+desp
    def moveUp(self,desp): 
            
            self.rot_center_Y = self.rot_center_Y-desp
            
            for i in range(len(self.blocks)):
                    self.blocks[i][1] = self.blocks[i][1]-desp
            
            
          
    #Aquesta es la part cuki de la rotació jeje, aqui nomes es canvia 
    # l'angle i s'envia la feina al update
    def rot(self,revert):
        if not revert:
            self.angle = self.angle+90
            if self.angle ==360:
                self.angle = 0
                
            self.blocks = get_piece_pos(self.type,self.rot_center_X,self.rot_center_Y,self.angle)
        else:
            if self.angle == 0:
                self.angle = 360 
            self.angle = self.angle-90
            self.blocks = get_piece_pos(self.type,self.rot_center_X,self.rot_center_Y,self.angle)
       
                
                
    #Cosa mes simple no hi ha, crida al draw dels blocks
    def draw(self,surf):
        
        for b in self.blocks:
            
            x = b[0]
            y = b[1]
            r1 = pygame.Rect(x,y,block_side,block_side)
            r2 = pygame.Rect(x+2,y+2,block_border_side,block_border_side)
            pygame.draw.rect(surf,self.color,r1)
            #Borde Negre de tamany 2
            pygame.draw.rect(surf,(0,0,0),r2,3)
    
            
            
        
                
            