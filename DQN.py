class Replay_buffer():
    def __init__(size = 100000):
        self.memory = []
        self.position = 0
        self.size = size
    def store(self, s):
        if(len(self.memory) < self.size):
            self.memory.append(s)
            return
        self.memory[self.position] = s
        self.postion = (self.position + 1)%self.size
    def sample(self, batch_size = 1):
        return random.sample(self.memory, batch_size)
    
class DQN():
    
    def __init__(self, observation_space):

        self.replay_buffer = Replay_buffer()
        self.explorationRate = 0.5
        self.model = Sequential([Dense(24, input_shape=(observation_space,)),
                                 activation("relu"),
                                Dense(24),
                                activation("relu"),
                                Dense(2)] 
                               )
        self.model.compile(loss="mse", optimizer=Adam(lr=LEARNING_RATE))
    def decay_epsilon(self):
        self.explorationRate = self.minExplorationRate + (self.explorationRate - self.minExplorationRate) * (np.exp(-self.decay))
    def policy(state):
        x = random.random()
        if(x < self.explorationRate):
            return random.randint(2)
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])
    def train(self):
        batch = self.replay_buffer.sample(BATCH_SIZE)
        for state, action, reward, state_next, terminal in batch:
            q_update = reward
            if not terminal:
                q_update += GAMMA * np.amax(self.model.predict(state_next)[0])
            q_values = self.model.predict(state)
            print(q_values)
            q_values[0][action] = q_update
            self.model.fit(state, q_values)
        self.decay_epsilon()
    