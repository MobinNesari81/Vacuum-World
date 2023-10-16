import gym
from gym import spaces
import pygame
import random

class VacuumWorldEnv(gym.Env):
    def __init__(self, n_rows:int = 5, n_cols:int = 5, max_timestep=100) -> None:
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.MAX_STEP = max_timestep
        self.observation_space = spaces.Tuple((spaces.Discrete(self.n_rows), spaces.Discrete(self.n_cols), spaces.Discrete(2))) # pos_x, pos_y, is_dirty
        self.action_space = spaces.Discrete(6)
        '''
            0 -> No_Op
            1 -> Right
            2 -> Left
            3 -> Up
            4 -> Down
            5 -> Suck
        '''

        self.map = [[0 for j in range(self.n_cols)] for i in range(self.n_rows)]
        self.pos_x = 0
        self.pos_y = 0
        self.time_step = 1

        self._generate_map()
                

    def _generate_map(self):
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                epsilon = random.random()
                if epsilon > 0.5:
                    self.map[i][j] = 1

    def _get_obs(self) -> tuple:
        return (self.pos_x, self.pos_y, self.map[self.pos_x][self.pos_y])

    def _get_info(self) -> dict:
        return {'time_step': self.time_step}
    
    def reset(self):
        super().reset()
        self._generate_map()
        self.pos_x = 0
        self.pos_y = 0
        self.time_step = 1

        return self._get_obs(), self._get_info()
    
    def step(self, action: int):

        self.time_step += 1
        if self.time_step > self.MAX_STEP:
            return self._get_obs(), 0, True, self._get_info()
        
        tmp_pos = [self.pos_x, self.pos_y]
        reward = 0
        if action == 1:
            tmp_pos[1] += 1
            reward = -1
        elif action == 2:
            tmp_pos[1] -= 1
            reward = -1
        elif action == 3:
            tmp_pos[0] -= 1
            reward = -1
        elif action == 4:
            tmp_pos[0] += 1
            reward = -1
        
        if not (tmp_pos[0] < 0 or tmp_pos[0] >= self.n_rows or tmp_pos[1] < 0 or tmp_pos[1] >= self.n_cols or self.map[tmp_pos[0]][tmp_pos[1]] == -1):
            self.pos_x = tmp_pos[0]
            self.pos_y = tmp_pos[1]
        
        if action == 5:
            if self.map[self.pos_x][self.pos_y] == 1:
                reward = 10
                self.map[self.pos_x][self.pos_y] = 0
        
        return self._get_obs(), reward, False, self._get_info()




