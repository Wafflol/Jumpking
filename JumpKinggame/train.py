import numpy as np
import os

from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO
from concurrent.futures import ThreadPoolExecutor

import asyncio

from env import JumpKingEnv
from game import Game
import time



print(os.getcwd())
models_dir = f"models/{int(time.time())}"
logdir = f"logs/{int(time.time())}"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)
if not os.path.exists(logdir):
    os.makedirs(logdir)

game = Game()
asyncio.get_event_loop().run_until_complete(game.startGame(False))

env = JumpKingEnv(game)
obs = env.reset()
# print("hello", check_env(env))
#print(env.observation_space.sample())

model = PPO("MultiInputPolicy", env, verbose=1, tensorboard_log = logdir)
TIMESTEPS = 200
for i in range(100):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO")
    model.save(f"{models_dir}/{TIMESTEPS*i}")
    
print("done learning") 


    #model.save("ppo_jumpking")
time.sleep(3)
#for i in range(1000):
#    action, _states = model.predict(obs, deterministic=True)
#    obs, reward, done, info = env.step(action)
#    env.render()
#obs = env.reset()
asyncio.get_event_loop().run_until_complete(game.terminate())

