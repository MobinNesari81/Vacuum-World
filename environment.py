import gym
from gym import spaces
import pygame
import random

class VacuumWorldEnv(gym.Env):
    def __init__(self, n_rows:int = 5, n_cols:int = 5, max_timestep=100, dirt_chance:float = 0.4, is_obstacle:bool = False, obstacle_chance: float = 0.3, dirt_uncertainity: bool = False, movement_uncertainity: bool = False, suck_uncertainity: bool = False, observation_uncertainity: bool = False, no_location_obs: bool = False) -> None:
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.MAX_STEP = max_timestep
        self.no_location_obs = no_location_obs
        if self.no_location_obs:
            self.observation_space = spaces.Tuple((spaces.Discrete(2), spaces.Discrete(2)))
        else:
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
        self.prev_x_pos = None
        self.prev_y_pos = None
        self.time_step = 1
        self.dirt_chance = dirt_chance
        self.is_obstacle = is_obstacle
        self.obstacle_chance = obstacle_chance
        self.dirt_uncertainity = dirt_uncertainity
        self.movement_uncertainity = movement_uncertainity
        self.suck_uncertainity = suck_uncertainity
        self.observation_uncertainity = observation_uncertainity

        self._generate_map()
                

    def _generate_map(self):
        for i in range(self.n_rows):
            blocks = 0
            for j in range(self.n_cols):
                epsilon = random.random()
                if self.is_obstacle:
                    if epsilon > 1-self.dirt_chance:
                        self.map[i][j] = 1
                    elif epsilon < self.obstacle_chance and blocks < self.n_cols:
                        self.map[i][j] = -1 if (i != 0 or j != 0) else self.map[i][j]
                        blocks += 1
                else:
                    if epsilon > 1-self.dirt_chance:
                        self.map[i][j] = 1

    def _get_obs(self) -> tuple:
        if not self.no_location_obs:
            return (self.pos_x, self.pos_y, self.map[self.pos_x][self.pos_y])
        else:
            if self.prev_x_pos and self.prev_x_pos:
                if self.prev_x_pos == self.pos_x and self.prev_y_pos == self.pos_y:
                    return (1, self.map[self.pos_x][self.pos_y])
                else:
                    return (0, self.map[self.pos_x][self.pos_y])
            else:
                return (0, self.map[self.pos_x][self.pos_y])

    def _get_info(self) -> dict:
        return {'time_step': self.time_step}
    
    def _dirt_process(self) -> None:
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if self.map[i][j] != -1:
                    epsilon = random.random()
                    if epsilon > 1 - self.dirt_chance:
                        self.map[i][j] = 1
    
    def reset(self):
        super().reset()
        self._generate_map()
        self.pos_x = 0
        self.pos_y = 0
        self.prev_x_pos = None
        self.prev_y_pos = None
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
            if self.movement_uncertainity:
                epsilon = random.random()
                if epsilon > 0.2:
                    self.prev_x_pos = self.pos_x
                    self.prev_y_pos = self.pos_y
                    self.pos_x = tmp_pos[0]
                    self.pos_y = tmp_pos[1]
                else:
                    pass
            else:
                self.prev_x_pos = self.pos_x
                self.prev_y_pos = self.pos_y
                self.pos_x = tmp_pos[0]
                self.pos_y = tmp_pos[1]

        
        if action == 5:
            if self.suck_uncertainity:
                epsilon = random.random()
                if epsilon > 0.25:
                    if self.map[self.pos_x][self.pos_y] == 1:
                        reward = 10
                        self.map[self.pos_x][self.pos_y] = 0
                else:
                    reward = -1
                    self.map[self.pos_x][self.pos_y] = 1
            else:
                if self.map[self.pos_x][self.pos_y] == 1:
                        reward = 10
                        self.map[self.pos_x][self.pos_y] = 0
            
        
        if self.dirt_uncertainity:
            self._dirt_process()
        
        obs = self._get_obs()
        if not self.no_location_obs:
            if self.observation_uncertainity:
                epsilon = random.random()
                if epsilon > 0.1:
                    pass
                else:
                    obs = (obs[0], obs[1], 1-obs[2])
        else:
            if self.observation_uncertainity:
                epsilon = random.random()
                if epsilon > 0.1:
                    pass
                else:
                    obs = (obs[0], 1-obs[2])
                
        return obs, reward, False, self._get_info()




