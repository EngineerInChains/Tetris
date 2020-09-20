# -*- coding: utf-8 -*-
import numpy as np

def get_piece_pos(piece_type,center_x,center_y,angle):
    
    p1 = [0,0,piece_type]
    
    blocks = np.array([p1,p1,p1,p1])
    
    block_side = 20
    
    if piece_type == -1:
        #Un sol block centrat al centre i de color color
        blocks[0][0] = center_x-block_side/2
        blocks[0][1] = center_y-block_side/2
        blocks[0]
        
    elif piece_type ==0:
        #Als quadrats no els hi importa una merda si els rotes per tant tot va bé fins aqui
        #Pots aagafar com a centre (0,0) i fer els calculs per veure quin block es quin
        #Declaracio block:: block(posX,posY,color)
        blocks[0][0] = center_x-block_side
        blocks[0][1] = center_y
        
        blocks[1][0] = center_x
        blocks[1][1] = center_y
        
        blocks[2][0] = center_x
        blocks[2][1] = center_y-block_side
        
        blocks[3][0] = center_x-block_side
        blocks[3][1] = center_y-block_side
    
        
    elif piece_type == 1:
       
        if angle>= 0 and angle < 90 :
            
            blocks[0][0] = center_x-block_side*2
            blocks[0][1] = center_y-block_side
            
            blocks[1][0] = center_x-block_side
            blocks[1][1] = center_y-block_side
            
            blocks[2][0] = center_x
            blocks[2][1] = center_y-block_side
            
            blocks[3][0] = center_x+block_side
            blocks[3][1] = center_y-block_side
                
        elif angle>=90 and angle<180:
            
            blocks[0][0] = center_x-block_side
            blocks[0][1] = center_y-block_side*2
            
            blocks[1][0] = center_x-block_side
            blocks[1][1] = center_y-block_side
            
            blocks[2][0] = center_x-block_side
            blocks[2][1] = center_y
            
            blocks[3][0] = center_x-block_side
            blocks[3][1] = center_y+block_side
            
        elif angle>=180 and angle<270:
            
            blocks[0][0] = center_x-block_side*2
            blocks[0][1] = center_y
            
            blocks[1][0] = center_x-block_side
            blocks[1][1] = center_y
            
            blocks[2][0] = center_x
            blocks[2][1] = center_y
            
            blocks[3][0] = center_x+block_side
            blocks[3][1] = center_y
              
        else:    
            blocks[0][0] = center_x
            blocks[0][1] = center_y-block_side*2
            
            blocks[1][0] = center_x
            blocks[1][1] = center_y-block_side
            
            blocks[2][0] = center_x
            blocks[2][1] = center_y
            
            blocks[3][0] = center_x
            blocks[3][1] = center_y+block_side
        
    elif piece_type == 2:
        
        if angle>= 0 and angle < 90 :
            blocks[0,0] = center_x-block_side/2
            blocks[0,1] = center_y-block_side/2
            
            blocks[1,0] = center_x-block_side*1.5
            blocks[1,1] = center_y-block_side/2
            
            blocks[2,0] = center_x+block_side/2
            blocks[2,1] = center_y-block_side/2
            
            blocks[3,0] = center_x-block_side/2
            blocks[3,1] = center_y-block_side*1.5
            
            
        elif angle>=90 and angle<180:
            blocks[0][0] = center_x-block_side/2
            blocks[0][1] = center_y-block_side/2
            
            blocks[1][0] = center_x+block_side/2
            blocks[1][1] = center_y-block_side/2
            
            blocks[2][0] = center_x-block_side/2
            blocks[2][1] = center_y-block_side*1.5
            
            blocks[3][0] = center_x-block_side/2
            blocks[3][1] = center_y+block_side/2
            
        elif angle>=180 and angle<270:
            
            blocks[0][0] = center_x-block_side/2
            blocks[0][1] = center_y-block_side/2
            
            blocks[1][0] = center_x-block_side*1.5
            blocks[1][1] = center_y-block_side/2
            
            blocks[2][0] = center_x-block_side/2
            blocks[2][1] = center_y+block_side/2
            
            blocks[3][0] = center_x+block_side/2
            blocks[3][1] = center_y-block_side/2
            
        else:    
            
            blocks[0][0] = center_x-block_side/2
            blocks[0][1] = center_y-block_side/2
            
            blocks[1][0] = center_x-block_side*1.5
            blocks[1][1] = center_y-block_side/2
            
            blocks[2][0] = center_x-block_side/2
            blocks[2][1] = center_y-block_side*1.5
            
            blocks[3][0] = center_x-block_side/2
            blocks[3][1] = center_y+block_side/2
           
        
    elif piece_type == 3:
        
        if angle>= 0 and angle < 90 :
            blocks[0][0] = center_x-block_side/2
            blocks[0][1] = center_y-block_side/2
            
            blocks[1][0] = center_x-block_side*1.5
            blocks[1][1] = center_y-block_side/2
            
            blocks[2][0] = center_x+block_side/2
            blocks[2][1] = center_y-block_side/2
            
            blocks[3][0] = center_x+block_side/2
            blocks[3][1] = center_y+block_side/2
            
        elif angle>=90 and angle<180 : 
            
            blocks[0][0] = center_x-block_side/2
            blocks[0][1] = center_y-block_side/2
            
            blocks[1][0] = center_x-block_side/2
            blocks[1][1] = center_y-block_side*1.5
            
            blocks[2][0] = center_x-block_side/2
            blocks[2][1] = center_y+block_side/2
            
            blocks[3][0] = center_x-block_side*1.5
            blocks[3][1] = center_y+block_side/2
            
        elif angle>=180 and angle<270 :   
            blocks[0][0] = center_x-block_side/2
            blocks[0][1] = center_y-block_side/2
            
            blocks[1][0] = center_x-block_side*1.5
            blocks[1][1] = center_y-block_side/2
            
            blocks[2][0] = center_x+block_side/2
            blocks[2][1] = center_y-block_side/2
            
            blocks[3][0] = center_x-block_side*1.5
            blocks[3][1] = center_y-block_side*1.5
            
        else :     
            blocks[0][0] = center_x-block_side/2
            blocks[0][1] = center_y-block_side/2
            
            blocks[1][0] = center_x-block_side/2
            blocks[1][1] = center_y-block_side*1.5
            
            blocks[2][0] = center_x-block_side/2
            blocks[2][1] = center_y+block_side/2
            
            blocks[3][0] = center_x+block_side/2
            blocks[3][1] = center_y-block_side*1.5               
            
            
    elif piece_type == 4:
        
        if angle>= 0 and angle < 90 :
            blocks[0][0] = center_x-block_side/2
            blocks[0][1] = center_y-block_side/2
            
            blocks[1][0] = center_x-block_side*1.5
            blocks[1][1] = center_y-block_side/2
            
            blocks[2][0] = center_x+block_side/2
            blocks[2][1] = center_y-block_side/2
            
            blocks[3][0] = center_x-block_side*1.5
            blocks[3][1] = center_y+block_side/2
            
        elif angle>=90 and angle<180 : 
            blocks[0][0] = center_x-block_side/2
            blocks[0][1] = center_y-block_side/2
            
            blocks[1][0] = center_x-block_side/2
            blocks[1][1] = center_y-block_side*1.5
            
            blocks[2][0] = center_x-block_side/2
            blocks[2][1] = center_y+block_side/2
            
            blocks[3][0] = center_x-block_side*1.5
            blocks[3][1] = center_y-block_side*1.5
            
        elif angle>=180 and angle<270 :   
            blocks[0][0] = center_x-block_side/2
            blocks[0][1] = center_y-block_side/2
            
            blocks[1][0] = center_x-block_side*1.5
            blocks[1][1] = center_y-block_side/2
            
            blocks[2][0] = center_x+block_side/2
            blocks[2][1] = center_y-block_side/2
            
            blocks[3][0] = center_x+block_side/2
            blocks[3][1] = center_y-block_side*1.5
                
        else :     
            blocks[0][0] = center_x-block_side/2
            blocks[0][1] = center_y-block_side/2
            
            blocks[1][0] = center_x-block_side/2
            blocks[1][1] = center_y-block_side*1.5
            
            blocks[2][0] = center_x-block_side/2
            blocks[2][1] = center_y+block_side/2
            
            blocks[3][0] = center_x+block_side/2
            blocks[3][1] = center_y+block_side/2
            
            
    elif piece_type == 5:
        
        if angle>=0 and angle<90 or angle>=180 and angle<270:
            blocks[0][0] = center_x-block_side/2
            blocks[0][1] = center_y-block_side/2
            
            blocks[1][0] = center_x+block_side/2
            blocks[1][1] = center_y-block_side/2
            
            blocks[2][0] = center_x-block_side/2
            blocks[2][1] = center_y+block_side/2
            
            blocks[3][0] = center_x-block_side*1.5
            blocks[3][1] = center_y+block_side/2
            
        else:
            blocks[0][0] = center_x-block_side/2
            blocks[0][1] = center_y-block_side/2
            
            blocks[1][0] = center_x+block_side/2
            blocks[1][1] = center_y-block_side/2
            
            blocks[2][0] = center_x-block_side/2
            blocks[2][1] = center_y-block_side*1.5
            
            blocks[3][0] = center_x+block_side/2
            blocks[3][1] = center_y+block_side/2
    
    
    elif piece_type == 6:
        
        if angle>=0 and angle<90 or angle>=180 and angle<270:
            blocks[0][0] = center_x-block_side/2
            blocks[0][1] = center_y-block_side/2
            
            blocks[1][0] = center_x+block_side/2
            blocks[1][1] = center_y+block_side/2
            
            blocks[2][0] = center_x-block_side/2
            blocks[2][1] = center_y+block_side/2
            
            blocks[3][0] = center_x-block_side*1.5
            blocks[3][1] = center_y-block_side/2
            
        else:
            blocks[0][0] = center_x-block_side/2
            blocks[0][1] = center_y-block_side/2
            
            blocks[1][0] = center_x-block_side/2
            blocks[1][1] = center_y+block_side/2
            
            blocks[2][0] = center_x+block_side/2
            blocks[2][1] = center_y-block_side/2
            
            blocks[3][0] = center_x+block_side/2
            blocks[3][1] = center_y-block_side*1.5
            
    return blocks