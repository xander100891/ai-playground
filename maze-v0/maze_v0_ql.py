"""
Maze game -- Q-learning
"""

import math
import random
from typing import Tuple

import gym
import gym_maze
import numpy as np


def calculate_learning_rate(t: int) -> float:
    """Calculates the learning rate.

    Args:
        t (int): a value used to calculate the learning rate

    Returns:
        float: the new learning rate value

    """
    return max(0.2, min(0.8, 1.0 - math.log10((t + 1) / decay_factor)))


def calculate_explore_rate(t: int) -> float:
    """Calculates the explore rate.

    Args:
        t (int): a value used to calculate the explore rate

    Returns:
        float: the new explore rate value

    """
    return max(0.001, min(0.8, 1.0 - math.log10((t + 1) / decay_factor)))


if __name__ == "__main__":
    # Flag used to enable or disable screen recording
    recording_is_enabled = False

    # Initializes the environment
    env = gym.make("maze-sample-5x5-v0")

    # Records the environment
    if recording_is_enabled:
        env = gym.wrappers.Monitor(env, "recording", video_callable=lambda episode_id: True, force=True)

    # Calculates the maze size
    maze_size: Tuple[int, int] = tuple((env.observation_space.high + np.ones(env.observation_space.shape)).astype(int))

    # Defines training related constants
    num_episodes: int = 50
    num_episode_steps: int = np.prod(maze_size, dtype=int) * 100
    num_actions: int = env.action_space.n

    # Defines learning related parameters
    decay_factor: float = np.prod(maze_size, dtype=float) / 10.0
    learning_rate: float = calculate_learning_rate(0)
    explore_rate: float = calculate_explore_rate(0)
    discount_factor: float = 0.99

    # Initializes the Q-values
    Q: np.ndarray = np.zeros(maze_size + (num_actions,), dtype=float)

    for episode in range(num_episodes):
        # Defines the total reward per episode
        total_reward: int = 0

        # Resets the environment
        observation = env.reset()

        # Gets the current state
        current_state: Tuple[int, int] = tuple(observation)

        # Renders the screen after new environment observation
        env.render(mode="human")

        # Selects a new random action or the best past action
        for episode_step in range(num_episode_steps):
            if random.uniform(0, 1) < explore_rate:
                action: int = env.action_space.sample()
            else:
                action: int = int(np.argmax(Q[current_state]))

            # Takes action and calculates the total reward
            observation, reward, done, _ = env.step(action)
            total_reward += reward

            # Gets the next state
            next_state = tuple(observation)

            # Calculates the temporary difference (TD)
            TD: float = reward + discount_factor * np.amax(Q[next_state]) - Q[current_state + (action,)]

            # Updates the Q-value by applying the Bellman equation
            Q[current_state + (action,)] += learning_rate * TD

            # Updates the current state
            current_state = next_state

            # Renders the screen after new environment observation
            env.render(mode="human")

            if done:
                print("Episode %d/%d finished after %d episode steps with total reward = %f."
                      % (episode + 1, num_episodes, episode_step + 1, total_reward))
                break

            elif episode_step >= num_episode_steps - 1:
                print("Episode %d/%d timed out at %d with total reward = %f."
                      % (episode + 1, num_episodes, episode_step + 1, total_reward))

        # Updates learning parameters
        explore_rate = calculate_explore_rate(episode)
        learning_rate = calculate_learning_rate(episode)

    # Closes the environment
    env.close()
