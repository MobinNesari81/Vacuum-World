'''
    Implementation of different agents for Vacuum World Problem
    Authors:
        Amirhossein Shabani
        Mobin Nesari
'''
import random

class Reflexive_Agent_2Rooms:
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
        

class Random_Reflexive_Agent:
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


class No_Location_Agent:
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


class TraGent:
    # Trace Agent implementation
    def __init__(self) -> None:
        self.memory_stack = []
        self.destination = None
        self.stal_flag = False
        self.prev_action = None
        self.last_row_direction = None

    def act(self, observation: tuple, terminated: bool):
        if terminated:
            return 0
        
        if observation[2] == 1:
            if self.destination:
                if self.destination[-1] == (observation[0], observation[1]):
                    self.destination.pop()
            return 5
        
        else:
            if  not self.destination:
                # Trace start to last
                if not self.prev_action:
                    # Initial State
                    self.memory_stack.append((observation[0], observation[1]))
                    self.prev_action = 'right'
                    return 1
                
                else:
                    if self.prev_action == 'right':
                        if self.memory_stack[-1] == (observation[0], observation[1]):
                            if self.stal_flag:
                                self.stal_flag = False
                                self.prev_action = 'down'
                                self.last_row_direction = 'right'
                                return 4
                            else:
                                self.stal_flag = True
                                return 1
                        
                        else:
                            self.memory_stack.append((observation[0], observation[1]))
                            self.stal_flag = False
                            return 1
                    
                    if self.prev_action == 'left':
                        if self.memory_stack[-1] == (observation[0], observation[1]):
                            if self.stal_flag:
                                self.stal_flag = False
                                self.prev_action = 'down'
                                self.last_row_direction = 'left'
                                return 4
                            else:
                                self.stal_flag = True
                                return 2
                        else:
                            self.memory_stack.append((observation[0], observation[1]))
                            self.stal_flag = False
                            return 2
                    
                    if self.prev_action == 'down':
                        if self.memory_stack[-1] == (observation[0], observation[1]):
                            if self.stal_flag:
                                self.destination = self.memory_stack[::-1]
                                self.memory_stack = []
                                self.stal_flag = False
                                self.prev_action = False
                                self.last_row_direction = None
                                return 2
                            
                            else:
                                self.stal_flag = True
                                return 4
                        
                        else:
                            if self.last_row_direction == 'right':
                                self.prev_action = 'left'
                                self.memory_stack.append((observation[0], observation[1]))
                                return 2
                            else:
                                self.prev_action = 'right'
                                self.memory_stack.append((observation[0], observation[1]))
                                return 1

                
                
            
            else:
                # Trace last to start
                if self.destination[0] == (observation[0], observation[1]):
                    self.destination.pop(0)
                delta_x = observation[0] - self.destination[0][0]
                delta_y = observation[1] - self.destination[0][1]
                if len(self.destination) == 1:
                    self.destination = None
                if delta_x > 0:
                    print('up')
                    return 3
                elif delta_x < 0:
                    print('down')
                    return 4
                elif delta_y > 0:
                    print('left')
                    return 2
                elif delta_y < 0:
                    print('right')
                    return 1
