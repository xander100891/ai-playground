import os
import gymnasium as gym
import flappy_bird_gymnasium

from gymnasium.wrappers import RecordVideo
from stable_baselines3 import PPO


VIDEO_DIR = "videos/ppo"
os.makedirs(VIDEO_DIR, exist_ok=True)

env = gym.make("FlappyBird-v0", render_mode="rgb_array")

env = RecordVideo(
    env,
    video_folder=VIDEO_DIR,
    episode_trigger=lambda episode_id: episode_id == 0,
    name_prefix="ppo-flappy",
)

model = PPO.load("models/ppo/best/best_model", env=env)

obs, _ = env.reset()

for _ in range(3000):
    action, _ = model.predict(obs, deterministic=True)
    obs, _, terminated, truncated, _ = env.step(action)

    if terminated or truncated:
        break

env.close()

print(f"Video saved in {VIDEO_DIR}")