import numpy as np


# obs = [ace, sum1, otherSum, rounds, cardsLeft]
# noinspection PyRedundantParentheses

class blackJack():
    numDeck = 5
    rounds = 1
    deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    def __init__(self):
        self.forPlayerCardCount = [0 for i in range(11)]
        self.cardCount = [0 for i in range(11)]
        self.playerSum = 0
        self.dealerSum = 0
        self.canUseAce = False
        self.numRounds = self.rounds
        self.playerHand = []
        self.dealerHand = []
        self.isNatural = False

    def reset(self):
        for i in self.deck:
            self.cardCount[i] = 4 * blackJack.numDeck
            self.forPlayerCardCount[i] = 4 * blackJack.numDeck
        self.cardCount[10] = 4 * 4 * blackJack.numDeck
        self.forPlayerCardCount[10] = 4 * 4 * blackJack.numDeck
        self.numRounds = self.rounds
        self.new_hand()
        return self.return_state(), self.isNatural

    def new_hand(self):
        self.canUseAce = False
        self.forPlayerCardCount = self.cardCount.copy()
        self.numRounds -= 1
        self.isNatural = False
        self.playerHand = [self.new_card(1), self.new_card(1)]
        self.dealerHand = [self.new_card(1), self.new_card(0)]
        self.playerSum = self.find_sum(self.playerHand)
        if(self.canUseAce):
            self.dealerSum = self.find_sum(self.dealerHand)
            self.canUseAce = True
        else:
            self.dealerSum = self.find_sum(self.dealerHand)
            self.canUseAce = False
        if(sorted(self.playerHand) == [1, 10]):
            # print("Got natural in new hand")
            self.isNatural = True

    # ensure count is returned last
    def return_state(self):
        return tuple([self.canUseAce, self.playerSum, self.dealerHand[0], self.numRounds] + self.cardCount)

    def new_card(self, a):
        if(sum(self.cardCount) <= 20 ):
            print(self.cardCount, self.numRounds)
        c = np.random.randint(0, sum(self.cardCount))
        card = 1
        sum2 = 0

        while (sum2 <= c):
            sum2 += self.cardCount[card]
            card += 1
        card -= 1

        if (card <= 0):
            print("Error : Invalid card value in new_card ", card, c, self.cardCount)
        if (a == 1):
            self.forPlayerCardCount[card] -= 1
        self.cardCount[card] -= 1
        return card

    def find_sum(self, hand):
        if (self.can_use_ace(hand)):
            return sum(hand) + 10
        return sum(hand)

    def can_use_ace(self, hand):
        if (1 in hand and sum(hand) + 10 <= 21):
            self.canUseAce = True
            return True
        else:
            self.canUseAce = False
            return False

    # action 1 is hit and 0 is stay
    def step(self, action):
        if (action == 1):
            self.playerHand.append(self.new_card(1))
            # print("Self hand in hit", self.playerHand)
            self.playerSum = self.find_sum(self.playerHand)
            if (self.playerSum > 21):
                self.new_hand()
                # print("Self new hand in hit", self.playerHand)
                return self.return_state(), -1, self.numRounds == -1, self.isNatural
            else:
                return self.return_state(), 0, False, self.isNatural
        else:
            # print("Self hand", self.playerHand)
            self.playerSum = self.find_sum(self.playerHand)
            while (sum(self.dealerHand) < 17):
                self.dealerHand.append(self.new_card(0))
                if (self.canUseAce):
                    self.dealerSum = self.find_sum(self.dealerHand)
                    self.canUseAce = True
                else:
                    self.dealerSum = self.find_sum(self.dealerHand)
                    self.canUseAce = False
            r = 0
            if (21 >= self.dealerSum > self.playerSum):
                r = -1
            elif (self.dealerSum == self.playerSum):
                r = 0
            elif (sorted(self.playerHand) == [1, 10] and self.dealerSum < self.playerSum):
                r = 1.5
            else:
                r = 1
            self.new_hand()
            # print("Self new hand", self.playerHand)
            return self.return_state(), r, self.numRounds == -1, self.isNatural