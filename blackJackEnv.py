import numpy as np


# obs = [ace, sum1, othersum, cards_left, rounds]

# noinspection PyRedundantParentheses
class blackJack():
    numDeck = 1

    def __init__(self):
        self.count = [0 for i in range(11)]
        self.deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        self.sum1 = 0
        self.ace = False
        self.otherSum = 0
        self.round = 1

    def reset(self):
        for i in self.deck:
            self.count[i] = 4 * blackJack.numDeck
        self.count[10] = 4 * 4 * blackJack.numDeck
        self.sum1 = 0
        self.ace = False
        self.otherSum = 0
        self.round = 1

    def new_card(self):
        if(self.count[0] < 0):
            pass
            # print(self.count, self.round, self.sum1)
        c = np.random.randint(0, sum(self.count))
        card = 1
        sum1 = 0

        while (sum1 <= c):
            sum1 += self.count[card]
            card += 1
        card -= 1

        if(card <= 0):
            print(card,  c, self.count)
        self.count[card] -= 1
        return card

    #ensure count is returned last
    def return_state(self):
        # return tuple([self.ace, self.sum1, self.otherSum, self.round])
        return tuple([self.ace, self.sum1, self.otherSum, self.round] + self.count)

    def new_hand(self):
        r = 0
        self.round -= 1
        while (self.round):
            self.otherSum = self.new_card()

            c1 = self.new_card()
            self.ace = False
            if (c1 == 1):
                self.ace = True
                c1 = 11
            c2 = self.new_card()
            if (c2 == 1):
                self.ace = True
                c2 = 11
            self.sum1 = c1 + c2
            if (self.sum1 > 21):
                self.sum1 -= 10
            if (self.sum1 != 21):
                return r

            o2 = self.new_card()
            if (o2 == 1):
                o2 = 11
            if (o2 + self.otherSum != 21):
                r += 1.5
            self.round -= 1
        return r

    # action 0 is stay
    # action 1 is hit
    def step(self, action):
        if (action == 1):
            c = self.new_card()
            if (c == 1):
                self.ace = True
                c = 11
            self.sum1 += c

            if (self.sum1 > 21 and self.ace):
                self.sum1 -= 10
                self.ace = False
            if (self.sum1 > 21):
                r = self.new_hand()
                return self.return_state(), r - 1, self.round == 0
            return self.return_state(), 0, False

        else:
            oace = (self.otherSum == 1)
            while (self.otherSum < 17):
                c = self.new_card()

                if (c == 1 and not oace):
                    c = 11
                    oace = True

                self.otherSum += c
                if (self.otherSum > 21 and oace):
                    oace = False
                    self.otherSum -= 10
            r = 0
            if (self.otherSum < self.sum1):
                r += 1
            elif (self.otherSum > self.sum1):
                r -= 1
            r += self.new_hand()
            return self.return_state(), r, self.round == 0
