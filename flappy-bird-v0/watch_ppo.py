import gymnasium as gym
import flappy_bird_gymnasium
import pygame

from stable_baselines3 import PPO


model = PPO.load("models/ppo/best/best_model")

env = gym.make("FlappyBird-v0", render_mode="human")
obs, _ = env.reset()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    action, _ = model.predict(obs, deterministic=True)
    obs, _, terminated, truncated, _ = env.step(action)

    if terminated or truncated:
        obs, _ = env.reset()

env.close()
pygame.quit()