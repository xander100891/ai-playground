import os
import gymnasium as gym

from gymnasium.wrappers import RecordVideo
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize


VIDEO_DIR = "videos/ppo"
MODEL_PATH = "models/ppo/best/best_model"
VEC_PATH = "models/ppo/best/vec_normalize.pkl"

os.makedirs(VIDEO_DIR, exist_ok=True)


def make_env():
    return gym.make("BipedalWalker-v3", render_mode="rgb_array")


env = DummyVecEnv([make_env])

env = VecNormalize.load(VEC_PATH, env)
env.training = False
env.norm_reward = False

# IMPORTANT: RecordVideo must wrap the underlying env
env = RecordVideo(
    env,
    video_folder=VIDEO_DIR,
    episode_trigger=lambda ep: ep == 0,
)

model = PPO.load(MODEL_PATH, env=env)

obs = env.reset()

for _ in range(5000):
    action, _ = model.predict(obs, deterministic=True)
    obs, _, done, _ = env.step(action)

    if done[0]:
        break

env.close()

print(f"Video saved in {VIDEO_DIR}")