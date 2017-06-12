""" 
Q learning bot for flappy bird 
"""
import numpy as np
import math

class Bot():
    """ Q learning bot for flappy bird """
    def __init__(self):
        self.episode = 0
        self.num_state = (20, 60, 2)       # x_diff, y_diff, y_vel
        self.state_bound = [[-40, 160], [-300, 300], [-9, 10]]
        self.lr = 0.70                      # learning rate
        self.df = 0.98                      # discount factor
        self.episilon = 0.1
        self.q_table = np.zeros(self.num_state + (2,), dtype=float)
        self.r_table = {'frame':1, 'die':-1000}
        self.state = tuple()
        self.next_state = tuple()
        self.action = 0
        self.state_reset()
    
    def update_q_table(self, reward):
        self.q_table[self.state][self.action] = (1.0 - self.lr) * self.q_table[self.state][self.action] + \
                                                self.lr * (reward + self.df * np.amax(self.q_table[self.next_state]))
        self.state = self.next_state

    def map_state(self, observation):
        state_indice = []
        for i in range(len(observation)):
            if observation[i] >= self.state_bound[i][1]:
                state_indice.append(self.num_state[i]-1)
            elif observation[i] <= self.state_bound[i][0]:
                state_indice.append(0)
            else:
                bound_width = self.state_bound[i][1] - self.state_bound[i][0]
                normalize_obv = (observation[i] - self.state_bound[i][0]) * (self.num_state[i]-1) / bound_width
                index = int(round(normalize_obv))
                state_indice.append(index)
        print (observation, state_indice)
        return tuple(state_indice)
    
    def get_action(self, observation):
        """
        if np.random.random() < self.episilon:
            self.action = np.argmax(self.q_table[self.state])
        else:
            self.action = 0 if observation[1] > 30 else 1
        """
        print (self.q_table[self.state])
        self.action = np.argmax(self.q_table[self.state])
        return self.action
                
    def update_episilon(self):
        self.episilon = max(0.1, min(0.999, math.log10((self.episode+1)/25)))

    def state_reset(self):
        self.state = tuple([self.num_state[0]-1, self.num_state[1]/2-1, 0])