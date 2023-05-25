from stable_baselines3.common.env_checker import check_env
from env import JumpKingEnv
from game import Game
import asyncio

game = Game()
loop = asyncio.get_event_loop()
asyncio.get_event_loop().run_until_complete(game.startGame(True))
episodes = 50
env = JumpKingEnv(game)

for episode in range(episodes):
    done = False
    obs = env.reset()
    while True:
        random_action = env.action_space.sample()
        print("action ", random_action)
        obs, reward, done, info = env.step(random_action)
        print('reward', reward)
        print(obs)



loop.run_until_complete(game.terminate())