import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for i in range(self.iterations):
            # Create a temporary copy of the values
            temp_values = self.values.copy()
            
            # For each state in the MDP
            for state in self.mdp.getStates():
                if self.mdp.isTerminal(state):
                    continue
                
                # Find the maximum value action
                max_value = float('-inf')
                for action in self.mdp.getPossibleActions(state):
                    current_value = 0
                    for next_state, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                        reward = self.mdp.getReward(state, action, next_state)
                        current_value += prob * (reward + self.discount * temp_values[next_state])
                    
                    max_value = max(max_value, current_value)
                
                # Update the value of the state
                self.values[state] = max_value


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        q_value = 0
        # For each next state and its probability
        for next_state, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            reward = self.mdp.getReward(state, action, next_state)
            q_value += prob * (reward + self.discount * self.values[next_state])
        return q_value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None

        best_action = None
        max_value = float('-inf')
        # For each possible action
        for action in self.mdp.getPossibleActions(state):
            q_value = self.computeQValueFromValues(state, action)
            # Update max_value and best_action if found higher Q-value
            if q_value > max_value:
                max_value = q_value
                best_action = action
        return best_action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        num_states = len(states)

        for i in range(self.iterations):
            # Get the state to update in this iteration
            state = states[i % num_states]

            # Skip if the state is terminal
            if self.mdp.isTerminal(state):
                continue

            # Find the maximum value action
            max_value = float('-inf')
            for action in self.mdp.getPossibleActions(state):
                current_value = 0
                for next_state, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                    reward = self.mdp.getReward(state, action, next_state)
                    current_value += prob * (reward + self.discount * self.values[next_state])
                
                max_value = max(max_value, current_value)
            
            # Update the value of the state
            self.values[state] = max_value

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
         # Initialize an empty priority queue
        queue = util.PriorityQueue()

        # For each non-terminal state s do
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                diff = abs(self.values[state] - max([self.computeQValueFromValues(state, action) for action in self.mdp.getPossibleActions(state)]))
                queue.update(state, -diff)

        # For the required number of iterations
        for _ in range(self.iterations):
            # If the queue is empty, then terminate
            if queue.isEmpty():
                break

            # Pop a state s off the queue
            state = queue.pop()

            # Update s's value (if it is not a terminal state) in self.values
            if not self.mdp.isTerminal(state):
                self.values[state] = max([self.computeQValueFromValues(state, action) for action in self.mdp.getPossibleActions(state)])

            # For each predecessor p of s, do
            for predecessor in self.mdp.getStates():
                if self.mdp.isTerminal(predecessor):
                    continue

                # Find the absolute value of the difference between the current value of p in self.values and the highest Q-value across all possible actions from p (this represents what the value should be)
                diff = abs(self.values[predecessor] - max([self.computeQValueFromValues(predecessor, action) for action in self.mdp.getPossibleActions(predecessor)]))

                # If diff > theta, push p into the queue with priority -diff
                if diff > self.theta:
                    queue.update(predecessor, -diff)

