import random
from play import *

Cards = {}   # a dictionary of cards and penalties
Scores = {}  # a dictionary tracking each person's score
Player_Hands = {}  # a dict of names, each associated with an initially empty list (hand)
round = True #loop to allow the game to start a new round
game = True #loop to keep the game running
limit = 66

def deal(players, cards, keys):
    i = 0 #number of cards given out
    j = 0 #number of players seen to
    for player in players:
        hand = players[player]  #current player's hand
        while i < (j+1)*10:
            hand.append(keys[i])
            #ex: keys[11] = 54; hand[54] = 1
            i += 1
        j += 1
    return keys[i:]

def sum_of_collection(collection):
    total = 0
    for elem in collection:
        total += Cards[elem]
    return total

#Populate Cards with their respective penalties
for i in range(1,105):
    if i != 55:
        if i%11 == 0:
            Cards[i] = 5
        elif i%10 == 0:
            Cards[i] = 3
        elif i%5 == 0 and i%10 != 0:
            Cards[i] = 2
        else:
            Cards[i] = 1
    elif i == 55:
        Cards[i] = 7

#take number of players and their names; populate score and hand trackers
players = int(input("How many players? (2-10) "))
while players < 2 or players > 10:
    print("Bad number of players")
    players = int(input("How many players? (2-10) "))
breakoff = players*10 + 4
for i in range(players):
    name = input("Player "+str(i+1)+", enter your name: ")
    Scores[name] = []
    Player_Hands[name] = []

limit = int(input("Point limit? (Default is 66) "))

lost = None

#main loop: controls gameplay
while game:
    #shuffle cards — we use a list called Deck; the dict "Cards" is just a reference
    Deck = list(Cards.keys())
    random.shuffle(Deck)
    for card in Deck[breakoff:]:
        Deck.pop(Deck.index(card))

    #dealing cards— this gives each player 10 cards from the shuffled deck
    #and returns the last 4 cards
    starts = deal(Player_Hands, Cards, Deck)
    Rows = [[starts[0]],
            [starts[1]],
            [starts[2]],
            [starts[3]]]

    playing = True
    while playing:
        play(Player_Hands, Cards, Scores, Rows)
        for player in Player_Hands:
            if len(Player_Hands[player]) == 0:
                playing = False 
                for player in Scores:
                    collected = Scores[player]
                    print(player + "'s collection: ")
                    for card in collected:
                        print("    " + display_card(card, Cards[card]))
                    print("(" + str(sum_of_collection(collected)) + " points total)\n")
                    if sum_of_collection(Scores[player]) >= limit:
                        lost = player + " lost with score "+str(sum_of_collection(collected))
                        game = False
        

    if lost != None: #somebody has lost the game (i.e. exceeded point lim)
        if input("Play again? (Y/N) " == 'Y'):
            game = True

#List iteration rules
#list[x:y] includes list[x] and list[y-1]
#list[x:] includes all from list[x] to end
#list[:x] includes all from list[0] to list[x-1]
