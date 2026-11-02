# CartPole-v1
A pole is attached by an un-actuated joint to a cart, which moves along a frictionless track. The system is controlled by applying a force of +1 or -1 to the cart. The pendulum starts upright, and the goal is to prevent it from falling over. A reward of +1 is provided for every timestep that the pole remains upright. The episode ends when the pole is more than 15 degrees from vertical, or the cart moves more than 2.4 units from the center.

## OpenAI Gym
OpenAI Gym is a toolkit for developing and comparing reinforcement learning algorithms. It supports teaching agents everything from walking to playing games like pong or pinball. Gym is an open source interface to reinforcement learning tasks.

## Reinforcement learning algorithms
- Deep Q-Learning (off-policy, model-free)

## Demo video
https://www.youtube.com/watch?v=YB9S74k3yhc

## Requirements
- [Python 3.6 or 3.7](https://www.python.org/downloads/release/python-360/)
- [CUDA Toolkit 10.1](https://developer.nvidia.com/cuda-10.1-download-archive-base)
- [cuDNN v7.6.5](https://developer.nvidia.com/cuda-10.1-download-archive-base)
- [Pipenv](https://pypi.org/project/pipenv/)

## How to install the packages
You can install the required Python packages using the following command:
- `pipenv sync`

## How to run it
You can run the script using the following command: 
- `pipenv run python cartpole_v1_dqn.py`
