import os
import gymnasium as gym

from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import BaseCallback, CheckpointCallback, EvalCallback
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize


MODEL_DIR = "models/ppo"
BEST_DIR = "models/ppo/best"
CHECKPOINT_DIR = "models/ppo/checkpoints"
LOG_DIR = "logs/ppo"

N_ENVS = 4
TOTAL_TIMESTEPS = 5_000_000

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(BEST_DIR, exist_ok=True)
os.makedirs(CHECKPOINT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)


def make_env():
    return Monitor(gym.make("BipedalWalker-v3"))


class SaveVecNormalizeCallback(BaseCallback):
    def __init__(self, save_path: str):
        super().__init__()
        self.save_path = save_path

    def _on_step(self) -> bool:
        vec_normalize = self.model.get_vec_normalize_env()

        if vec_normalize is not None:
            vec_normalize.save(os.path.join(self.save_path, "vec_normalize.pkl"))

        return True


env = DummyVecEnv([make_env for _ in range(N_ENVS)])
env = VecNormalize(
    env,
    norm_obs=True,
    norm_reward=True,
    clip_obs=10.0,
)

eval_env = DummyVecEnv([make_env])
eval_env = VecNormalize(
    eval_env,
    norm_obs=True,
    norm_reward=False,
    clip_obs=10.0,
)
eval_env.training = False

checkpoint_callback = CheckpointCallback(
    save_freq=max(50_000 // N_ENVS, 1),
    save_path=CHECKPOINT_DIR,
    name_prefix="ppo_bipedal",
    save_vecnormalize=True,
)

save_best_vecnormalize_callback = SaveVecNormalizeCallback(BEST_DIR)

eval_callback = EvalCallback(
    eval_env,
    best_model_save_path=BEST_DIR,
    log_path=LOG_DIR,
    eval_freq=max(25_000 // N_ENVS, 1),
    deterministic=True,
    render=False,
    callback_on_new_best=save_best_vecnormalize_callback,
)

model = PPO(
    policy="MlpPolicy",
    env=env,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    gamma=0.999,
    gae_lambda=0.95,
    clip_range=0.18,
    ent_coef=0.0,
    vf_coef=0.5,
    max_grad_norm=0.5,
    policy_kwargs=dict(net_arch=[256, 256]),
    verbose=1,
    tensorboard_log=LOG_DIR,
)

model.learn(
    total_timesteps=TOTAL_TIMESTEPS,
    callback=[checkpoint_callback, eval_callback],
    progress_bar=True,
)

model.save(os.path.join(MODEL_DIR, "ppo_bipedal_final"))
env.save(os.path.join(MODEL_DIR, "vec_normalize_final.pkl"))

env.close()
eval_env.close()

print("Training finished.")
