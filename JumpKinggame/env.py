import asyncio
import gym
from gym import spaces
from game import Game
import time
import numpy as np

class JumpKingEnv(gym.Env):
    
    metadata = {'render_modes': ['human']}
    
    def __init__(self, gameEnv, renderMode='human'):
        # gameEnv: the game object JumpKing runs in
        # renderMode: render toggle
        super(JumpKingEnv, self).__init__()
        self.current_level = 0
        self.current_step = 0
        self.env = gameEnv
        self.reward_range = (-1, 1)
        self.score = 0
        self.action_space = spaces.MultiDiscrete([6, 2])
        self.observation_space = spaces.Dict({"map": spaces.Box(
            low=0, high=1, shape=(900,1200)
            , dtype=np.uint8), "playerPosition": spaces.Box(low=-float('0'), high=float('1199'), shape=(2,)), "level": spaces.Discrete(43)})
        self.obs = {"map": np.zeros((900,1200)), "playerPosition": np.array([0, 0]), "level": 0}
        self.time_start = time.time()
        assert renderMode is None or renderMode in self.metadata["render_modes"]
        self.render_mode = renderMode
        
    def reset(self):
        asyncio.get_event_loop().run_until_complete(self.env.reset())
        time.sleep(0.001)
        self.current_step = 0
        self.score = 0
        self.time_start = time.time()
        self.obs = asyncio.get_event_loop().run_until_complete(self.env.obs())
        return self.obs
        # resets the env
        # ! change to reset to current level at previous starting position
    
    def step(self, action):
        asyncio.get_event_loop().run_until_complete(self.env.action(action))
        self.current_step += 1
        reward = asyncio.get_event_loop().run_until_complete(self.env.reward())
        self.obs = asyncio.get_event_loop().run_until_complete(self.env.obs())
        self.score = reward
        #print("score = ", self.score)
        done = reward == 5 #time.time() - self.time_start > 4 or (reward!=0)
        return self.obs, reward, done, {}
        
        
    def render(self, mode='human', close=False):
        self.env.setRenderMode(mode)
        pass
        