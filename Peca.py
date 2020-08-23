# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 21:42:04 2020

@author: Miki
"""
import pygame

block_side = 100



#Sprite
class block(pygame.sprite.Sprite):
    
    #Inicialitzacio
    def __init__(self,posX,posY,color):
        
        
        super().__init__() 
        
        self.posX = posX
        self.posY = posY
        self.color = (255,255,255)
        self.sprit = pygame.Rect(posX,posY,block_side,block_side)
        
    def moveDown(self,desp):
        self.posY = self.posY+desp
        self.sprit = pygame.Rect(self.posX,self.posY,block_side, block_side)
        
    def draw(self,surf):
        pygame.draw.rect(surf,self.color,self.sprit)
        

class piece():
    def __init__(self,typ):
        
        self.color =(255,255,255)
        self.type = typ
        self.blocks = []
        self.rot_center_X = 0
        self.rot_center_Y = 0
        
    
    def gen_piece(self,posInitX,posInitY):
        
        self.rot_center_X = posInitX
        self.rot_center_Y = posInitY
        
        if self.type=='sq':
            self.blocks.append(block(posInitX-block_side,posInitY+block_side,self.color))
            self.blocks.append(block(posInitX,posInitY+block_side,self.color))
            self.blocks.append(block(posInitX-block_side,posInitY,self.color))
            self.blocks.append(block(posInitX,posInitY,self.color))
            
    def moveDown(self,desp):
        self.rot_center_Y = self.rot_center_Y+desp
        for b in self.blocks:
            b.moveDown(desp)
    
    def rotRight(self):
        pass  
    
    def draw(self,surf):
        for b in self.blocks:
            b.draw(surf)
    
            
            
        
                
            