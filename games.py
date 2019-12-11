import random

# define class for blackjack
class Blackjack:
    def __init__(self):
        # initialize variables
        self.deck = [1, 2, 3, 4, 5,
            6, 7, 8, 9, 10,
            11, 12, 13] * 4 # four of each card
        # shuffle deck
        random.shuffle(self.deck)
    
    def deal_cards(self):
        hand = []
        for i in range(0, 2): # start with 2 cards
            card = self.deck.pop()
            
            if card == 1:
                card = "Ace"
            if card == 11 or card == 12 or card == 13:
                card = 10

            hand.append(card)
        return(hand)

    def get_total(self, hand):
        total = 0
        # aggregate total
        for card in hand:
            if card == "Ace" and total >= 11:
                total += 1
            elif card == "Ace":
                total += 11
            else:
                total += card
        return total
    
    def hit_or_stand(self, message):
        # tally dictionary
        votes = {react.emoji: react.count for react in message.reactions}
        
        # compare votes
        if votes.get("✅") > votes.get("❌"):
            return 1
        else:
            return 0
       
    def hit(self, hand):
        # take another card
        card = self.deck.pop()
        
        if card == 1:
            card = "Ace"
        if card == 11 or card == 12 or card == 13:
            card = 10

        hand.append(card)
        
        return hand
    
        
    def get_result(self, player_hand, enemy_hand):
        # end conditions
        status = ""
        if self.get_total(player_hand) > 21:
            status += "\nYou went over 21. You lost.\n"
        elif self.get_total(enemy_hand) > 21:
            status += "\nThe dealer went over 21. You won!\n"
        elif self.get_total(player_hand) > self.get_total(enemy_hand):
            status += "\nYou're over the dealer. You won!\n"
        elif self.get_total(player_hand) < self.get_total(enemy_hand):
            status += "\nYou're under the dealer. You lost.\n"
        elif self.get_total(enemy_hand) == 21:
            status += "\nThe dealer got a blackjack. You lost.\n"
        elif self.get_total(player_hand) == 21:
            status += "\nBlackjack! You won!\n"
        else:
            status += "\nIt's a tie.\n"
            
        return status
