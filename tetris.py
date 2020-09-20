

import pygame
import random
import numpy as np
import time
pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


# SHAPE FORMATS

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
#types = {S: 0,Z: 1,I: 2,O: 3,J: 4,L: 5,T: 6}
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):  # *
    def __init__(self, x, y, shape,type_p):
        self.x = x
        self.y = y
        self.shape = shape
        self.type = type_p
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

class env:
    def __init__(self,silent):
        self.max_current_q = 0
        if not silent:
            self.win = pygame.display.set_mode((s_width, s_height))
            pygame.display.set_caption('Tetris')
        self.last_score = 0
        self.locked_positions = {}
        self.grid = self.create_grid(self.locked_positions)
        self.state = []
        self.change_piece = False
        self.run = True
        self.current_piece = self.get_shape()
        self.next_piece = self.get_shape()
        self.level_time = 0
        self.score = 0
    def create_grid(self,locked_pos={}):  # *
        grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]
    
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j, i) in locked_pos:
                    c = locked_pos[(j,i)]
                    grid[i][j] = c
        return grid
    
    
    def convert_shape_format(self,shape):
        positions = []
        format = shape.shape[shape.rotation % len(shape.shape)]
    
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((shape.x + j, shape.y + i))
    
        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)
    
        return positions
    
    
    def valid_space(self,shape, grid):
        accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
        accepted_pos = [j for sub in accepted_pos for j in sub]
    
        formatted = self.convert_shape_format(shape)
    
        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True
    
    
    def check_lost(self,positions):
        for pos in positions:
            x, y = pos
            if y < 1:
                return True
    
        return False
    
    
    def get_shape(self):
        d = random.randint(0,len(shapes)-1)
        return Piece(5, 0, shapes[d],d)
    
    
    def draw_text_middle(self,surface, text, size, color):
        font = pygame.font.SysFont("comicsans", size, bold=True)
        label = font.render(text, 1, color)
    
        surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))
    
    
    def draw_grid(self,surface, grid):
        sx = top_left_x
        sy = top_left_y
    
        for i in range(len(grid)):
            pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+play_width, sy+ i*block_size))
            for j in range(len(grid[i])):
                pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy),(sx + j*block_size, sy + play_height))
    
    
    def clear_rows(self,grid, locked):
    
        inc = 0
        for i in range(len(grid)-1, -1, -1):
            row = grid[i]
            if (0,0,0) not in row:
                inc += 1
                ind = i
                for j in range(len(row)):
                    try:
                        del locked[(j,i)]
                    except:
                        continue
    
        if inc > 0:
            for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    locked[newKey] = locked.pop(key)
    
        return inc
    
    
    def draw_next_shape(self,shape, surface):
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Next Shape', 1, (255,255,255))
    
        sx = top_left_x + play_width + 50
        sy = top_left_y + play_height/2 - 100
        format = shape.shape[shape.rotation % len(shape.shape)]
    
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)
    
        surface.blit(label, (sx + 10, sy - 30))
    
    
    def update_score(self,nscore):
        score = self.max_score()
    
        with open('scores.txt', 'w') as f:
            if int(score) > nscore:
                f.write(str(score))
            else:
                f.write(str(nscore))
    
    
    def max_score(self):
        with open('scores.txt', 'r') as f:
            lines = f.readlines()
            score = lines[0].strip()
    
        return score
    
    
    def draw_window(self,surface, grid,action, score=0, last_score = 0):
        surface.fill((0, 0, 0))
    
        pygame.font.init()
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('Tetris', 1, (255, 255, 255))
    
        surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))
    
        # current score
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Score: ' + str(score), 1, (255,255,255))
        
        sx = top_left_x + play_width + 50
        sy = top_left_y + play_height/2 - 100
    
        surface.blit(label, (sx + 20, sy + 160))
        #State
        if len(self.state)>0:
            font = pygame.font.SysFont('comicsans', 30)
            label = font.render('X: ' + str(self.state[0]), 1, (255,255,255))
            sx = top_left_x + play_width + 30
            sy = top_left_y + play_height/2 - 350
            surface.blit(label, (sx - 20, sy ))
            label = font.render('Y: ' + str(self.state[1]), 1, (255,255,255))
            sx = top_left_x + play_width + 80
            sy = top_left_y + play_height/2 - 350
            surface.blit(label, (sx - 20, sy ))
            label = font.render('Type: ' + str(self.state[2]), 1, (255,255,255))
            sx = top_left_x + play_width + 140
            sy = top_left_y + play_height/2 - 350
            surface.blit(label, (sx - 20, sy ))
            label = font.render('Rot: ' + str(self.state[3]), 1, (255,255,255))
            sx = top_left_x + play_width + 30
            sy = top_left_y + play_height/2 - 320
            surface.blit(label, (sx - 20, sy ))
            pos_x = self.state[0]
    
            pos_y = self.state[1]
            if pos_x < 2:
                pos_x = 2
            if pos_x >= 6:
                pos_x =6
    
            bump = self.state[4][pos_x-2:pos_x+3]
            min_bump = np.min(bump)
            real_bump = []
            for b in bump:
                #b = int(b-min_bump)
                if b>11:
                    b=11
                else:
                    time.sleep(0.03)
                real_bump.append(b)
            font = pygame.font.SysFont('comicsans', 30)
            
            label = font.render("Dist: "+str(real_bump)[1:-1], 1, (255,255,255))
            sx = top_left_x + play_width + 30
            sy = top_left_y + play_height/2 - 280
            surface.blit(label, (sx - 20, sy))
            
            if action==1:
                text = "Right"
            elif action==0:
                text = "Left"
            elif action==2:
                text = "Rot"
            elif action==3:
                text = "None"
            font = pygame.font.SysFont('comicsans', 30)
            label = font.render("Action: "+text, 1, (255,255,255))
            sx = top_left_x + play_width + 30
            sy = top_left_y + play_height/2 - 230
            surface.blit(label, (sx - 20, sy))
            
                
            
            
        # last score
        label = font.render('High Score: ' + str(last_score), 1, (255,255,255))
    
        sx = top_left_x - 200
        sy = top_left_y + 200
    
        surface.blit(label, (sx + 20, sy + 160))
    
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)
    
        pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    
        self.draw_grid(surface, grid)
        #pygame.display.update()
    
    def is_run(self):
        return self.run
    
    def get_state(self):
        state = []
        
        pos_x = self.current_piece.x
        pos_y = self.current_piece.y
        #print("Piece pos is: ",int(pos[0]/20),int(pos[1]/20))
        #state.append(int(pos[0]/20)-1)
        #state.append(int(pos[1]/20))
        state.append(pos_x)
        state.append(pos_y)
        
        state.append(self.current_piece.type)
        r = self.current_piece.rotation%4
        state.append(r)
        
        #print(len(self.grid),len(self.grid[0]),self.grid[0][0])
        shape_blocks = []
        
        for i in range(len(self.grid[0])):
            col = np.array([self.grid[j][i] for j in range(len(self.grid))])
            if pos_y <=20:
                if len(col[pos_y:])>0:
                    m = np.where(col[pos_y:] != (0,0,0))[0]
                    if len(m)>0:
                        m = np.min(m)
                    else:
                        m=20-pos_y
                else:
                    m = 20-pos_y
            else:
                m = 0
            shape_blocks.append(m)
        #print(shape_blocks)
        state.append(shape_blocks)
        
        self.state = state
        return state
    '''
    def set_curr_q(self,q):
        if self.q > self.max_current_q:
            self.max_current_q = self.q
    '''        
    def step(self,action,silent):
        
        self.grid = self.create_grid(self.locked_positions)
        
        
        self.current_piece.y += 1
        if not(self.valid_space(self.current_piece, self.grid)) and self.current_piece.y > 0:
            self.current_piece.y -= 1
            self.change_piece = True
        if not silent:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    #pygame.display.quit()
        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_piece.x -= 1
                        if not(self.valid_space(self.current_piece, self.grid)):
                            self.current_piece.x += 1
                    if event.key == pygame.K_RIGHT:
                        self.current_piece.x += 1
                        if not(self.valid_space(self.current_piece, self.grid)):
                            self.current_piece.x -= 1
                    if event.key == pygame.K_DOWN:
                        self.current_piece.y += 1
                        if not(self.valid_space(self.current_piece, self.grid)):
                            self.current_piece.y -= 1
                    if event.key == pygame.K_UP:
                        self.current_piece.rotation += 1
                        if not(self.valid_space(self.current_piece, self.grid)):
                            self.current_piece.rotation -= 1
        
        if not self.change_piece:
            
        
            
            if action==0:
                self.current_piece.x -= 1
                if not(self.valid_space(self.current_piece, self.grid)):
                    self.current_piece.x += 1
            elif action==1:
                self.current_piece.x += 1
                if not(self.valid_space(self.current_piece, self.grid)):
                    self.current_piece.x -= 1
            #elif action==2:
                #self.current_piece.y += 1
                #if not(self.valid_space(self.current_piece, self.grid)):
                    #self.current_piece.y -= 1
            elif action==2:
                self.current_piece.rotation += 1
                if not(self.valid_space(self.current_piece, self.grid)):
                    self.current_piece.rotation -= 1
        
        self.shape_pos = self.convert_shape_format(self.current_piece)
        for i in range(len(self.shape_pos)):
            x, y = self.shape_pos[i]
            if y > -1:
                self.grid[y][x] = self.current_piece.color
    
        if self.change_piece:
            for pos in self.shape_pos:
                p = (pos[0], pos[1])
                self.locked_positions[p] = self.current_piece.color
            self.current_piece = self.next_piece
            self.next_piece = self.get_shape()
            while self.next_piece.type == self.current_piece.type:
                self.next_piece = self.get_shape()
            self.change_piece = False
            aux = self.clear_rows(self.grid, self.locked_positions) * 10
            self.score += aux
            reward = aux*2
        else:
            reward=0
        if not silent:
            self.draw_window(self.win, self.grid,action, self.score, self.last_score)
            self.draw_next_shape(self.next_piece, self.win)
            pygame.display.update()
    
        if self.check_lost(self.locked_positions):
            if not silent:
                self.draw_text_middle(self.win, "YOU LOST!", 80, (255,255,255))
                pygame.display.update()
            #pygame.time.delay(1500)
            self.run = False
            self.update_score(self.score)
        state = self.get_state()
        
        return self.run,state,reward
        

