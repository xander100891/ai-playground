# 🤖 Bipedal Walker RL (Gymnasium + PPO)

Train an AI agent to learn how to walk using reinforcement learning with Stable-Baselines3 and Gymnasium.

## 🚀 Features

- PPO agent that learns continuous control (4 joints)
- Automatic checkpoint saving
- Best model selection during training
- Observation & reward normalization (VecNormalize)
- TensorBoard logging
- Video recording of trained agent

## 📦 Installation

```bash
pipenv sync
```

## 🧠 Training

```bash
pipenv run python train_ppo.py
```

This will:

- train for up to 5,000,000 timesteps
- use multiple environments for faster learning
- normalize observations and rewards
- save checkpoints during training
- automatically save the best model

## 📊 Monitor Training

```bash
pipenv run tensorboard --logdir logs
```

Open in browser:

```
http://localhost:6006
```

## 👀 Watch the Agent

```bash
pipenv run python watch_ppo.py
```

This loads:

```text
models/ppo/best/best_model  
models/ppo/best/vec_normalize.pkl  
```

## 🎥 Record a Video

```bash
pipenv run python record_ppo.py
```

Video output:

```text
videos/ppo/
```

## 🧠 Results

Typical training progression:

0–200k    → random falling  
200k–600k → crawling / unstable movement  
600k–1M   → walking starts  
1M–3M     → stable walking  
3M+       → strong agent (reward 200+)  

## ⚠️ Notes

- PPO training may fluctuate. This is normal.
- The final model is not always the best model.
- Use models/ppo/best/best_model for evaluation.
- VecNormalize must be loaded when watching/recording.
- Box2D installation may require additional setup on Windows.

## 📁 Project Structure

```text
.
├── train_ppo.py
├── watch_ppo.py
├── record_ppo.py
├── models/
├── logs/
└── videos/
```

## 🛠️ Tech Stack

- Gymnasium
- Stable-Baselines3
- PyTorch
- Pygame
- Pipenv

## 📌 Future Improvements

- Try SAC / TD3 for improved performance
- Increase number of parallel environments
- Tune PPO hyperparameters further
- Train on BipedalWalkerHardcore-v3
