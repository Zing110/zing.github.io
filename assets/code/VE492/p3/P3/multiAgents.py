from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
         # Initialize the score with the successor game state score
        score = successorGameState.getScore()

        # Penalize the score if the new position is close to a ghost
        for ghostState in newGhostStates:
            distance = manhattanDistance(newPos, ghostState.getPosition())
            if distance > 0:
                if ghostState.scaredTimer > 0:  # If the ghost is scared
                    score += 10 / distance  # Encourage going towards the ghost
                else:
                    score -= 10 / distance  # Discourage going towards the ghost

        # Reward the score if the new position is on a food pellet
        if newPos in newFood.asList():
            score += 10

        # Reward based on the distance to the closest food
        foodDistances = [manhattanDistance(newPos, foodPos) for foodPos in newFood.asList()]
        if foodDistances:
            score += 1 / min(foodDistances)

        return score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def minimax(agent, depth, gameState):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)

            if agent == 0:  # Pacman is the maximizing agent
                return max(minimax(1, depth, gameState.generateSuccessor(agent, newState)) for newState in gameState.getLegalActions(agent))
            else:  # Ghosts are the minimizing agents
                nextAgent = agent + 1  # Get the next agent
                if nextAgent == gameState.getNumAgents():  # Check if all agents have been processed
                    nextAgent = 0  # Start over with Pacman
                    depth += 1  # Increase the depth
                return min(minimax(nextAgent, depth, gameState.generateSuccessor(agent, newState)) for newState in gameState.getLegalActions(agent))

        # Pacman starts the game, so we start with agent 0 at depth 0
        return max(gameState.getLegalActions(0), key=lambda x: minimax(1, 0, gameState.generateSuccessor(0, x)))

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alphabeta(agent, depth, gameState, alpha, beta):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)

            if agent == 0:  # Pacman is the maximizing agent
                value = -float('inf')
                for newState in gameState.getLegalActions(agent):
                    value = max(value, alphabeta(1, depth, gameState.generateSuccessor(agent, newState), alpha, beta))
                    if value > beta:
                        return value
                    alpha = max(alpha, value)
                return value
            else:  # Ghosts are the minimizing agents
                nextAgent = agent + 1  # Get the next agent
                if nextAgent == gameState.getNumAgents():  # Check if all agents have been processed
                    nextAgent = 0  # Start over with Pacman
                    depth += 1  # Increase the depth
                value = float('inf')
                for newState in gameState.getLegalActions(agent):
                    value = min(value, alphabeta(nextAgent, depth, gameState.generateSuccessor(agent, newState), alpha, beta))
                    if value < alpha:
                        return value
                    beta = min(beta, value)
                return value

        # Pacman starts the game, so we start with agent 0 at depth 0
        alpha = -float('inf')
        beta = float('inf')
        bestScore = -float('inf')
        bestAction = Directions.STOP
        for action in gameState.getLegalActions(0):
            nextState = gameState.generateSuccessor(0, action)
            score = alphabeta(1, 0, nextState, alpha, beta)
            if score > bestScore:
                bestScore = score
                bestAction = action
            if bestScore > beta:
                return bestAction
            alpha = max(alpha, bestScore)
        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectimax(agent, depth, gameState):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)

            if agent == 0:  # Pacman is the maximizing agent
                return max(expectimax(1, depth, gameState.generateSuccessor(agent, newState)) for newState in gameState.getLegalActions(agent))
            else:  # Ghosts are the minimizing agents
                nextAgent = agent + 1  # Get the next agent
                if nextAgent == gameState.getNumAgents():  # Check if all agents have been processed
                    nextAgent = 0  # Start over with Pacman
                    depth += 1  # Increase the depth
                return sum(expectimax(nextAgent, depth, gameState.generateSuccessor(agent, newState)) for newState in gameState.getLegalActions(agent)) / len(gameState.getLegalActions(agent))

        # Pacman starts the game, so we start with agent 0 at depth 0
        return max(gameState.getLegalActions(0), key=lambda x: expectimax(1, 0, gameState.generateSuccessor(0, x)))

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    from util import manhattanDistance
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    foodScore = 0
    if food.count() != 0:
        foodScore = 1 / (min([manhattanDistance(pos, foodPos) for foodPos in food.asList()]))

    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    ghostDistances = []
    for i in range(len(ghostStates)):
        distance = manhattanDistance(pos, ghostStates[i].getPosition()) + scaredTimes[i]
        if distance != 0:
            ghostDistances.append(1 / distance)
        else:
            ghostDistances.append(distance)
    return foodScore - 10*max(ghostDistances) + currentGameState.getScore()


better = betterEvaluationFunction
