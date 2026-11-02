# Pendulum-v0
The inverted pendulum swing-up problem is a classic problem in the control literature. In this version of the problem, the pendulum starts in a random position, and the goal is to swing it up so it stays upright.

## OpenAI Gym
OpenAI Gym is a toolkit for developing and comparing reinforcement learning algorithms. It supports teaching agents everything from walking to playing games like pong or pinball. Gym is an open source interface to reinforcement learning tasks.

## Requirements
- [Python 3.6 or 3.7](https://www.python.org/downloads/release/python-360/)
- [CUDA Toolkit 10.1](https://developer.nvidia.com/cuda-10.1-download-archive-base)
- [cuDNN v7.6.5](https://developer.nvidia.com/cuda-10.1-download-archive-base)
- [Pipenv](https://pypi.org/project/pipenv/)

## How to install the packages
You can install the required Python packages using the following command:
- `pipenv sync`

## Deep Deterministic Policy Gradient
Deep Deterministic Policy Gradient (DDPG) is a model-free off-policy algorithm for learning continous actions.

It combines ideas from DPG (Deterministic Policy Gradient) and DQN (Deep Q-Network). It uses Experience Replay and slow-learning target networks from DQN, and it is based on DPG, which can operate over continuous action spaces.

More details can be found in [this](https://arxiv.org/pdf/1509.02971.pdf) paper.

## How to train the agent
You can train the agent using the following command:
- `pipenv run python ddpg_pendulum.py`
