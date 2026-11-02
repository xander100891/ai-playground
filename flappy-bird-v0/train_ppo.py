import os
import gymnasium as gym
import flappy_bird_gymnasium

from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback


MODEL_DIR = "models/ppo"
BEST_DIR = "models/ppo/best"
CHECKPOINT_DIR = "models/ppo/checkpoints"
LOG_DIR = "logs/ppo"

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(BEST_DIR, exist_ok=True)
os.makedirs(CHECKPOINT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

def make_env():
    return Monitor(gym.make("FlappyBird-v0"))


env = make_env()
eval_env = make_env()

checkpoint_callback = CheckpointCallback(
    save_freq=25_000,
    save_path=f"{MODEL_DIR}/checkpoints",
    name_prefix="ppo_flappy",
)

eval_callback = EvalCallback(
    eval_env,
    best_model_save_path=BEST_DIR,
    log_path=LOG_DIR,
    eval_freq=25_000,
    deterministic=True,
    render=False,
)

model = PPO(
    policy="MlpPolicy",
    env=env,
    learning_rate=1e-4,
    n_steps=1024,
    batch_size=64,
    n_epochs=5,
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.15,
    ent_coef=0.002,
    vf_coef=0.5,
    max_grad_norm=0.5,
    policy_kwargs=dict(net_arch=[256, 256]),
    verbose=1,
    tensorboard_log=LOG_DIR,
)

model.learn(
    total_timesteps=1_000_000,
    callback=[checkpoint_callback, eval_callback],
    progress_bar=True,
)

model.save(f"{MODEL_DIR}/ppo_flappy_final")

env.close()
eval_env.close()

print("Training finished.")