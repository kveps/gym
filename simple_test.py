import gym
import numpy as np
import random
from gym.envs import snake

env = snake.SnakeEnv()
num_actions = env.get_num_actions()

for i in range(0, 1000):
	env.reset()
	in_play = True
	while in_play:
		ob, reward, episode_over, joke = env.step(random.randint(0,num_actions - 1))
		in_play = ~episode_over
		env.render()

