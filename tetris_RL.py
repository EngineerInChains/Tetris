# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 13:09:42 2020

@author: Miki
"""
from tetris import env
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime
import pygame
from pygame.locals import *
state_print = 0
def get_discrete_state(state):
    global state_print
    discrete_state = []
    pos_x = state[0]
    #discrete_state.append(pos_x)
    pos_y = state[1]
    type_p = state[2]
    discrete_state.append(type_p)
    rot = state[3]
    discrete_state.append(rot)
    bump = state[4]
    bump = np.array(bump)
    
    
    
    if pos_x < 2:
        pos_x = 2
    if pos_x >= 6:
        pos_x =6
    #print(bump)
    bump = bump[pos_x-2:pos_x+3]
    max_bump = np.min(bump)
    for b in bump:
        #b = int(max_bump-b)
        if b>11:
            b=11
        discrete_state.append(b)
    
    if state_print>5:
        state_print=0
        #print(discrete_state)
    
    else:
        state_print+=1
    #state[4]+=1
    #print(discrete_state)
    return tuple(discrete_state)

def save_all():            
    np.save("Out_lr="+str(lr)+"_discount="+str(discount),q_table)
    end_prova = time.time()
    print("Prova ha durat: ",end_prova-start)
    plt.figure()
    plt.title("AVG Prova amb lr="+str(lr)+" i discount="+str(discount))
    plt.plot(aggr_rewards['ep'],aggr_rewards['avg'],label='avg')
    plt.legend()
    plt.show()
    plt.savefig("AVG_Out_lr="+str(lr)+"_discount="+str(discount)+".png")
    plt.close()
    plt.figure()
    plt.title("MAX Prova amb lr="+str(lr)+" i discount="+str(discount))
    plt.plot(aggr_rewards['ep'],aggr_rewards['max'],label='max')
    plt.legend()
    plt.show()
    plt.savefig("MAX_Out_lr="+str(lr)+"_discount="+str(discount)+".png")
    plt.close()
    plt.figure()
    plt.title("MIN Prova amb lr="+str(lr)+" i discount="+str(discount))
    plt.plot(aggr_rewards['ep'],aggr_rewards['min'],label='min')
    plt.legend()
    plt.show()
    plt.savefig("MIN_Out_lr="+str(lr)+"_discount="+str(discount)+".png")
    plt.close()
    plt.figure()
    print(aggr_rewards['dur'])
    plt.title("Dur Prova amb lr="+str(lr)+" i discount="+str(discount))
    dur_ep = np.linspace(int(show_every/10),len(aggr_rewards['dur'])*int(show_every/10),len(aggr_rewards['dur']))
    plt.plot(aggr_rewards['ep'],aggr_rewards['dur'],label='dur')
    plt.legend()
    plt.show()
    plt.savefig("Dur_Out_lr="+str(lr)+"_discount="+str(discount)+".png")
    plt.close()


show_every = 300
start = time.time()
#print("Start Training: ",time.time())
for lr in [0.5]:
    valors_avg_dur = []
    avg_dur = 0
    end_lr=0.1
    discount = 0.2
    #0.4?
    episodes=30000
    #epsilon = 0.5
    epsilon = 1
    end_epsilon = 0.001
    start_epsilon = 0
    start_epsilon_decaying = 0
    #end_epsilon_decaying = episodes//2
    end_lr_decaying = int(episodes*0.75)
    end_epsilon_decaying = int(episodes*0.2)
    lr_decay_value = (lr-end_lr)/(end_lr_decaying-1)
    #lr_decay_value = 0
    epsilon_decay_value = (epsilon-end_epsilon)/(end_epsilon_decaying-start_epsilon_decaying)
    episode_rewards = np.zeros(int(show_every))
    aggr_rewards = {'ep': [],'avg': [],'min': [],'max': [],'dur': []}
    
    action_space_n = 4
    DISCRETE_OBS_SIZES = [7,4,12,12,12,12,12]
    #np.random.seed(seed=0)
    #print("Creating q table:")
    q_table = np.random.uniform(low=0,high=10,size=(DISCRETE_OBS_SIZES+[action_space_n]))
    #q_table = np.ones((DISCRETE_OBS_SIZES+[action_space_n]))+10
    #print("Created with size: ",q_table.shape)
    #q_table = np.load("read1.npy")
    manual = 0
    count_r = 0
    
    for ep in range(episodes):
        
        game = env(False)
        run = False
        episode_reward = 0
        #print("Creating Board For Episode: ",ep)
        
        #print("Board Created")
        #print(q_table.shape)
        
        #print("1st Step:")
        run,state,reward = game.step(4,not ep%show_every==0)
        
        discrete_state = get_discrete_state(state)
        game_start = time.time()
        while run:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_all()
                    pygame.display.quit()
        
                
            if np.random.random() > epsilon or ep < start_epsilon:
                #print("Taken Action:")
                action = np.argmax(q_table[discrete_state])
            else:
                #print("Random Action:")
                action = np.random.randint(0,action_space_n)
            #print("Step this ep")
            #print("Iniciant Step amb action: ",action)
            #game.step(4)
            run,state,reward = game.step(action,not ep%show_every==0)
            episode_reward += reward
            if ep%show_every==0:
                time.sleep(0.05)
            new_discrete_state = get_discrete_state(state)
            if np.any(new_discrete_state)>1:
                pass
            if run:
                #print("Calculating Q")
                ant_table = list(q_table[discrete_state])
                max_future_q = np.max(q_table[new_discrete_state])
                current_q = q_table[discrete_state+(action,)]
                new_q = (1-lr)*current_q + lr*(reward+discount*max_future_q)
                q_table[discrete_state+(action,)] = new_q
                curr_table = q_table[discrete_state]
            else:
                pass
                #print(1/(time.time()-game_start))
                #q_table[discrete_state+(action,)] -= 1/(time.time()-game_start)*2
            discrete_state = new_discrete_state
                
        
        if end_epsilon_decaying>= ep >= start_epsilon_decaying:
            epsilon -= epsilon_decay_value
        if end_lr_decaying>= ep >= 1:
            lr -= lr_decay_value    
        episode_rewards[count_r]=episode_reward
        #print(episode_rewards)
        count_r+=1
        if ep%(show_every)==0:
            if ep!=0:
                count_r =0
                average_reward = np.sum(episode_rewards)/(show_every)
                aggr_rewards['ep'].append(ep)
                aggr_rewards['avg'].append(average_reward)
                aggr_rewards['min'].append(min(episode_rewards[-show_every:]))
                m = max(episode_rewards[-show_every:])
                if m not in aggr_rewards['max']:
                    np.save("Check_lr="+str(lr)+"_discount="+str(discount)+"_MAX_REWARD="+str(m),q_table)
                aggr_rewards['max'].append(m)
                
                act_1 = time.time()-aux_time
                
                valors_avg_dur.append(act_1)
                act_1 = str(datetime.timedelta(seconds=act_1))
                act_1 = act_1.split('.')
                act_1 = act_1[0]+'.'+act_1[1][0:3]
                if len(valors_avg_dur)>20:
                    valors_avg_dur.pop(0)
                if len(valors_avg_dur)>0:
                    avg = np.sum(np.array(valors_avg_dur))/len(valors_avg_dur)
                else:
                    avg=0
                aggr_rewards['dur'].append(avg)
                print(f"Episode: {ep} avg: {average_reward} min: {min(episode_rewards[-show_every:])} max: {max(episode_rewards[-show_every:])} duration: {str(act_1)[:15]} avg_dur: {str(avg)[:6]} lr: {str(lr)[:10]}")
                print("\t Q Table:",ant_table)
                print("\t New Q Table:",curr_table)
                
            aux_time = time.time()
            episode_rewards = np.zeros(1+int(show_every))
        
    save_all()
end_sessio = time.time()
print("Sessio ha durat: ",end_sessio-start)




pygame.quit()