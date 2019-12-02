import random
import numpy as np
from keras import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import Adam


class Replay_buffer():
    def __init__(self, size=100000):
        self.memory = []
        self.position = 0
        self.size = size

    def store(self, s):
        if (len(self.memory) < self.size):
            self.memory.append(s)
            return
        self.memory[self.position] = s
        self.position = (self.position + 1) % self.size

    def sample(self, batch_size=1):
        if (len(self.memory) < batch_size):
            return []
        return random.sample(self.memory, batch_size)


class DQN():
    GAMMA = 0.9
    LEARNING_RATE = 0.5
    BATCH_SIZE = 15
    NUM_EPISODES = 50000

    def __init__(self, observation_space):

        self.replay_buffer = Replay_buffer()
        self.explorationRate = 0.5
        self.decay = 0.0002
        self.minExplorationRate = 0.0001
        self.observation_space = observation_space
        self.model = Sequential([Dense(15, input_shape=(observation_space,)),
                                 Activation("relu"),
                                 Dense(6),
                                 Activation("relu"),
                                 Dense(2)]
                                )
        self.model.compile(loss="mse", optimizer=Adam(lr=DQN.LEARNING_RATE))
        self.critic = Sequential([Dense(15, input_shape=(observation_space,)),
                                 Activation("relu"),
                                 Dense(6),
                                 Activation("relu"),
                                 Dense(2)]
                                )
        self.critic.compile(loss="mse", optimizer=Adam(lr=DQN.LEARNING_RATE))

    def decay_epsilon(self, episodes):
        if (episodes < 0.6 * DQN.NUM_EPISODES):
            self.decay = 1 / (2 * DQN.NUM_EPISODES)
        else:
            self.decay = 10 / DQN.NUM_EPISODES
        self.explorationRate = self.minExplorationRate + (self.explorationRate - self.minExplorationRate) * (np.exp(-self.decay))

    def policy(self, state):
        x = random.random()
        if (x < self.explorationRate):
            return random.randint(0, 1)
        # state2 = np.asarray(state)
        # state2 = state2.reshape([1, self.observation_space])
        # print(state.shape)
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])

    def train(self, num_ep):
        batch = self.replay_buffer.sample(DQN.BATCH_SIZE)
        for state, action, reward, state_next, terminal in batch:
            q_update = reward
            if not terminal:
                q_update += DQN.GAMMA * np.amax(self.critic.predict(state_next)[0])
            q_values = self.model.predict(state)
            # print(q_values)
            q_values[0][action] = q_update
            self.model.fit(state, q_values, verbose=0)
        self.decay_epsilon(num_ep)
    def make_equal(self):
        self.critic.set_weights(self.model.get_weights())