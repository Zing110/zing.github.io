---
title: "Hidden Markov Model"
collection: projects
type: "Undergraduate project"
permalink: /projects/HMM
venue: "SJTU-UM JI, ECE Department"
date: 2024-08-01
location: "Shanghai, China"
---

This Project aims to implement Hidden Markov Model in Pac Man Problem using python.

### What is a Hidden Markov Model (HMM)?

A Hidden Markov Model (HMM) is a statistical model that represents a system which is assumed to follow a Markov process with hidden states. In HMMs, the system is modeled as a chain of states that evolve over time, with the added complexity that the states are not directly observable (hidden). Instead, the agent can only observe some output or observation that is probabilistically related to the hidden state.

### Key Concepts in Hidden Markov Models

1. **States**: These are the hidden variables that represent the system's underlying conditions. The true state is not observable directly.

2. **Observations**: These are the visible outputs or measurements that are emitted by the system. The observations provide indirect information about the hidden states.

3. **Transition Probabilities**: These represent the probabilities of transitioning from one state to another. The transition probabilities depend only on the current state and are independent of previous states (this is the Markov property).

4. **Emission Probabilities**: These represent the probabilities of observing a particular output given the system is in a particular hidden state.

5. **Initial State Distribution**: This defines the probability distribution over the possible initial states of the system.

### HMM Process

The process of an HMM typically follows these steps:

1. **Initialization**: The model begins in some initial state, determined by the initial state distribution.
2. **State Transitions**: The system evolves from one hidden state to another based on transition probabilities.
3. **Observation Emission**: At each time step, an observation is generated according to the emission probability of the current hidden state.
4. This process is repeated over time, and the goal is often to infer the hidden state sequence from the observable data.

### Components of an HMM

An HMM is defined by the following elements:

- **States** \( S = \{s_1, s_2, ..., s_N\} \)
- **Observations** \( O = \{o_1, o_2, ..., o_M\} \)
- **Initial state distribution** \( \pi \) (probability of starting in each state)
- **Transition matrix** \( A \) (probability of transitioning from one state to another)
- **Emission matrix** \( B \) (probability of an observation given a state)

### Types of Problems in HMM

1. **Evaluation Problem**: Given a sequence of observations, compute the probability of that sequence under the HMM model. This is solved using the **Forward Algorithm**.

2. **Decoding Problem**: Given a sequence of observations, find the most likely sequence of hidden states. This is solved using the **Viterbi Algorithm**.

3. **Learning Problem**: Given a set of observations, estimate the parameters of the HMM (transition probabilities, emission probabilities, initial state distribution). This is typically solved using the **Baum-Welch Algorithm**.


### Implementation:

The doc of the requirement for the implementation is [Project explination](../assets/code/VE492/p5/p5.pdf).

The code files can be found [here](https://github.com/Zing110/VE492/tree/main/p5/P5)
