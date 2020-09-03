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
import numpy as np
import pylab
import seaborn as sns

#Funcio que em demanen que posi(la llibreria)
pygame.init()

#Constants joc
HEIGHT = 600
SENSE_HEIGHT = 580
WIDTH = 360


lr = 0.1
discount = 0.8
episodes = 10000


q_table = np.random.uniform(0,200,size=(65535,5))






min_global_y = 580
block_side = 20
def get_state(pos_x_peça,pos_y_peça,blocks,extra_blocks,angle_peça,tipus_peça):
    
    state = 0
    i = 0
    is_below = False
    is_hole = False
    aux_extra = extra_blocks[1:]
    
    while not is_below and i < 4:
        x_b = blocks[i,0]
        aux = aux_extra[aux_extra[:,0] == x_b]
        is_below = np.any(aux[:,1] > blocks[i][1] )
           
        i = i+1
    
    upper_left_b_x = np.argmin(blocks[:,0])
    upper_left_b_y = np.argmin(blocks[:,1])
    lower_right_b_x = np.argmax(blocks[:,0])
    lower_right_b_y = np.argmax(blocks[:,1])
    upper_left_b_x = blocks[upper_left_b_x]
    upper_left_b_y = blocks[upper_left_b_y]
    lower_right_b_x = blocks[lower_right_b_x]
    lower_right_b_y = blocks[lower_right_b_y]
    min_diff = np.Inf
    n_h=0
    if not is_below:
         
         
         for i in range(upper_left_b_x[0],lower_right_b_x[0]+20,20):
             c = blocks[blocks[:,0]==i]
             c = c[c[:,1]==lower_right_b_y[1]]
             c = np.reshape(c,-1)
             if len(c)==0:
                 is_hole = True
                 n_h = n_h +1
             
    else:
        for i in range(upper_left_b_x[0],lower_right_b_x[0]+20,20):
            min_y = aux_extra[aux_extra[:,0] == i] 
            if len(min_y) == 0:
                min_y = HEIGHT-40
            else:
                min_y_aux = min_y[np.argmin(min_y[:,1])]
                min_y = min_y_aux[1]-20
            max_y = blocks[blocks[:,0] == i] 
            if len(max_y)!=0:
                max_y = max_y[np.argmax(max_y[:,1])]
                max_y = max_y[1]
            diff = abs(min_y-max_y)
            if min_diff > diff:
                min_diff = diff
                min_global_y = min_y
                
        for  i in range(upper_left_b_x[0],lower_right_b_x[0]+20,20):
            min_y = aux_extra[aux_extra[:,0] == i]
            if len(min_y) == 0:
                min_y = HEIGHT-40
            else:
                min_y = min_y[np.argmin(min_y[:,1])]
                min_y = min_y[1]-20
            
            max_y = blocks[blocks[:,0] == i]
            if len(max_y)!=0:
                max_y = max_y[np.argmax(max_y[:,1])]
                max_y = max_y[1]
                
                diff = abs(min_y-max_y)
                if diff != min_diff:
                    is_hole = True
                    n_h = n_h +int(abs(diff-min_diff)/20)
                 
            

            
    #if n_h==0:
        #print("UEEEPA")
    if is_below:
        state = 2**(15)
    if is_hole:
        state = state + 2**(14)
    if pos_y_peça < block_side:
        pos_y_peça = 0
    pos_y = format(int(pos_y_peça/block_side),'05b')
    
    state = state + 2**(13)*int(pos_y[0])+2**(12)*int(pos_y[1])+2**(11)*int(pos_y[2])+2**(10)*int(pos_y[3])+2**(9)*int(pos_y[4])
    
    pos_x = str(format(int(pos_x_peça/block_side),'04b'))
    state = state +2**(8)*int(pos_x[0])+2**(7)*int(pos_x[1])+2**(6)*int(pos_x[2])+2**(5)*int(pos_x[3])
    
    if angle_peça == 0:
        state = state 
    elif angle_peça == 90:
        state = state +2**(3)
    elif angle_peça == 180:
        state = state +2**(4)
    else:
        state = state +2**(4)+2**(3)
        
    t = str(format(tipus_peça,'03b'))
    
    state = state + 2**(2)*int(t[0])+ 2**(1)*int(t[1])+ 2**(0)*int(t[2])
        
    return state,n_h
max_score = 0
max_length = 0
start = time.time()

for ep in range(episodes):
    show = False
    #Crecio Board
    b = board.board(WIDTH,HEIGHT,'Tetris')
    #Primera Peça
    b.create_piece()
    reward = 0
    piece_pos = b.get_piece_pos()
    blocks = b.get_piece_blocks()
    init_state,n_h = get_state(piece_pos[0],piece_pos[1],blocks,b.get_extra_blocks(),b.get_piece_angle(),b.get_piece_type())
    #Bucle Principal del Joc(Aixo va tot el rato i d'aqui se surt a fer cusas)
    if ep %50==0:
        pylab.figure()
        ax = sns.heatmap(q_table)
        pylab.show()
        pylab.close()
    if ep%50==0:
        print("Episode: ",ep)
    game_start = time.time()
    ant_type = ""
    n_pieces = 0
    while not b.is_lost():
        
        
        action = np.argmax(q_table[init_state])
        
        if action==0:
            b.move_active('d')
        elif action==1:
            b.move_active('r')
        elif action==2:
            b.move_active('l')
        elif action==3:
            b.move_active('dd')
        elif action==4:
            b.rotate_active()    
        
        
        
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
        
        
        
        
        
        #Difficulty setting
        diff = 0.0005
        delay = 0.1
        #Sleep perque no es torni locatis
        
        if ep%40==0:
            if b.get_score() != 0:
                score = b.get_score()**2
                time.sleep(delay-b.get_score()*diff)
            else:
                time.sleep(delay)
        
        #Update Board(move down)
        b.update_board()
        
        #Draw Board
        if ep %40==0:
            b.draw_board()
        
        
        
        #Update Display
        pygame.display.update()
        
        
        if not b.is_lost():
            
            piece_pos = b.get_piece_pos()
            blocks = b.get_piece_blocks()
            
            new_state,n_h = get_state(piece_pos[0],piece_pos[1],blocks,b.get_extra_blocks(),b.get_piece_angle(),b.get_piece_type())
            if ant_type != b.get_piece_type():
                ant_type = b.get_piece_type()
                n_pieces = n_pieces+1
            reward = b.get_score()*10
            if n_h == 0:
                reward = reward +5
            
            reward = reward + min_global_y/100
            max_future_q = np.max(q_table[new_state])
            current_q = q_table[new_state][action]
            new_q = (1-lr) * current_q + lr*(reward+discount*max_future_q)
            q_table[init_state][action] = new_q
        else:
            q_table[init_state][action] = q_table[init_state][action]+b.get_score()-q_table[init_state][action]*(1/n_pieces)
            
        init_state = new_state
    if ep%40==0:
        if b.is_lost():
            diff = time.time()-game_start
            print("GAME LENGTH:" +str(diff))
            if diff > max_length:
                max_length = diff
            print("MAX GAME LENGTH:" +str(max_length))
            print("TOTAL TIME: "+str(time.time()-start))
            print("CURRENT SCORE: "+str(b.get_score()))
            if b.get_score() > max_score:
                max_score=b.get_score()
            print("MAX SCORE: "+str(max_score)+"\n")
        
            
            
            