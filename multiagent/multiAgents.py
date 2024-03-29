# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        """
        for x in scores:
          print "score I can get: ", x

        print "best score in action: ",bestScore
        print "best indices", bestIndices
        print "chosen index", chosenIndex
        """
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
        newpos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        score = successorGameState.getScore()
        foodList=newFood.asList()
     
        newGhostpos=successorGameState.getGhostPosition(1)

        ghostdistance=manhattanDistance(newpos,newGhostpos)
        capList=successorGameState.getCapsules()

        #scaredy ghost
        if newpos in capList:
          score+=10/ghostdistance
 

        else:  
    

          fdistance=[]
          for food in foodList:
            fdistance.append(manhattanDistance(food, newpos))

          if len(fdistance)!=0:
            score+=10/min(fdistance)


          if newScaredTimes[0]==0:
            if ghostdistance<5:
             score-=5
            if ghostdistance<2:
             score-=10
            if ghostdistance<15:
        
              if ghostdistance!=0:
                score+=ghostdistance/2
          else:
             if ghostdistance!=0:
                if ghostdistance<15:
                 score+= 15/ghostdistance
                score+=5/ghostdistance
         

          

        """
        print "ghostpos:",newGhostpos
        print "mypos:",newpos
        print "ghostdist:",ghostdistance
        print "min food distance:",min(fdistance)
        print "calculatedscore:",score

        """
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
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()
        depth = self.depth
        bestAction = None

        def value(gameState, depth, agentIndex):
            #print "depth ", depth
            #print "agentIndex ", agentIndex
            if agentIndex > (numAgents-1):
                agentIndex = 0
                depth-=1
            if (depth == 0) or gameState.isWin() or gameState.isLose():
                #print self.evaluationFunction(gameState)
                return (self.evaluationFunction(gameState), None)
           # print "agentIndex ", agentIndex
            if agentIndex == 0:
                return maxValue(gameState, depth, agentIndex)
            if agentIndex > 0:
                return minValue(gameState, depth, agentIndex)

        def maxValue(gameState, depth, agentIndex):
            v = float('-inf')
            bestAction = None
            legalActions = gameState.getLegalActions(agentIndex)
            for action in legalActions:
                successorState = gameState.generateSuccessor(agentIndex, action)
                val = value(successorState, depth, agentIndex+1)[0]
                if val > v:
                    v = val
                    bestAction = action
                #v = max(v, value(successorState, depth-1, agentIndex+1))
            return (v, bestAction)            
        def minValue(gameState, depth, agentIndex):
            v = float('inf')
            legalActions = gameState.getLegalActions(agentIndex)
            for action in legalActions:
                successorState = gameState.generateSuccessor(agentIndex, action)
                val = value(successorState, depth, agentIndex+1)[0]
                if val < v:
                  v = val
                  bestAction = action
               # v = min(v, value(successorState, depth, agentIndex+1)[0])
            return (v, bestAction)

        minimax = value(gameState, depth, 0)
        #print "move chosen!!! ",  minimax
        return minimax[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()
        depth = self.depth
        bestAction = None

        def value(gameState, depth, agentIndex, alpha, beta):
            #print "depth ", depth
            #print "agentIndex ", agentIndex
            if agentIndex > (numAgents-1):
                agentIndex = 0
                depth-=1
            if (depth == 0) or gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState), None)
            if agentIndex == 0:
                return maxValue(gameState, depth, agentIndex, alpha, beta)
            if agentIndex > 0:
                return minValue(gameState, depth, agentIndex, alpha, beta)

        def maxValue(gameState, depth, agentIndex, alpha, beta):
            v = float('-inf')
            bestAction = None
            legalActions = gameState.getLegalActions(agentIndex)
            for action in legalActions:
                successorState = gameState.generateSuccessor(agentIndex, action)
                val = value(successorState, depth, agentIndex+1, alpha, beta)[0]
                if val > v:
                    v = val
                    bestAction = action
                if v > beta:
                  return (v, bestAction)
                alpha = max(alpha, v)
            return (v, bestAction)            
        def minValue(gameState, depth, agentIndex, alpha, beta):
            v = float('inf')
            legalActions = gameState.getLegalActions(agentIndex)
            for action in legalActions:
                successorState = gameState.generateSuccessor(agentIndex, action)
                val = value(successorState, depth, agentIndex+1, alpha, beta)[0]
                if val < v:
                  v = val
                  bestAction = action
                if v < alpha:
                  return (v, bestAction)
                beta = min(beta, v)
            return (v, bestAction)

        alphabeta = value(gameState, depth, 0, float('-inf'), float('inf'))
        return alphabeta[1]

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
        numAgents = gameState.getNumAgents()
        depth = self.depth
        bestAction = None

        def value(gameState, depth, agentIndex):
            if agentIndex > (numAgents-1):
                agentIndex = 0
                depth-=1
            if (depth == 0) or gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState), None)
            if agentIndex == 0:
                return maxValue(gameState, depth, agentIndex)
            if agentIndex > 0:
                return expValue(gameState, depth, agentIndex)

        def maxValue(gameState, depth, agentIndex):
            v = float('-inf')
            bestAction = None
            legalActions = gameState.getLegalActions(agentIndex)
            for action in legalActions:
                successorState = gameState.generateSuccessor(agentIndex, action)
                val = value(successorState, depth, agentIndex+1)[0]
                if val > v:
                    v = val
                    bestAction = action
            return (v, bestAction)            
        def expValue(gameState, depth, agentIndex):
            v = 0
            legalActions = gameState.getLegalActions(agentIndex)
            numActions = len(legalActions)
            for action in legalActions:
                successorState = gameState.generateSuccessor(agentIndex, action)
                v += value(successorState, depth, agentIndex+1)[0] * (1.0/numActions)
            return (v, bestAction)

        expectimax = value(gameState, depth, 0)
        return expectimax[1]


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    score = currentGameState.getScore()
    foodList=food.asList()
     
    ghostpos=currentGameState.getGhostPosition(1)

    ghostdistance=manhattanDistance(pos,ghostpos)
    capList=currentGameState.getCapsules()

    #scaredy ghost
    if pos in capList:
      score+=10.0/ghostdistance
 

    else:  
      fdistance=[]
      for food in foodList:
        fdistance.append(manhattanDistance(food, pos))

        if len(fdistance)!=0:
          score+=10.0/min(fdistance)
        
        if scaredTimes[0]==0:
          if ghostdistance<5:
            score-=5
          if ghostdistance<2:
            score-=10
          if ghostdistance<15:
            if ghostdistance!=0:
              score+=ghostdistance/2
        else:
          if ghostdistance!=0:
            if ghostdistance<15:
              score+= 15.0/ghostdistance
            score+=5.0/ghostdistance
      return score 

# Abbreviation
better = betterEvaluationFunction

