"""
multi_agents.py
---------------
THE MAZE RUNNER - Mini Project 2: Adversarial Search

This is where you write Thomas's agents (Questions 1-5).

An agent has a method getAction(gameState) that returns one of
gameState.getLegalActions(0): 'North', 'South', 'East', 'West' or 'Stop'.
Read the GameState methods in game.py before you start.

  * Thomas is agent 0. The Grievers are agents 1, 2, ..., n-1, where
    n = gameState.getNumAgents(). They move in that order.
  * ONE PLY is one move by every agent: Thomas, then each Griever. A search
    of depth 2 looks two plies ahead (Thomas, every Griever, Thomas, every
    Griever) and then calls self.evaluationFunction on the states it reaches.
  * Stop expanding at the depth limit OR when the game is over
    (state.isWin() or state.isLose()), and evaluate that state with
    self.evaluationFunction.
  * Generate successors with state.generateSuccessor(agentIndex, action),
    taking the actions in the order getLegalActions returns them. 
  * If several actions at the root tie for the best value, return the FIRST
    of them.
"""

import random

import util
from game import Agent
from maze import STOP


# ----------------------------------------------------------------------
# Q0 (worked example, not graded): the beeline
# ----------------------------------------------------------------------
class BeelineAgent(Agent):
    """
    Not a real game-playing agent: Thomas runs straight for the nearest code
    piece (or for the exit once it is open) and ignores the Grievers
    completely. It shows you how to read a GameState and how to look one move
    ahead. Try it:
        python play.py -a beeline -l duel            (often escapes)
        python play.py -a beeline -l arena_medium    (runs into a Griever)
    """

    def getAction(self, gameState):
        pos = gameState.getRunnerPosition()
        targets = list(gameState.getKeys()) or [gameState.getExit()]
        best, bestDistance = STOP, float('inf')
        for action in gameState.getLegalActions(self.index):
            nextState = gameState.generateRunnerSuccessor(action)
            nextPos = nextState.getRunnerPosition()
            d = min(gameState.mazeDistance(nextPos, t) for t in targets)
            if d < bestDistance:
                best, bestDistance = action, d
        return best


# ----------------------------------------------------------------------
# Q1: Reflex agent
# ----------------------------------------------------------------------
class ReflexAgent(Agent):
    """
    A reflex agent looks at the moves available right now and picks the one
    that leads to the best-looking state, according to evaluationFunction.
    It does not look further ahead.

    getAction is written for you. Your job is evaluationFunction.
    """

    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions()

        # Score every move and pick one of the best (ties broken at random).
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Q1: return a number that is HIGHER for better moves.

        The code below pulls some useful information out of the state that
        'action' leads to. Things worth thinking about: how far away is the
        next code piece (or the exit, once it is open)? How close are the
        Grievers? Is standing still ever a good idea?

        gameState.mazeDistance(pos1, pos2) gives the real distance through
        the maze, and util.manhattanDistance(pos1, pos2) the straight-line
        grid distance.
        """
        successorGameState = currentGameState.generateRunnerSuccessor(action)
        newPos = successorGameState.getRunnerPosition()
        newKeys = successorGameState.getKeys()
        newGrieverPositions = successorGameState.getGrieverPositions()
        
        currentPos = currentGameState.getRunnerPosition()
        "*** YOUR CODE HERE ***"
        
        if successorGameState.isWin() or successorGameState.isLose():
            return successorGameState.getScore()

        score =  successorGameState.getScore()
        targets = list(newKeys) or [successorGameState.getExit()]
        least_distance_to_key_in_new_state = min(currentGameState.mazeDistance(newPos, t) for t in targets) ## gets the minimum distance for keys avilable in current state
        if(grieverDistance):
            grieverDistance = min(currentGameState.mazeDistance(newPos, g)for g in newGrieverPositions) ## minimum distance to a griver in current state
        else:
            grieverDistance = float('inf')
        score += 10.0 / (least_distance_to_key_in_new_state) ## the closer we are the more score we get
        if(grieverDistance == 1):
            score -= 300 ## well less than 500 if game is lost
        elif(grieverDistance == 2 ):
            score -=20 ## well less than 500 if game is lost
        return score


def scoreEvaluationFunction(currentGameState):
    """
    The default evaluation function for the search agents: just the score.
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    Common parent of MinimaxAgent, AlphaBetaAgent and ExpectimaxAgent.
    You do not need to change anything here, but you will use
    self.depth and self.evaluationFunction.

    Do NOT change this class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        Agent.__init__(self, 0)     # Thomas is always agent 0
        self.evaluationFunction = globals()[evalFn] if isinstance(evalFn, str) else evalFn
        self.depth = int(depth)


# ----------------------------------------------------------------------
# Q2: Minimax
# ----------------------------------------------------------------------
class MinimaxAgent(MultiAgentSearchAgent):
    """
        Q2: Thomas maximises, every Griever minimises.
        """
    """
                Returns the minimax action from gameState, searching self.depth plies
                and evaluating the states at the bottom with self.evaluationFunction.
        
                Useful methods:
                    gameState.getLegalActions(agentIndex)
                    gameState.generateSuccessor(agentIndex, action)
                    gameState.getNumAgents()
                    gameState.isWin(), gameState.isLose()
        
                Hint: a recursive helper value(state, agentIndex, depth) is the most
                natural way to write this. Work out which agent moves next, and when
                the depth goes up.
    """
    
    "*** YOUR CODE HERE ***"
            
    def getAction(self, gameState):
        
        def value(state, agentIndex, depth):
            
            if depth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)


            nextAgent = (agentIndex + 1) % state.getNumAgents() ## for the next index
            nextDepth = depth
            if nextAgent == 0:
                nextDepth = depth + 1

            if agentIndex == 0:                      # Thomas: max
                best = float('-inf')
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    best = max(best, value(successor, nextAgent, nextDepth))
                return best
            else:                                 # Griever: min
                best = float('inf')
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    best = min(best, value(successor, nextAgent, nextDepth))
                return best


        bestScore = float('-inf')
        bestAction = None
        for action in gameState.getLegalActions(0): ## legal action for plauyer
            successor = gameState.generateSuccessor(0, action) ## successor for player
            score = value(successor, 1 % gameState.getNumAgents(),1 if gameState.getNumAgents() == 1 else 0) ## depth 1 if agents = 1
            if score > bestScore:
                bestScore = score
                bestAction = action
        return bestAction


# ----------------------------------------------------------------------
# Q3: Alpha-beta pruning
# ----------------------------------------------------------------------
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Q3: minimax with alpha-beta pruning.
    """

    def getAction(self, gameState):
        """
        Returns the same action as MinimaxAgent, but skips the parts of the
        tree that cannot change the decision.

        Do NOT prune on equality: prune only when a value is STRICTLY better
        than the bound (v > beta at Thomas's levels, v < alpha at a
        Griever's levels). Remember to update alpha at the root as well.
        """
        "*** YOUR CODE HERE ***"
        
        
        def value(state, agentIndex, depth, alpha, beta):
            
            if depth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state) ## base case return score

            nextAgent = (agentIndex + 1) % state.getNumAgents() ## next agent
            nextDepth = depth
            if nextAgent == 0:
                nextDepth = depth + 1 ## when it is turn of player again depth increases

            if agentIndex == 0:                     
                v = float('-inf')
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    v = max(v, value(successor, nextAgent, nextDepth, alpha, beta))
                    if v > beta:                     # strict: no pruning on equality
                        return v
                    alpha = max(alpha, v)
                return v
            else:                                    
                v = float('inf')
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    v = min(v, value(successor, nextAgent, nextDepth, alpha, beta))
                    if v < alpha:                    # strict: no pruning on equality
                        return v
                    beta = min(beta, v)
                return v

        numAgents = gameState.getNumAgents() 
        nextAgent = 1 % numAgents
        nextDepth = 1 if nextAgent == 0 else 0

        alpha = float('-inf')
        beta = float('inf')
        bestScore = float('-inf')
        bestAction = None
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            score = value(successor, nextAgent, nextDepth, alpha, beta)
            if score > bestScore:                    # strict: ties keep the first action
                bestScore = score
                bestAction = action
            alpha = max(alpha, bestScore)            # update alpha at the root too
        return bestAction


# ----------------------------------------------------------------------
# Q4: Expectimax
# ----------------------------------------------------------------------
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Q4: Thomas maximises; every Griever is a chance node.
    """

    def getAction(self, gameState):
        numAgents = gameState.getNumAgents()

        def nextTurn(agentIndex, depth):
            """Return (nextAgentIndex, nextDepth). Depth increases only when
            play wraps back around to Thomas (end of a ply)."""
            nextAgentIndex = (agentIndex + 1) % numAgents
            nextDepth = depth + 1 if nextAgentIndex == 0 else depth
            return nextAgentIndex, nextDepth

        def value(state, agentIndex, depth):
            # Stop at the depth limit or when the game is over (even mid-ply).
            if depth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            legalActions = state.getLegalActions(agentIndex)
            if not legalActions:                      # safety net
                return self.evaluationFunction(state)

            nextAgentIndex, nextDepth = nextTurn(agentIndex, depth)

            if agentIndex == 0:                       # Thomas: MAX node
                bestValue = float('-inf')
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    bestValue = max(bestValue, value(successor, nextAgentIndex, nextDepth))
                return bestValue

            # Griever: CHANCE node, average of children (float division)
            totalValue = 0.0
            for action in legalActions:
                successor = state.generateSuccessor(agentIndex, action)
                totalValue += value(successor, nextAgentIndex, nextDepth)
            return totalValue / len(legalActions)

        # Root: Thomas picks the action with the best expected value.
        # Strict '>' keeps the FIRST action on ties.
        nextAgentIndex, nextDepth = nextTurn(0, 0)
        bestAction, bestValue = None, float('-inf')
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            actionValue = value(successor, nextAgentIndex, nextDepth)
            if actionValue > bestValue:
                bestValue, bestAction = actionValue, action
        return bestAction


# ----------------------------------------------------------------------
# Q5: Evaluation function
# ----------------------------------------------------------------------
def betterEvaluationFunction(currentGameState):
    """
    DESCRIPTION:
    Scores a state as:
        score  -  TOUR_WEIGHT * estimated_remaining_route  -  griever_danger

    1. score: the game's own score, which already includes +50 per piece,
       -1 per move and +500/-500 for win/lose.
    2. estimated_remaining_route: a greedy tour. Starting at Thomas, repeatedly
       walk (by true maze distance) to the nearest uncollected code piece,
       then finish at the exit. Using the whole tour, not just the nearest
       piece, makes Thomas plan to visit ALL pieces (key-hunt idea from
       Project 1). Because the exit is always the last stop, the term also
       works after every piece is collected.
    3. griever_danger: only Grievers within DANGER_RADIUS maze steps matter,
       with penalty GRIEVER_WEIGHT / distance, so adjacent Grievers are
       penalised far more than distant ones (distant ones would make Thomas timid).

    Picking up a piece never lowers the value: +50 from the score outweighs
    the small change in the tour length, so Thomas won't hover next to the
    last piece.
    """


    # ---- tunable weights ----
    TOUR_WEIGHT = 1.5
    GRIEVER_WEIGHT = 100.0
    DANGER_RADIUS = 3

    # Terminal states: the score already says everything.
    if currentGameState.isWin() or currentGameState.isLose():
        return currentGameState.getScore()

    runnerPosition = currentGameState.getRunnerPosition()
    remainingKeys = list(currentGameState.getKeys())
    exitPosition = currentGameState.getExit()

    # feature 1: greedy tour through remaining keys, then the exit

    estimatedRouteLength = 0
    currentPosition = runnerPosition 
    unvisitedKeys = remainingKeys[:]
    while unvisitedKeys:
        nearestKey = min(unvisitedKeys,key=lambda key: currentGameState.mazeDistance(currentPosition, key))
        estimatedRouteLength += currentGameState.mazeDistance(currentPosition, nearestKey) ## increasing the estimated distance
        currentPosition = nearestKey
        unvisitedKeys.remove(nearestKey)
    estimatedRouteLength += currentGameState.mazeDistance(currentPosition, exitPosition)

    # feature 2: danger from nearby Grievers

    grieverDanger = 0.0
    for grieverPosition in currentGameState.getGrieverPositions():
        distanceToGriever = currentGameState.mazeDistance(runnerPosition, grieverPosition)
        if distanceToGriever <= DANGER_RADIUS:
            grieverDanger += GRIEVER_WEIGHT / max(distanceToGriever, 1) ## if wee are in danger radius, the more we are away freom griever the less the weight gets

    return currentGameState.getScore() - TOUR_WEIGHT * estimatedRouteLength - grieverDanger

# Abbreviation
better = betterEvaluationFunction
