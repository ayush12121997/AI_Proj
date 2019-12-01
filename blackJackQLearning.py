import blackJackEnv
import numpy as np
import random as randi
import time


# noinspection PyRedundantParentheses
class solveBlackJacK:
    numEpisodes = 1500000
    merges = [[1, 2, 3], [4, 5, 6, 7], [8, 9, 10]]
    # merges = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]
    # merges = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]

    def __init__(self):
        self.learningRate = 0.5
        self.startTime = 0
        self.endTime = 0
        self.explorationRate = 0.5
        self.discountRate = 0.9
        self.env = blackJackEnv.blackJack()
        self.actions = [1, 0]
        self.allRewards = []
        self.qTable = dict()
        self.decay = 0.00001
        self.minExplorationRate = 0.00005

    def merge(self, state):
        count = list(state[-11:])
        merged = []
        for grp in self.merges:
            temp = 0
            for i in grp:
                temp += count[i]
            merged.append(temp)
        return tuple(list(state[:-11]) + merged)
        # return tuple(list(state[:-11]))

    def new_actions(self):
        return [0, 0]

    def decay_epsilon(self):
        self.explorationRate = self.minExplorationRate + (self.explorationRate - self.minExplorationRate) * (np.exp(-self.decay))
        if (not (1 > self.explorationRate > self.minExplorationRate)):
            print("Error : Wrong decay function in decay_espilon ", self.explorationRate)

    def play(self):
        self.startTime = time.perf_counter()
        for episode in range(self.numEpisodes):
            gameState, isNatural = self.env.reset()
            gameState = self.merge(gameState)
            done = False
            rewardCurrEpisode = 0

            while (not done):
                explorationValue = randi.uniform(0, 1)
                if (isNatural):
                    action = 0

                elif (explorationValue < self.explorationRate):
                    action = np.random.choice(self.actions)
                else:
                    if (gameState not in self.qTable):
                        self.qTable[gameState] = self.new_actions()
                    if (self.qTable[gameState][0] > self.qTable[gameState][1]):
                        action = 0
                    elif (self.qTable[gameState][0] < self.qTable[gameState][1]):
                        action = 1
                    else:
                        action = np.random.choice(self.actions)

                new_gameState, reward, done, isNatural = self.env.step(action)
                new_gameState = self.merge(new_gameState)

                if (gameState not in self.qTable):
                    self.qTable[gameState] = self.new_actions()
                if (new_gameState not in self.qTable):
                    self.qTable[new_gameState] = self.new_actions()
                self.qTable[gameState][action] += self.learningRate * (reward + self.discountRate * np.max(self.qTable[new_gameState]) - self.qTable[gameState][action])
                # if (gameState[1] == 21 and np.argmax(self.qTable[gameState]) == 1):
                #     print(gameState, reward, action, new_gameState)
                #     print(self.qTable[gameState])
                #     print(self.qTable[new_gameState])

                gameState = new_gameState
                rewardCurrEpisode += reward
                if (done):
                    break

            if (episode < self.numEpisodes * 0.4):
                self.decay = 1 / self.numEpisodes
            else:
                self.decay = 10 / self.numEpisodes
            self.decay_epsilon()
            if (episode % (self.numEpisodes / 100) == 0):
                print("Episode :", episode, "Reward :", rewardCurrEpisode, " Table size :", len(self.qTable), " Exp rate :", self.explorationRate)
            self.allRewards.append(rewardCurrEpisode)

        self.endTime = time.perf_counter()

        option_count = [[0, 0] for i in range(35)]
        for i in self.qTable:
            option_count[i[1]][np.argmax(self.qTable[i])] += 1
        print(option_count)

    def printResults(self):

        gap = self.numEpisodes / 100
        rewardsForEveryHundred = np.split(np.array(self.allRewards), self.numEpisodes / gap)
        count = gap
        for r in rewardsForEveryHundred:
            print(count, ": ", str(sum(r / gap)))
            count += gap


if __name__ == "__main__":
    solver = solveBlackJacK()
    solver.play()
    solver.printResults()
