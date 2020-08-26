# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 21:42:04 2020

@author: Miki
"""
#imports tontos
import pygame
import numpy as np



block_side = 20

block_border_side = 16



#Block class(En principi no la has de tocar)
class block():
    
    #Inicialitzacio, se li passa posició inicial i un colorsito reshulon
    def __init__(self,posX,posY,color):

        #Assignacions varies
        self.posX = posX
        self.posY = posY
        self.color = color
        
    #Bastant selfexplanatory, se li dona un desplaçament i updatea les posicions i els sprites
    def moveRight(self,desp):
        self.posX = self.posX+desp
        
    def moveLeft(self,desp):
        self.posX = self.posX-desp
        
    def moveDown(self,desp):
        #Canviem la posicio del block
        self.posY = self.posY+desp
    
    #Dibuixa els dos rectangles (quadrats) dels que portem parlant una estona,
    #fa servir la funcio de pygame i necessita la superficie(matriu gran amb tot) per funcionar
    def draw(self,surf):
        #Rectangle Blanc
        r1 = pygame.Rect(self.posX,self.posY,block_side,block_side)
        r2 = pygame.Rect(self.posX,self.posY,block_border_side,block_border_side)
        pygame.draw.rect(surf,self.color,r1)
        #Borde Negre de tamany 2
        pygame.draw.rect(surf,(0,0,0),r2)
        
        
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
        self.blocks = np.zeros((4,2))
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
        
        #Neteja llista de blocks(es molt millorable ja que es podrien reutilitzar)
        self.blocks = []
        
        
        if self.type == 'example':
            #Un sol block centrat al centre i de color color
            self.blocks[0,0] = center_x-block_side/2
            self.blocks[0,1] = center_y-block_side/2
            
            
        elif self.type =='sq':
            #Als quadrats no els hi importa una merda si els rotes per tant tot va bé fins aqui
            #Pots aagafar com a centre (0,0) i fer els calculs per veure quin block es quin
            #Declaracio block:: block(posX,posY,color)
            self.blocks[0,0] = center_x-block_side
            self.blocks[0,1] = center_y
            
            self.blocks[1,0] = center_x
            self.blocks[1,1] = center_y
            
            self.blocks[2,0] = center_x
            self.blocks[2,1] = center_y-block_side
            
            self.blocks[3,0] = center_x-block_side
            self.blocks[3,1] = center_y-block_side
        
            
        elif self.type == 'li':
           
            if self.angle>= 0 and self.angle < 90 :
                
                self.blocks[0,0] = center_x-block_side*2
                self.blocks[0,1] = center_y-block_side
                
                self.blocks[1,0] = center_x-block_side
                self.blocks[1,1] = center_y-block_side
                
                self.blocks[2,0] = center_x
                self.blocks[2,1] = center_y-block_side
                
                self.blocks[3,0] = center_x+block_side
                self.blocks[3,1] = center_y-block_side
                    
            elif self.angle>=90 and self.angle<180:
                
                self.blocks[0,0] = center_x-block_side
                self.blocks[0,1] = center_y-block_side*2
                
                self.blocks[1,0] = center_x-block_side
                self.blocks[1,1] = center_y-block_side
                
                self.blocks[2,0] = center_x-block_side
                self.blocks[2,1] = center_y
                
                self.blocks[3,0] = center_x-block_side
                self.blocks[3,1] = center_y+block_side
                
            elif self.angle>=180 and self.angle<270:
                
                self.blocks[0,0] = center_x-block_side*2
                self.blocks[0,1] = center_y
                
                self.blocks[1,0] = center_x-block_side
                self.blocks[1,1] = center_y
                
                self.blocks[2,0] = center_x
                self.blocks[2,1] = center_y
                
                self.blocks[3,0] = center_x+block_side
                self.blocks[3,1] = center_y
                  
            else:    
                self.blocks[0,0] = center_x
                self.blocks[0,1] = center_y-block_side*2
                
                self.blocks[1,0] = center_x
                self.blocks[1,1] = center_y-block_side
                
                self.blocks[2,0] = center_x
                self.blocks[2,1] = center_y
                
                self.blocks[3,0] = center_x
                self.blocks[3,1] = center_y+block_side
            
        elif self.type == 'T':
            
            if self.angle>= 0 and self.angle < 90 :
                self.blocks[0,0] = center_x-block_side/2
                self.blocks[0,1] = center_y-block_side/2
                
                self.blocks[1,0] = center_x-block_side*1.5
                self.blocks[1,1] = center_y-block_side/2
                
                self.blocks[2,0] = center_x+block_side/2
                self.blocks[2,1] = center_y-block_side/2
                
                self.blocks[3,0] = center_x-block_side/2
                self.blocks[3,1] = center_y-block_side*1.5
                
                
            elif self.angle>=90 and self.angle<180:
                self.blocks[0,0] = center_x-block_side/2
                self.blocks[0,1] = center_y-block_side/2
                
                self.blocks[1,0] = center_x+block_side/2
                self.blocks[1,1] = center_y-block_side/2
                
                self.blocks[2,0] = center_x-block_side/2
                self.blocks[2,1] = center_y-block_side*1.5
                
                self.blocks[3,0] = center_x-block_side/2
                self.blocks[3,1] = center_y+block_side/2
                
            elif self.angle>=180 and self.angle<270:
                
                self.blocks[0,0] = center_x-block_side/2
                self.blocks[0,1] = center_y-block_side/2
                
                self.blocks[1,0] = center_x-block_side*1.5
                self.blocks[1,1] = center_y-block_side/2
                
                self.blocks[2,0] = center_x-block_side/2
                self.blocks[2,1] = center_y+block_side/2
                
                self.blocks[3,0] = center_x+block_side/2
                self.blocks[3,1] = center_y-block_side/2
                
            else:    
                
                self.blocks[0,0] = center_x-block_side/2
                self.blocks[0,1] = center_y-block_side/2
                
                self.blocks[1,0] = center_x-block_side*1.5
                self.blocks[1,1] = center_y-block_side/2
                
                self.blocks[2,0] = center_x-block_side/2
                self.blocks[2,1] = center_y-block_side*1.5
                
                self.blocks[3,0] = center_x-block_side/2
                self.blocks[3,1] = center_y+block_side/2
               
            
        elif self.type == 'J':
            
            if self.angle>= 0 and self.angle < 90 :
                self.blocks[0,0] = center_x-block_side/2
                self.blocks[0,1] = center_y-block_side/2
                
                self.blocks[1,0] = center_x-block_side*1.5
                self.blocks[1,1] = center_y-block_side/2
                
                self.blocks[2,0] = center_x+block_side/2
                self.blocks[2,1] = center_y-block_side/2
                
                self.blocks[3,0] = center_x+block_side/2
                self.blocks[3,1] = center_y+block_side/2
                
            elif self.angle>=90 and self.angle<180 : 
                
                self.blocks[0,0] = center_x-block_side/2
                self.blocks[0,1] = center_y-block_side/2
                
                self.blocks[1,0] = center_x-block_side/2
                self.blocks[1,1] = center_y-block_side*1.5
                
                self.blocks[2,0] = center_x-block_side/2
                self.blocks[2,1] = center_y+block_side/2
                
                self.blocks[3,0] = center_x-block_side*1.5
                self.blocks[3,1] = center_y+block_side/2
                
            elif self.angle>=180 and self.angle<270 :   
                self.blocks[0,0] = center_x-block_side/2
                self.blocks[0,1] = center_y-block_side/2
                
                self.blocks[1,0] = center_x-block_side*1.5
                self.blocks[1,1] = center_y-block_side/2
                
                self.blocks[2,0] = center_x+block_side/2
                self.blocks[2,1] = center_y-block_side/2
                
                self.blocks[3,0] = center_x-block_side*1.5
                self.blocks[3,1] = center_y-block_side*1.5
                
            else :     
                self.blocks[0,0] = center_x-block_side/2
                self.blocks[0,1] = center_y-block_side/2
                
                self.blocks[1,0] = center_x-block_side/2
                self.blocks[1,1] = center_y-block_side*1.5
                
                self.blocks[2,0] = center_x-block_side/2
                self.blocks[2,1] = center_y+block_side/2
                
                self.blocks[3,0] = center_x+block_side/2
                self.blocks[3,1] = center_y-block_side*1.5               
                
                
        elif self.type == 'L':
            
            if self.angle>= 0 and self.angle < 90 :
                self.blocks[0,0] = center_x-block_side/2
                self.blocks[0,1] = center_y-block_side/2
                
                self.blocks[1,0] = center_x-block_side*1.5
                self.blocks[1,1] = center_y-block_side/2
                
                self.blocks[2,0] = center_x+block_side/2
                self.blocks[2,1] = center_y-block_side/2
                
                self.blocks[3,0] = center_x-block_side*1.5
                self.blocks[3,1] = center_y+block_side/2
                
            elif self.angle>=90 and self.angle<180 : 
                
                self.blocks.append(block(center_x-block_side/2,center_y-block_side/2,self.color))
                self.blocks.append(block(center_x-block_side/2,center_y-block_side*1.5,self.color))
                self.blocks.append(block(center_x-block_side/2,center_y+block_side/2,self.color))
                self.blocks.append(block(center_x-1.5*block_side,center_y-block_side*1.5,self.color))
                
            elif self.angle>=180 and self.angle<270 :   
                
                self.blocks.append(block(center_x-block_side/2,center_y-block_side/2,self.color))
                self.blocks.append(block(center_x-block_side*1.5,center_y-block_side/2,self.color))
                self.blocks.append(block(center_x+block_side/2,center_y-block_side/2,self.color))
                self.blocks.append(block(center_x+0.5*block_side,center_y-block_side*1.5,self.color))
                    
            else :     
                
                self.blocks.append(block(center_x-block_side/2,center_y-block_side/2,self.color))
                self.blocks.append(block(center_x-block_side/2,center_y-block_side*1.5,self.color))
                self.blocks.append(block(center_x-block_side/2,center_y+block_side/2,self.color))
                self.blocks.append(block(center_x+block_side*0.5,center_y+block_side*0.5,self.color)) 
                
                
        elif self.type == 'S':
            
            if self.angle>=0 and self.angle<90 or self.angle>=180 and self.angle<270:
                
                self.blocks.append(block(center_x-block_side/2,center_y-block_side/2,self.color))
                self.blocks.append(block(center_x+block_side/2,center_y-block_side/2,self.color))
                self.blocks.append(block(center_x-block_side/2,center_y+block_side/2,self.color))
                self.blocks.append(block(center_x-block_side*1.5,center_y+block_side/2,self.color))
                
            else:
                
                self.blocks.append(block(center_x-block_side/2,center_y-block_side/2,self.color))
                self.blocks.append(block(center_x+block_side/2,center_y-block_side/2,self.color))
                self.blocks.append(block(center_x-block_side/2,center_y-block_side*1.5,self.color))
                self.blocks.append(block(center_x+block_side/2,center_y+block_side*0.5,self.color))
        
        
        elif self.type == 'Z':
            
            if self.angle>=0 and self.angle<90 or self.angle>=180 and self.angle<270:
                
                self.blocks.append(block(center_x-block_side/2,center_y-block_side/2,self.color))
                self.blocks.append(block(center_x+block_side/2,center_y+block_side/2,self.color))
                self.blocks.append(block(center_x-block_side/2,center_y+block_side/2,self.color))
                self.blocks.append(block(center_x-block_side*1.5,center_y-block_side/2,self.color))
                
            else:
                
                self.blocks.append(block(center_x-block_side/2,center_y-block_side/2,self.color))
                self.blocks.append(block(center_x-block_side/2,center_y+block_side/2,self.color))
                self.blocks.append(block(center_x+block_side/2,center_y-block_side/2,self.color))
                self.blocks.append(block(center_x+block_side/2,center_y-block_side*1.5,self.color))
                
                
         
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
    
    def moveLeft(self,desp):
        r = False
        if not self.stop and not self.is_side('l'):
            #centre
            aux = self.rot_center_X
            self.rot_center_X = self.rot_center_X-desp
            #cadascun dels blocks
            for b in self.blocks:
                #Avall
                b.moveLeft(desp)
            #Tornem a serhi, s'ha d'actualitzar el sprite
            r = self.update_sprite()
            if not r:
                self.rot_center_X = aux
                self.update_sprite()
        return r
    def moveRight(self,desp):
        r = False
        if not self.stop and not self.is_side('r'):
            #centre
            aux = self.rot_center_X
            self.rot_center_X = self.rot_center_X+desp
            #cadascun dels blocks
            for b in self.blocks:
                #Avall
                b.moveLeft(desp)
            #Tornem a serhi, s'ha d'actualitzar el sprite
            r = self.update_sprite()
            if not r:
                self.rot_center_X = aux
                self.update_sprite()
        return r
    #Si t'has llegit aixo despres del update crec que no sera problema :)
    #Se li dona un desplaçament i canvia el centre de rotacio cap avajo i 
    # passa per cadascun dels blocks moventlos tambe
    def moveDown(self,desp):
        #centre
        r = False
        if not self.stop:
            aux = self.rot_center_Y
            self.rot_center_Y = self.rot_center_Y+desp
            #cadascun dels blocks
            for b in self.blocks:
                #Avall
                b.moveDown(desp)
            #Tornem a serhi, s'ha d'actualitzar el sprite
            r = self.update_sprite()
            if not r:
                self.rot_center_Y = aux
                self.update_sprite()
                self.stop = True
        return r
    
    #Aquesta es la part cuki de la rotació jeje, aqui nomes es canvia 
    # l'angle i s'envia la feina al update
    def rotRight(self):
        aux = self.angle
        r = False
        if not self.stop:
            if not self.stop_rot:
                self.angle = self.angle+90
                if self.angle == 360:
                    self.angle = 0
                r = self.update_sprite()
                if not r:
                    self.rot_center_Y = aux
                    self.update_sprite()
                    self.stop_rot =True
        return r
                
        
    #Lo mismo pa lotro lao(sense angles negatius chungus)
    def rotLeft(self):
        aux = self.angle
        r = False
        if not self.stop:
            if not self.stop_rot:
                if self.angle == 0:
                    self.angle = 360
                self.angle = self.angle-90
                
                r = self.update_sprite()
                if not r:
                    self.rot_center_Y = aux
                    self.update_sprite()
                    self.stop_rot =True
        return r
    def is_stop(self):
        return self.stop
    #Comprovo si algun dels blocks ha arribat al limit que es passa per parametre
    #Esquema de bucle de cerca caca avorrida.
    #Actualitza la variable stop per a saber despres si ta parao
    
    def is_bottom(self):
        i = 0
        stop = False
        while not stop and i < len(self.blocks):
            b = self.blocks[i]
            
            if (b.posY+block_side)>=self.lim_z:
                stop = True
            else:
                stop = False
            i = i+1
        return stop
            
        
    #Cosa mes simple no hi ha, crida al draw dels blocks
    def draw(self,surf):
        for b in self.blocks:
            x = b.x
            y = b.y
            r1 = pygame.Rect(x,y,block_side,block_side)
            r2 = pygame.Rect(x,y,block_border_side,block_border_side)
            pygame.draw.rect(surf,self.color,r1)
            #Borde Negre de tamany 2
            pygame.draw.rect(surf,(0,0,0),r2)
    
            
            
        
                
            