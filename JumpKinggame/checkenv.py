from stable_baselines3.common.env_checker import check_env
from env import JumpKingEnv
from game import Game
import asyncio

game = Game()
asyncio.get_event_loop().run_until_complete(game.startGame(True))

env = JumpKingEnv(game)
check_env(env)
asyncio.get_event_loop().run_until_complete(game.terminate())