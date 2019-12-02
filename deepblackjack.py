import numpy as np
import random as randi
import time
import numpy as np

# noinspection PyRedundantParentheses
from DQN import DQN
from blackJackEnv import blackJack


class solveBlackJacK:
    numEpisodes = 50000
    merges = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]

    def __init__(self):
        self.learningRate = 0.5
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
            if episode % 50 == 0:
                self.agent.make_equal()
            if (episode % (self.numEpisodes / 100) == 0):
                print("Episode :", episode, "Reward :", rewardCurrEpisode, " Exp rate :", self.agent.explorationRate)
            self.allRewards.append(rewardCurrEpisode)

    def printResults(self):
        array_y = []
        array_x = []
        gap = self.numEpisodes / 250
        rewardsForEveryHundred = np.split(np.array(self.allRewards), self.numEpisodes / gap)
        count = gap
        for r in rewardsForEveryHundred:
            array_y.append(sum(r / gap))
            array_x.append(count)
            print(count, ": ", str(sum(r / gap)))
            count += gap
        cumsum, moving_aves = [0], []
        N = 10
        for i, x in enumerate(array_y, 1):
            cumsum.append(cumsum[i - 1] + x)
            if i >= N:
                moving_ave = (cumsum[i] - cumsum[i - N]) / N
                moving_aves.append(moving_ave)
        moving_aves = np.array(moving_aves)
        array_x = array_x[4:-5]
        array_x = np.array(array_x)
        np.savetxt("WICC_y_DQL_5.txt", array_x, fmt="%s")
        np.savetxt("WICC_x_DQL_5.txt", moving_aves, fmt="%s")


if __name__ == "__main__":
    solver = solveBlackJacK()
    solver.play()
    solver.printResults()
