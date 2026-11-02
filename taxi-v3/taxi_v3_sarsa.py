"""
Taxi-v3 -- SARSA
"""

import random
import numpy as np
import gym

if __name__ == "__main__":
    # Initializes the environment
    env = gym.make("Taxi-v3")

    # Defines containers for stats
    rewards = []

    # Defines training related constants
    num_episodes = 5000
    num_episode_steps = env.spec.max_episode_steps
    num_actions = env.action_space.n
    num_states = env.observation_space.n

    # Defines learning related parameters
    epsilon_decay = 0.001
    epsilon = 0.4
    gamma = 0.95
    lr = 0.1

    # Initializes the Q-values
    Q = np.zeros((num_states, num_actions))

    for episode in range(num_episodes):
        # Defines the total reward per episode
        total_reward = 0

        # Resets the environment
        state = env.reset()

        # Selects a new random action or the best past action
        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(Q[state])

        for episode_step in range(num_episode_steps):
            # Takes action and calculates the total reward
            next_state, reward, done, info = env.step(action)
            total_reward += reward

            # Selects a new random action or the best past action
            if random.uniform(0, 1) < epsilon:
                next_action = env.action_space.sample()
            else:
                next_action = np.argmax(Q[next_state])

            # Updates the Q-value by applying the Bellman equation
            Q[state][action] = Q[state][action] + lr * (reward + gamma * Q[next_state][next_action] - Q[state][action])

            # Updates the current state & action
            state = next_state
            action = next_action

            if done:
                print("Episode %d/%d finished after %d episode steps with total reward = %f."
                      % (episode + 1, num_episodes, episode_step + 1, total_reward))
                break

            elif episode_step >= num_episode_steps - 1:
                print("Episode %d/%d timed out at %d with total reward = %f."
                      % (episode + 1, num_episodes, episode_step + 1, total_reward))

        # Register total_reward
        rewards.append(total_reward)

        # Updates epsilon
        epsilon = max(0.01, epsilon - epsilon_decay)

    print('Mean score: %.3f of %i episodes' % (np.mean(rewards), num_episodes))

    # Closes the environment
    env.close()
