import numpy as np
import random as randi
import time
import numpy as np

# noinspection PyRedundantParentheses
from DQN import DQN
from blackJackEnv import blackJack


class solveBlackJacK:
    numEpisodes = 5000
    # merges = [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10]]

    # merges = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]
    merges = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]

    def __init__(self):
        self.learningRate = 0.5
        self.startTime = 0
        self.endTime = 0
        self.env = blackJack()
        self.actions = [1, 0]
        self.allRewards = []
        self.agent = DQN(4 + len(self.merges))

    def merge(self, state):
        count = list(state[-11:])
        merged = []
        for grp in self.merges:
            temp = 0
            for i in grp:
                temp += count[i]
            merged.append(temp)
        return np.asarray(tuple(list(state[:-11]) + merged)).reshape([1, 4 + len(merged)])

    #         return tuple(list(state[:-11]))

    def new_actions(self):
        return [0, 0]

    def play(self):
        self.startTime = time.perf_counter()
        for episode in range(self.numEpisodes):
            gameState, isNatural = self.env.reset()
            gameState = self.merge(gameState)
            done = False
            rewardCurrEpisode = 0

            while (not done):
                if (isNatural):
                    action = 0
                else:
                    action = self.agent.policy(gameState)

                new_gameState, reward, done, isNatural = self.env.step(action)
                new_gameState = self.merge(new_gameState)

                self.agent.replay_buffer.store([gameState, action, reward, new_gameState, done])
                self.agent.train(episode)

                gameState = new_gameState
                rewardCurrEpisode += reward
                if (done):
                    break

            if (episode % (self.numEpisodes / 100) == 0):
                print("Episode :", episode, "Reward :", rewardCurrEpisode, " Exp rate :", self.agent.explorationRate)
            self.allRewards.append(rewardCurrEpisode)

        self.endTime = time.perf_counter()

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
