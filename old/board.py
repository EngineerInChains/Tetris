# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 15:45:16 2020

@author: Miki
"""

import random
import pygame
from Peca import *
import pygame
from pygame.locals import *

#Constants joc
HEIGHT = 400
SENSE_HEIGHT = 380
WIDTH = 360


block_side = 20


class board():
    def __init__(self,sizeX,sizeY,caption,silent):
        self.state = []
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.silent = silent
        if not silent:
            #Funcio que em demanen que posi(la llibreria)
            pygame.init()
            #Creacio superficie on es pinta (anchura i altura) 
            self.displaysurface = pygame.display.set_mode((sizeX, sizeY))
            self.font2 = pygame.font.SysFont(None,18)
            self.font = pygame.font.SysFont(None, 24)
            
            #Titol de la pantalla
            pygame.display.set_caption(caption)
        
        
        self.lim_z = sizeY
        
        self.lim_x_min = 0
        self.lim_x_max = sizeX-20*10
        
        self.score = 0
        self.last_score=0
        self.active_p = ""
        self.n_pieces = 0
        
        self.stop_active = False
        self.stop_active_space = False
        
        self.extra_blocks = []
        
        self.colors = {0: (242, 242, 82),1: (114, 230, 232),2: (171, 64, 237),3: (64, 237, 73),
                  4: (235, 48, 23),5: (235, 150, 23),6: (27, 23, 235)}
        
        self.next_piece_pos = [[self.sizeX-20-50-40,115],[self.sizeX-20-50-40,135],[self.sizeX-20-50-40,125],[self.sizeX-20-50-40,105],[self.sizeX-20-50-40,105],[self.sizeX-20-50-40,110],[self.sizeX-20-50-40,110]]
        #["sq",'li','T','S','Z','L','J']
        self.next_p = random.randint(0,6)
        self.lost = False
        self.next_p_draw = ""
        #print("Creating Piece(init)")
        self.create_piece()
        
    def step(self,action,manual):
         #Bucle per comprovar si la llibreria ha detectat algun event
         
        if not self.silent:
            if manual:
                action=3
        
                    
        
        new_state = 0
        reward = 0
        lost = False
        if action==0:
            #print("Moving R")
            self.move_active('r')
        elif action==1:
            #print("Moving L")
            self.move_active('l')
        elif action==2:
            #print("Rot")
            self.rotate_active()
        #else:
            #print("Nothing")            
        #Update Board(move down)
        #print("Updating Board(Step)")
        self.update_board()
        
        if self.get_score()!=self.last_score:
            reward = 10
            self.last_score=self.get_score()
        #print("Obtaining State(Step)")
        new_state = self.get_state()
        lost = self.is_lost()
        return new_state,reward,lost,self.n_pieces,action
    
    def get_state(self):
        
        state = []
        
        pos = self.get_piece_position()
        #print("Piece pos is: ",int(pos[0]/20),int(pos[1]/20))
        #state.append(int(pos[0]/20)-1)
        #state.append(int(pos[1]/20))
        
        d = {"sq":0,'li':1,'T':2,'S':3,'Z':4,'L':5,'J':6}
        #print("Piece type is: ",self.active_p.type)
        state.append(self.active_p.type)
        
        if self.active_p.angle <90:
            state.append(0)
        elif self.active_p.angle <180:
            state.append(1)
        elif self.active_p.angle <270:
            state.append(2)
        else:
            state.append(3)
        
        min_y = int(np.max(self.active_p.blocks[:,1])/20)
        sizes = [20,20,20,20]
        inter = [20/sizes[0],20/sizes[1],20/sizes[2],20/sizes[3]]
        if not(self.active_p.type ==0 or self.active_p.type==1):
            pos[0] = pos[0] -10
            pos[1] = pos[1]+10
        
        mins = []
        for i,s in zip(range(pos[0]-40,pos[0]+40,20),inter):
            if i <20:
                i=20
            if i>200:
                i=200
            extra = self.extra_blocks[self.extra_blocks[:,0]==i]
            
            if len(extra)>0:
                aux = np.argmin(extra[:,1])
                extra_y = extra[aux]
                is_left = True
                while extra_y[1]<min_y and is_left:
                    extra = np.delete(extra,aux,axis=0)
                    if len(extra)>0:
                        aux = np.argmin(extra[:,1])
                        extra_y = extra[aux]
                    else:
                        is_left = False
                if is_left:    
                    extra_y = int(extra_y[1]/20)
                    
                    extra_y = extra_y
                    extra_y = int(extra_y/s)
                    #if extra_y == 0:
                        #print("HERE")
                    
                    #print("Col ",int(i/20)," is at: ",extra_y)
                else:
                    extra_y = int(19/s)
                mins.append(extra_y)
                
            else:
                extra_y = int(19/s)
                mins.append(extra_y)
                #print("Col ",int(i/20)," is at: ",extra_y)
        min_t = np.min(mins)
        mins = np.array(mins)
        mins[:] = abs(min_t-mins[:])
        mins[mins[:]>1] = 1
        for m in mins:
            state.append(m)
        
        self.state = state
        
            
        
        return tuple(state)
                
   
    def render(self,action,state,q_sita):
        if not self.silent:
            self.draw_board(action,state,q_sita)
            #Update Display
            pygame.display.update()


    def create_piece(self):
        self.n_pieces +=1
        self.stop_active = False
        self.stop_active_space = False
        typ = self.next_p
        #print("of type: ",typ)
        self.next_p = random.randint(0,6)
        
        while self.next_p == typ:
            self.next_p = random.randint(0,6)
        #print("Next is: ",self.next_p)
        #typ='sq'
        if typ == 0 or typ == 1 :
            posX = 140
            posY = 20
        else :
            posX = 150
            posY=10
        
        angle = 0
        #d = {"sq":0,'li':1,'T':2,'S':3,'Z':4,'L':5,'J':6}
        color = self.colors[typ]
        #print("Create next p")
        self.next_p_draw = piece(self.next_p,self.next_piece_pos[self.next_p][0],self.next_piece_pos[self.next_p][1],angle,self.colors[self.next_p],self.lim_z,self.lim_x_min,self.lim_x_max)
        #print("Create curr P")
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
        #d = {"sq":0,'li':1,'T':2,'S':3,'Z':4,'L':5,'J':6}
        return self.active_p.type
                        
    def get_piece_position(self):
        return self.active_p.get_center()
    
    def get_piece_angle(self):
        return self.active_p.get_angle()
            
        
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
                        '''
                        aux_extra = self.extra_blocks[:,1]<= line
                        blocks[aux_blocks,1]= blocks[aux_blocks,1]+20
                        self.extra_blocks[aux_extra,1] = self.extra_blocks[aux_extra,1]+20
                        '''
                self.extra_blocks = np.vstack((self.extra_blocks,blocks))
                if b:        
                    self.move_extra_blocks(lines)
                self.create_piece()
    
    #Comprovo si algun dels blocks ha arribat al limit que es passa per parametre
    #Esquema de bucle de cerca caca avorrida.
    #Actualitza la variable stop per a saber despres si ta parao
    def is_lost(self):
        b1 = False
        if self.active_p != "" and len(self.extra_blocks) >1:
            b = self.active_p.get_blocks()
            aux = np.any(b[:,1]<20)
            aux2 = self.touch_piece()
            b1 = aux and aux2
        
        return b1
    def touch_down(self):
        i = 0
        
        
        blocks = self.active_p.get_blocks()
        
        b = np.any((blocks[:,1]+block_side)>=self.lim_z)
        return b
             
    
    def touch_piece(self):
        blocks = self.active_p.get_blocks()
        touch = False
        i = 0
        
        #b = [self.extra_blocks[self.extra_blocks[:,0] == blocks[i][0]] for i in range(4)]
        #touch = np.any(b)
        
        while not touch and i < 4:
            j = 1
            #b = self.extra_blocks[self.extra_blocks[:,0] == blocks[i][0]]
            #if len(b)>0:
                #touch = np.any(self.extra_blocks[:,1] == blocks[i][1])
            
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
    
    def move_extra_blocks(self,lines):
        
        for l in lines:
            lim = l-block_side
            for i in range(lim,-block_side,-block_side):
                line = np.where(self.extra_blocks[:,1]==i)[0]
                if len(line)>0:
                    self.extra_blocks[line,1]+=20
                    if i+20< self.lim_z-40:
                        x_line = np.sort(self.extra_blocks[line,0])
                        lower_line = np.sort(self.extra_blocks[np.where(self.extra_blocks[:,1]==i+20)[0],0])
                        chop=[]
                        for j in range(len(x_line)):
                            if j == len(x_line)-1 or x_line[j]+20 != x_line[j+1]:
                                chop.append(line[j])
                                
                                touch = np.any([np.any(lower_line[:]==self.extra_blocks[c,0]) for c in chop])
                                count =0
                                while not touch:
                                    self.extra_blocks[chop,1]+=20
                                    count +=20
                                    lowerr_line = np.sort(self.extra_blocks[np.where(self.extra_blocks[:,1]==i+20+count)[0],0])
                                    touch = touch = np.any([np.any(lower_line[:]==self.extra_blocks[c,0]) for c in chop]) or i+count+20 >=self.lim_z-40
                                chop=[]
                            else:
                                chop.append(line[j])
            
    
    def touch_side(self,side):
        
        blocks = self.active_p.get_blocks()
        if side == 'l':
            is_bad = np.any(blocks[:,0]<=self.lim_x_min)
        else:
            is_bad = np.any(blocks[:,0]>self.lim_x_max)
            
        return is_bad    
                
                
    def draw_board(self,accio,state,q_sita):
        self.displaysurface.fill((0,0,0))
        self.grid_draw()
        if not self.is_lost():
            size = 20
            pygame.draw.line(self.displaysurface,(150,150,150),(size/2-1,0),(size/2-1,self.sizeY-size),size+1)
            pygame.draw.line(self.displaysurface,(150,150,150),(0,self.sizeY-size/2),(self.sizeX,self.sizeY-size/2),size)
            ol_size = size
            size = size *9
            pygame.draw.line(self.displaysurface,(150,150,150),(self.sizeX-size/2,self.sizeY-ol_size),(self.sizeX-size/2,0),size)
            
            pygame.draw.rect(self.displaysurface,(0,0,0),pygame.Rect(self.sizeX-20-100-40,0+20,80,25))
            
            
            img = self.font.render(str(self.score), True, (255,255,255))
            self.displaysurface.blit(img, (self.sizeX-20-95-40,0+25))
            
            img = self.font.render("Next Piece:", True, (0,0,0))
            self.displaysurface.blit(img, (self.sizeX-20-100-40,0+60))
            
            pygame.draw.rect(self.displaysurface,(0,0,0),pygame.Rect(self.sizeX-20-100-40,0+80,100,80))
            self.next_p_draw.draw(self.displaysurface)
            #print("NEXT MAL", self.next_p_draw.type)
            for b in self.extra_blocks[1:]:
                x = b[0]
                y = b[1]
                r1 = pygame.Rect(x,y,block_side,block_side)
                r2 = pygame.Rect(x+2,y+2,block_border_side,block_border_side)
                pygame.draw.rect(self.displaysurface,self.colors[b[2]],r1)
                #Borde Negre de tamany 2
                pygame.draw.rect(self.displaysurface,(0,0,0),r2,3)
            
            self.active_p.draw(self.displaysurface)
            #print("MAL ",self.active_p.type)
            if accio==0:
                accio='right'
            elif accio==1:
                accio='left'
            elif accio==2:
                accio='rot'
            elif accio==3:
                accio='None'
            
            img = self.font2.render("tp,rt,c5,c4,c3,c2,c1,c0",True,(255,255,255))
            self.displaysurface.blit(img, (self.sizeX-20-95-55,0+220))
            q_sita = ['{0:.4f}'.format(q) for q in q_sita]
            img = self.font2.render(str(q_sita),True,(255,255,255))
            self.displaysurface.blit(img, (20,0+382))
            img = self.font.render(str(state),True,(255,255,255))
            self.displaysurface.blit(img, (self.sizeX-20-95-55,0+240))
            img = self.font.render("Action: "+accio,True,(255,255,255))
            self.displaysurface.blit(img, (self.sizeX-20-95-20,0+185))
            
            
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
            
        