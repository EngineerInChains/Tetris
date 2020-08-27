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
    def __init__(self,typ,rotX,rotY,initangle,color,limit_z,lim_x_min,lim_x_max,extra_blocks):
        
        #Res interessant son tot assignacions
        self.color =color
        self.type = typ
        p1 = [0,0]
        self.extra_blocks = extra_blocks
        self.blocks = np.array([p1,p1,p1,p1])
        self.rot_center_X = rotX
        self.rot_center_Y = rotY
        self.angle = initangle
        self.lim_z = limit_z
        self.lim_x_min = lim_x_min
        self.lim_x_max = lim_x_max
        self.stop_rot = False
        self.stop = False
        self.update_sprite()
        
        
    #Forçar el centre de rotació de la peça on tu vulguis(moure la peça vamos)   
    def set_center(self,c_x,c_y):
        #En X
        self.rot_center_X = c_x
        #En Y
        self.rot_center_Y = c_y
        #ui mira qui surt per aqui, un altre cop s'ha de fer update al sprite
        self.update_sprite()
    
    #Funcio magica que resol els problemes de la vida(dels blocks) i sobre 
    #la qual s'expliquen llegendes en la part alta de la codificació. 
    #Per entendrens, dona vida als blocks, els crea, i els hi dona color. Com Jesus Vamos.
    #Utilitza la posició i l'angle de la peça i  a partir d'aqui explico serio 
    def update_sprite(self):
        
        #Assignem centre per no escriure tant :P
        center_x = self.rot_center_X
        center_y = self.rot_center_Y
        self.blocks = get_piece_pos(self.type,center_x,center_y,self.angle)
        
    def get_blocks(self):
        return self.blocks
    
    def is_side(self,side):
        i = 0
        is_ok = True
        if side == 'l':
            while is_ok and i < len(self.blocks):
                b = self.blocks[i]
                
                if b[0] <= self.lim_x_min:
                    is_ok = False
                i = i+1
        else:
            while is_ok and i < len(self.blocks):
                b = self.blocks[i]
                
                if b[0] > self.lim_x_max:
                    is_ok = False
                i = i+1
        return not is_ok
    
    def moveside(self,side,desp):
        r = False
        if not self.stop:
            center_x_ant = self.rot_center_X
            if side=='l':
                self.rot_center_X = self.rot_center_X-desp
            else:
                self.rot_center_X = self.rot_center_X+desp
            
            self.update_sprite()
            
            if self.is_side(side):
                self.rot_center_X = center_x_ant
                self.update_sprite()
            else:
                r=True
        return r
    
    
    #Si t'has llegit aixo despres del update crec que no sera problema :)
    #Se li dona un desplaçament i canvia el centre de rotacio cap avajo i 
    # passa per cadascun dels blocks moventlos tambe
    def moveDown(self,desp):
        r = False
        if not self.stop:
            center_Y_ant = self.rot_center_Y
            
            self.rot_center_Y = self.rot_center_Y+desp
            
            self.update_sprite()
            
            if self.is_bottom():
                self.rot_center_Y = center_Y_ant
                self.update_sprite()
            else:
                r=True
        return r
    
    #Aquesta es la part cuki de la rotació jeje, aqui nomes es canvia 
    # l'angle i s'envia la feina al update
    def rot(self):
        last_angle = self.angle
        r = False
        self.angle = self.angle+90
        if self.angle ==360:
            self.angle = 0
        self.update_sprite()
       
        if self.is_side('l') or self.is_side('r') or self.is_bottom() or self.stop:
                self.angle = last_angle
                self.update_sprite()
                self.stop_rot =True
        else:
            if self.stop_rot:
                self.stop_rot = False
            r = True
        return r
                
        
    
    def is_stop(self):
        return self.stop
    #Comprovo si algun dels blocks ha arribat al limit que es passa per parametre
    #Esquema de bucle de cerca caca avorrida.
    #Actualitza la variable stop per a saber despres si ta parao
    
    def is_bottom(self):
        i = 0
        
        self.stop = False
        while not self.stop and i < len(self.blocks):
            b = self.blocks[i]
            if (b[1]+block_side)<self.lim_z:
                j = 0
                while not self.stop and j < len(self.extra_blocks):
                    
                    s = self.extra_blocks[j]
                    
                    if b[0]==s[0] and b[1]==s[1]:
                        self.stop = True
                    
                    j = j+1
            else:
                self.stop = True
            i = i+1
        return self.stop
            
    def is_line(self,height,block_s):
        lines = []
        b = False
        if len(self.extra_blocks)>0:
            for line in range(0,height,block_s):
                b1_line = self.blocks[self.blocks[:,1]==line]
                b2_line = self.extra_blocks[self.extra_blocks[:,1]==line]
                if len(b1_line)+len(b2_line)==10:
                    b = True
                    lines.append(line)
        
        return lines,b     
            
                
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
    
            
            
        
                
            