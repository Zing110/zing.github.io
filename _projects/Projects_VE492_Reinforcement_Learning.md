---
title: "Reinforcement Learning"
collection: projects
type: "Undergraduate project"
permalink: /projects/RL
venue: "SJTU-UM JI, ECE Department"
date: 2024-08-01
location: "Shanghai, China"
---

This Project aims to implement Reinforcement Learning in Pac Man Problem using python.

### What is Reinforcement Learning?

Reinforcement Learning (RL) is a branch of machine learning where an agent learns to make decisions by interacting with its environment. The goal of the agent is to maximize a reward signal through trial and error.

### Key Concepts in Reinforcement Learning

1. **Agent**: The learner or decision maker. It takes actions in the environment to achieve a goal.

2. **Environment**: The external system with which the agent interacts. It provides feedback to the agent based on its actions.

3. **State**: A representation of the current situation or configuration of the environment. It contains all the information needed for the agent to make a decision.

4. **Action**: A decision or move that the agent can take to interact with the environment. Actions affect the state of the environment.

5. **Reward**: A scalar value that indicates how good or bad the agent's action was in the context of its objective. The agent’s goal is to maximize the cumulative reward.

6. **Policy**: A strategy that the agent follows to choose actions given states. The policy can be deterministic or stochastic.

7. **Value Function**: A function that estimates the expected return (future cumulative reward) for being in a particular state or taking a particular action.

8. **Q-Function**: A function that estimates the expected return of taking a particular action in a particular state and following the optimal policy thereafter.

9. **Discount Factor (γ)**: A factor that determines how much future rewards are taken into consideration. A discount factor of 1 means future rewards are as important as immediate ones, while a factor close to 0 makes the agent focus mostly on immediate rewards.

### RL Process

The RL process typically follows these steps:
1. The **agent** observes the **state** of the environment.
2. The agent selects an **action** based on its policy.
3. The environment reacts to the action and provides the agent with a new **state** and a **reward**.
4. The agent updates its policy based on the received reward, aiming to maximize future rewards.
5. This process is repeated over multiple steps (episodes) until the agent converges to an optimal policy.

### Types of Reinforcement Learning

1. **Model-Free RL**: The agent learns a policy directly from interactions without building a model of the environment.
   - **Value-based**: The agent tries to estimate the value function (e.g., Q-learning).
   - **Policy-based**: The agent directly learns the policy (e.g., REINFORCE).
   - **Actor-Critic**: Combines value-based and policy-based methods to learn both a value function and a policy (e.g., A3C).

2. **Model-Based RL**: The agent builds a model of the environment to plan ahead and make decisions.



### Implementation:

The doc for how the requirement of the implementation is [Project explination](../assets/code/VE492/p4/p4.pdf).

The code files can be found [here](https://github.com/Zing110/VE492/tree/main/p4/P4)
