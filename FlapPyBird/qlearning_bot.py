""" 
Q learning bot for flappy bird 
"""
import math
import numpy as np


class Bot():
    """ Q learning bot for flappy bird """
    def __init__(self):
        self.episode = 0
        self.num_state = (50, 120, 10)       # x_diff, y_diff, y_vel
        self.state_bound = [[-60, 190], [-300, 300], [-9, 10]]
        self.lr = 0.70                      # learning rate
        self.df = 0.98                      # discount factor
        self.episilon = self.update_episilon()
        self.q_table = np.zeros(self.num_state + (2,), dtype=float)
        self.r_table = {'alive':1, 'dead':-1000, 'score':50}
        self.state = tuple()
        self.action = 0
    
    def update_q_table(self, next_state,reward):
        """ Q(s,a) = Q(s,a) + alpha*(r + gamma*maxQ(s',a') - Q(s,a)) """
        self.q_table[self.state][self.action] = (1.0 - self.lr) * self.q_table[self.state][self.action] + \
                                                self.lr * (reward + self.df * np.amax(self.q_table[next_state]))
        self.state = next_state
    
    def select_action(self):
        """ select an action with episilon greedy """
        """
        if self.episilon > np.random.random():
            self.action = 0 if self.state[1] > self.num_state[1]/2 + 5 else 1
        else:
            self.action = np.argmax(self.q_table[self.state])
        """
        self.action = np.argmax(self.q_table[self.state])
        return self.action
    
    def observe_reward(self, is_crash, is_score):
        if is_crash:
            return self.r_table['dead']
        elif is_score:
            return self.r_table['score']
        else:
            return self.r_table['alive']

    def observe_new_state(self, playerx, playery, playerVelY, lowerPipes):
        PIPEWIDTH = 50
        if lowerPipes[0]['x']-playerx > - PIPEWIDTH:
            checked_pipe = lowerPipes[0]
        else: 
            checked_pipe = lowerPipes[1]

        x_diff = checked_pipe['x'] - playerx
        y_diff = checked_pipe['y'] - playery
        observation = [x_diff, y_diff, playerVelY]
        return self.map_state(observation)

    def map_state(self, observation):
        """ Discretize the state and map to np array """
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
        
        return tuple(state_indice)

    def update_episilon(self):
        """ For episilon-greedy """
        min_episolon = .0001
        episilon = (math.exp(-0.1*self.episode))
        self.episilon = max(min_episolon, episilon)
