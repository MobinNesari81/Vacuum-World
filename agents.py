'''
    Implementation of different agents for Vacuum World Problem
    Authors:
        Amirhossein Shabani
        Mobin Nesari
'''
import random

class reflexive_agent_2rooms:
    def __init__(self) -> None:
        pass
        '''
            0 -> No_Op
            1 -> Right
            2 -> Left
            5 -> Suck
        '''
    def act(self, observation, terminated):
        if terminated: 
            return 0
        else: 
            if observation[2] == 1:
                return 5
            elif observation[0] == 0 and observation[1] == 0: 
                return 1
            elif observation[0] == 0 and observation[1] == 1: 
                return 2
        

class random_reflexive_agent:
    def __init__(self) -> None:
        pass
        '''
            0 -> No_Op
            1 -> Right
            2 -> Left
            3 -> Up
            4 -> Down
            5 -> Suck
        '''
    def act(self, observation, terminated):
        if terminated: 
            return 0
        elif observation[2] == 1:
            return 5 
        else: 
            action = random.randint(1,4)
            return action 


class no_location_agent:
    def __init__(self, env):
        self.model = [[1 for j in range(env.n_cols)] for i in range(env.n_rows)] 
        self.cols = env.n_cols 
        self.rows = env.n_rows 
        self.cleaned = False 
        '''
            0 -> No_Op
            1 -> Right
            2 -> Left
            3 -> Up
            4 -> Down
            5 -> Suck
        '''

    def act(self, obs, terminated=False):
        if terminated:
            return 0 
        elif (obs[2] == 1 and self.model[obs[0]][obs[1]] == 1):
            self.model[obs[0]][obs[1]] = self.model[obs[0]][obs[1]] * 0.25 
            self.cleaned = True 
            return 5 
        else: 
            frontier = [(obs[0]+i,obs[1]+j) for i,j in zip([0,0,-1,1,0], [1,-1,0,0,0])] # right, left, up, down, suck 
            max_idx = -1 
            max = -1 
            for idx, (i, j) in enumerate(frontier):
                if not (i<0 or j<0 or i>=self.rows or j>=self.cols):
                    if self.model[i][j] > max: 
                        max_idx = idx
                        max = self.model[i][j]

            if max_idx + 1 == 5: # Suck 
                if obs[2] == 1: 
                    self.model[obs[0]][obs[1]] = self.model[obs[0]][obs[1]] * 0.25 
                    self.cleaned = True 
                else: 
                    #self.model[obs[0]][obs[1]] = self.model[obs[0]][obs[1]] * 0.1
                    self.cleaned = False 
                    max_idx = -1 


            else: 
                self.model[obs[0]][obs[1]] = self.model[obs[0]][obs[1]] if self.cleaned else self.model[obs[0]][obs[1]] * 0.1
                self.cleaned = False 


            return max_idx + 1     
