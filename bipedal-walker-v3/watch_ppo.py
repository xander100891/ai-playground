import gymnasium as gym
import pygame

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize


MODEL_PATH = "models/ppo/best/best_model"
VEC_PATH = "models/ppo/best/vec_normalize.pkl"


def make_env():
    return gym.make("BipedalWalker-v3", render_mode="human")


env = DummyVecEnv([make_env])

env = VecNormalize.load(VEC_PATH, env)
env.training = False
env.norm_reward = False

model = PPO.load(MODEL_PATH, env=env)

obs = env.reset()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)

    if done[0]:
        obs = env.reset()

env.close()
pygame.quit()