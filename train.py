import mcts
import keras
from board import Board
from tqdm import tqdm
import numpy as np

def fst(x):
    return x[0]

class ReinfLearn():

    def __init__(self, model):
        self.model = model

    def playGame(self):
        positionsData = []
        moveProbsData = []
        valuesData = []
        g = Board()
        while((not fst(g.isTerminal()))):
            positionsData.append(g.networkInput())
            rootEdge = mcts.Edge(None, None)
            rootEdge.N = 1
            rootNode = mcts.Node(g, rootEdge)
            mctsSearcher = mcts.MCTS(self.model)
            moveProbs = mctsSearcher.search(rootNode)
            outputVec = [ 0.0 for x in range(0, 65)]
            for (move, prob, _, _) in moveProbs:
                move_idx = g.getNetworkOutputIndex(move)
                outputVec[move_idx] = prob
            if outputVec[64] > 0.5:
                outputVec = np.zeros_like(outputVec)
                outputVec[64] = 1.0
            else:
                outputVec[64] = 0.0
                outputVec = outputVec / np.sum(outputVec)
            rand_idx = np.random.multinomial(1, outputVec)
            idx = np.where(rand_idx==1)[0][0]
            nextMove = None
            for move, _, _, _ in moveProbs:
                move_idx = g.getNetworkOutputIndex(move)
                if(move_idx == idx):
                    nextMove = move
            if(g.turn == Board.WHITE):
                valuesData.append(1)
            else:
                valuesData.append(-1)
            moveProbsData.append(outputVec)
            g.applyMove(nextMove)
        else:
            _, winner = g.isTerminal()
            for i in range(0, len(moveProbsData)):
                if(winner == Board.BLACK):
                    valuesData[i] = valuesData[i] * -1.0
                elif(winner == Board.WHITE):
                    valuesData[i] = valuesData[i] * 1.0
                else:
                    valuesData[i] = 0.0
        return (positionsData, moveProbsData, valuesData)
    

model = keras.models.load_model("new_model.keras")
learner = ReinfLearn(model)
for i in (range(0,100)):
    print("Training Iteration: "+str(i))
    allPos = []
    allMovProbs = []
    allValues = []
    for j in tqdm(range(0,10)):
        pos, movProbs, values = learner.playGame()
        allPos += pos
        allMovProbs += movProbs
        allValues += values
    npPos = np.array(allPos)
    npProbs = np.array(allMovProbs)
    npVals = np.array(allValues)
    model.fit(npPos,[npProbs, npVals], epochs=128, batch_size=16)
    model.save('model_it'+str(i)+'.keras')
