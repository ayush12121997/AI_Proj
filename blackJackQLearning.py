import blackJackEnv
import numpy as np
import random as randi


# noinspection PyRedundantParentheses
class solveBlackJacK:
    numEpisodes = 1000000
    merges = [[1, 2, 3], [4, 5, 6, 7], [8, 9, 10]]

    def __init__(self):
        self.learningRate = 0.01
        self.explorationRate = 0.3
        self.discountRate = 0.99
        self.env = blackJackEnv.blackJack()
        self.actions = [1, 0]
        self.allRewards = []
        self.qTable = {}
        self.decay = 0.00005
        self.decay_freq = 100
        self.minExplorationRate = 0.005

    def merge(self, state):
        count = list(state[-10:])
        merged = []
        for grp in self.merges:
            temp = 0
            for i in grp:
                temp += count[i - 1]
            merged.append(temp)
        return tuple(list(state[:-10]))


    def new_actions(self):
        return [0, np.random.uniform(-(0.000001), 0.000001)]

    def decay_epsilon(self):
        self.explorationRate = self.minExplorationRate + (self.explorationRate - self.minExplorationRate) * (np.exp(-self.decay))
        if(not (1 > self.explorationRate > self.minExplorationRate)):
            print("Wrong decay function ", self.explorationRate)

    def play(self):
        for episode in range(self.numEpisodes):
            self.env.reset()
            gameState = self.merge(self.env.return_state())
            done = False
            rewardCurrEpisode = 0
            while(not done):
                explorationValue = randi.uniform(0, 1)
                if (explorationValue < self.explorationRate):
                    action = np.random.choice(self.actions)
                else:
                    if (gameState not in self.qTable):
                        self.qTable[gameState] = self.new_actions()
                    action = np.argmax(self.qTable[gameState])
                new_gameState, reward, done = self.env.step(action)
                new_gameState = self.merge(new_gameState)

                if (gameState not in self.qTable):
                    self.qTable[gameState] = self.new_actions()
                if (new_gameState not in self.qTable):
                    self.qTable[new_gameState] = self.new_actions()

                self.qTable[gameState][action] += self.learningRate * (reward + self.discountRate * np.max(self.qTable[new_gameState]) - self.qTable[gameState][action])
                gameState = new_gameState
                rewardCurrEpisode += reward

                if (done):
                    break
            self.decay_epsilon()
            if (episode % 10000 == 0):
                print("Episode : ", episode, "Reward : ", rewardCurrEpisode, " Table density : ", len(self.qTable), " Exp rate : ", self.explorationRate)
            self.allRewards.append(rewardCurrEpisode)

        option_count = [[0, 0] for i in range(35)]
        for i in self.qTable:
            option_count[i[1]][np.argmax(self.qTable[i])] += 1
        print(option_count)

    def printResults(self):
        gap = 10000
        rewardsForEveryHundred = np.split(np.array(self.allRewards), self.numEpisodes / gap)
        count = gap

        for r in rewardsForEveryHundred:
            print(count, ": ", str(sum(r / gap)))
            count += gap


if __name__ == "__main__":
    solver = solveBlackJacK()
    solver.play()
    solver.printResults()