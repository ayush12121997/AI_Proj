import numpy as np


# obs = [ace, sum1, otherSum, rounds, cardsLeft]
# noinspection PyRedundantParentheses

class blackJack():
    numDeck = 10

    def __init__(self):
        self.cardCount = [0 for i in range(11)]
        self.deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        self.playerSum = 0
        self.canUseAce = False
        self.dealerSum = 0
        self.numRounds = 1

    def reset(self):
        for i in self.deck:
            self.cardCount[i] = 4 * blackJack.numDeck
        self.cardCount[10] = 4 * 4 * blackJack.numDeck
        self.numRounds = 10
        self.new_hand()
        self.numRounds = 1

    def new_card(self):
        c = np.random.randint(0, sum(self.cardCount))
        card = 1
        sum2 = 0

        while (sum2 <= c):
            sum2 += self.cardCount[card]
            card += 1
        card -= 1

        if (card <= 0):
            print("Error : Invalid card value in new_card ", card, c, self.cardCount)
        self.cardCount[card] -= 1
        return card

    # ensure count is returned last
    def return_state(self):
        return tuple([self.canUseAce, self.playerSum, self.dealerSum, self.numRounds] + self.cardCount)

    def new_hand(self):
        r = 0
        self.numRounds -= 1
        if (self.numRounds < 0):
            print("Error : Invalid numRounds in new_hand ", self.return_state())
        while (self.numRounds > 0):
            self.dealerSum = self.new_card()
            dealerOtherCard = self.new_card()

            playerC1 = self.new_card()
            self.canUseAce = False
            if (playerC1 == 1):
                self.canUseAce = True
                playerC1 = 11
            playerC2 = self.new_card()
            if (playerC2 == 1):
                self.canUseAce = True
                playerC2 = 11

            self.playerSum = playerC1 + playerC2
            if (self.playerSum > 21):
                self.playerSum -= 10
                if(playerC1 == 11 and playerC2 == 11):
                    self.canUseAce = True
                else:
                    self.canUseAce = False
            if (self.playerSum != 21):
                return r

            if (dealerOtherCard == 1):
                dealerOtherCard = 11
            if (dealerOtherCard + self.dealerSum != 21):
                r += 1.5
            self.numRounds -= 1
        return r

    # action 0 is stay
    # action 1 is hit
    def step(self, action):
        if (action == 1):
            card = self.new_card()
            if (card == 1):
                self.canUseAce = True
                card = 11
            self.playerSum += card

            if (self.playerSum > 21 and self.canUseAce):
                self.playerSum -= 10
                self.canUseAce = False
            if (self.playerSum > 21):
                r = self.new_hand()
                return self.return_state(), r - 1, self.numRounds == 0
            return self.return_state(), 0, False

        else:
            if (self.dealerSum == 1):
                otherAce = True
            else:
                otherAce = False
            while (self.dealerSum < 17):
                card = self.new_card()

                if (card == 1 and not otherAce):
                    card = 11
                    otherAce = True
                self.dealerSum += card
                if (self.dealerSum > 21 and otherAce):
                    otherAce = False
                    self.dealerSum -= 10
            r = 0
            if (self.dealerSum < self.playerSum):
                r += 1
            elif (self.dealerSum > self.playerSum):
                r -= 1
            r += self.new_hand()
            return self.return_state(), r, self.numRounds == 0
