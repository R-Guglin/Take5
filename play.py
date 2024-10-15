from getpass import getpass

def display_card(card, num):
    cow = "\U0001F42E"  #Unicode 'cow face'
    return str(card) + "(" + cow + "x"+str(num)+")"

def take(rows, row, choice, scores):
    #adds to a player's collection
    ind = rows.index(row)
    for card in row:
        scores[choices[choice]].append(card)
    rows[ind] = [choice]
    return rows

def pick_row(card, rows):
    minimum_dif = 104
    pick = []
    if card < min(rows[0][-1], rows[1][-1], rows[2][-1], rows[3][-1]):
        return False
    for row in rows:
        dif = card - row[-1]
        if dif >0 and dif < minimum_dif:
            minimum_dif = dif
            pick = row
    return pick

#visualizing the face-up cards on the table
def show_face_up(rows, cards):
    for row in rows:
        out = ""
        for card in row:
            out += display_card(card, cards[card]) + "   "
        print(out)

choices = {}

#play 1 game (i.e. 1 round in the overall game, updating score table afterwards)
def play(player_hands, cards, scores, rows):
    show_face_up(rows, cards)
    #players pick cards
    final_round = False
    for player in player_hands:
        hand = player_hands[player]
        if len(player_hands[player]) == 1:
            final_round = True
        if final_round:
            last_card = hand[0]
            choices[last_card] = player
            hand.pop(0)
            return True
        check = input(player+ ", please enter your first initial: ")
        if check != player[0]:
            check = input(player+ ", please enter your first initial: ")
        out = ""
        for card in sorted(hand):
            out += display_card(card, cards[card]) + "   "
        print(out)
        choice = int(getpass("Pick a card! "))  #hides choice
        while choice not in player_hands[player]:
            print("Invalid choice")
            choice = int(getpass("Pick a card! "))
        choices[choice] = player
        #print(player + " chose "+str(choice))
        #remove card from hand
        hand.pop(hand.index(choice))
        #print("\nRemoved "+str(choice)+" from "+player+"'s hand\nNew hand has length "+str(len(hand)))
    #handle choices
    print()
    for player in player_hands:
        choice = [k for k, v in choices.items() if v == player]
        print(player + " chose "+str(choice[0]))
    print()
    for choice in sorted(choices.keys()):
        #print("\nHandling choice "+str(choice))
        chosen_row = pick_row(choice, rows)
        if chosen_row:
            if len(chosen_row) < 5:
                #player is NOT placing 6th card
                #print("Accepted card "+str(choice)+" to row "+str(rows.index(chosen_row)+1))
                chosen_row.append(choice)
            else:
                #player IS placing 6th card
                rows = take(rows, chosen_row, choice, scores)
                #print(rows[ind])
        else:
            #card doesn't fit in any row
            row = input(choices[choice] + ", pick a row to replace (1, 2, 3, or 4): ")
            take(rows, rows[int(row)-1], choice, scores)
        choices.pop(choice)
    #for player in scores:
    #    print(player + ": "+ scores[player])
