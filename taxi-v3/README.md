# Taxi-v3
There are 4 locations (labeled by different letters) and your job is to pick up the passenger at one location and drop him off in another. You receive +20 points for a successful dropoff, and lose 1 point for every timestep it takes. There is also a 10 point penalty for illegal pick-up and drop-off actions.

## Reinforcement learning algorithms
- SARSA (on-policy, model-free)
- Q-learning (off-policy, model-free)

## Requirements
- [Python 3.6 or 3.7](https://www.python.org/downloads/release/python-360/)
- [Pipenv](https://pypi.org/project/pipenv/)

## How to install the packages
You can install the required Python packages using the following command:
- `pipenv sync`

## How to train the agent
You can train the agent using the following command:
- `pipenv run python taxi_v3_ql.py`
- `pipenv run python taxi_v3_sarsa.py`
