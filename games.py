import random
        
def deal_cards(deck):
    # initialize variables
    hand = []
    card = 0
    
    for i in range(0, 2): # start with 2 cards
        card = deck.pop()
        
        if card == 1:
            card = "Ace"
        if card == 11 or card == 12 or card == 13:
            card = 10

        hand.append(card)
        
    return hand

def get_total(hand):
    total = 0
    
    for card in hand:
        if card == "Ace" and total >= 11:
            total += 1
        elif card == "Ace":
            total += 11
        else:
            total += card
            
    return total

def hit(hand, deck):
    card = deck.pop()
    
    if card == 1:
        card = "Ace"
    if card == 11 or card == 12 or card == 13:
        card = 10

    hand.append(card)
    
    return hand
    
def get_result(player_hand, enemy_hand, status):
    if get_total(player_hand) == 21:
        status += "\nBlackjack! You won!\n"
    elif get_total(player_hand) > 21:
        status += "\nYou went over 21. You lost.\n"
    elif get_total(player_hand) > get_total(enemy_hand):
        status += "\nYou're over the dealer. You won!\n"
    elif get_total(player_hand) < get_total(enemy_hand):
        status += "\nYou're under the dealer. You lost.\n"
    elif get_total(enemy_hand) == 21:
        status += "\nThe dealer got a blackjack. You lost.\n"
    elif get_total(enemy_hand) > 21:
        status += "\nThe dealer went over 21. You won!\n"
    else:
        status += "\nIt's a tie.\n"
        
    return status
