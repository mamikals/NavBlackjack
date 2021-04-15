import json
import requests

url = "http://nav-deckofcards.herokuapp.com/shuffle"


class Player:

    def __init__(self):
        self.sum = 0
        self.cards = []

    def drawCard(self, shuffle):
        card = shuffle.pop(0)
        self.cards.append(card)
        self.sum += self.getValue(card["value"])

    def getValue(self, value):
        if value in ["K", "Q", "J"]:
            return 10
        if value == "A":
            return 11
        return int(value)

    def formatCards(self):
        text = ""
        for card in self.cards:
            text += card["suit"][0] + str(self.getValue(card["value"])) + ","
        return text[:-1]


def formatResult(winner, player1, player2):
    print("Vinner:", winner, "\n")
    print("Marit |", player2.sum, "|", player2.formatCards())
    print("Truls |", player1.sum, "|", player1.formatCards())


def playGame():
    shuffle = requests.get(url).json()

    truls = Player()
    marit = Player()

    truls.drawCard(shuffle)
    truls.drawCard(shuffle)
    marit.drawCard(shuffle)
    marit.drawCard(shuffle)

    if marit.sum == 21:
        formatResult("Marit", truls, marit)
        return
    if truls.sum == 21:
        formatResult("Truls", truls, marit)
        return

    while truls.sum < 17:
        truls.drawCard(shuffle)
    if truls.sum > 21:
        formatResult("Marit", truls, marit)
        return

    while marit.sum < truls.sum and marit.sum <= 21:
        marit.drawCard(shuffle)
    if marit.sum > 21:
        formatResult("Truls", truls, marit)
        return
    formatResult("Marit", truls, marit)


userInput = input("Want to watch a game of blackjack (Y/N)")

while userInput.capitalize() == "Y":
    playGame()
    userInput = input("Want to watch a game of blackjack (Y/N)")
