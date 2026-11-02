# 🐦 Flappy Bird RL (Gymnasium + PPO)

Train an AI agent to play Flappy Bird using reinforcement learning with Stable-Baselines3 and Gymnasium.

## 🚀 Features

- PPO agent that learns to play Flappy Bird
- Automatic checkpoint saving
- Best model selection during training
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

- train for 1,000,000 timesteps
- save checkpoints every 25k steps
- automatically save the best model

## 📊 Monitor Training

```bash
pipenv run tensorboard --logdir logs
```

Open in browser:

```text
http://localhost:6006
```

## 👀 Watch the Agent

```bash
pipenv run python watch_ppo.py
```

This loads:

```text
models/ppo/best/best_model
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

```text
200k steps  → learning survival
400k steps  → stable gameplay
700k+ steps → strong agent, ep_len_mean > 1000
```

## ⚠️ Notes

- PPO training may fluctuate. This is normal.
- The final model is not always the best model.
- Use `models/ppo/best/best_model` for watching and recording.
- Occasional Gymnasium observation-space warnings can usually be ignored if training is working.

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

- Tune PPO hyperparameters
- Compare PPO vs DQN
- Train on pixel input with CNN policy
- Add parallel environments for faster training
