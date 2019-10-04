from common import VALUES, RED, BLACK, INVALID_PLAY, VALID_FINAL_PLAY
from common import VALID_NONFINAL_PLAY

def comp10001bo_match_discard(play_card, discard_pile, player_no, to_player_no,
                              from_hand=True):
    """
    comp10001bo_match_discard takes as input a 2-character string represting 
    the card in play, a list of strings representing the discard pile the card 
    is to be placed on, an integer representing the number of the player
    making the move, another integer representing the number of the player of 
    which the pile belongs to and a bool value indicating whether or not the 
    card is being played from the hand. This function will return an integer 
    value 0 if the play is invalid, 1 if the play is a non-turn-ending play 
    or 2 if the play is a turn-ending play
    """
    
    # Define variables for the value, suit and index value of 'play_card'
    play_value, play_suit = play_card 
    play_index = VALUES.index(play_value)
    
    # Define empty as a boolean value that is true if the discard pile is 
    # empty and False otherwise
    
    if not discard_pile:
        empty = True       
    else:
        empty = False
        # If not empty, define the 'last_card' as the last card in the list, 
        # and define variables for the value, suit and index of said card
        last_card = discard_pile[-1]
        discard_value, discard_suit = last_card
        discard_index = VALUES.index(discard_value) 
    
    # Define 'ace' as a boolean that equates to True if the card is an ace
    if play_value is 'A':
        ace = True 
    else:
        ace = False 
    
    # If there is/are card/s in the discard pile define 'colour' as the colour 
    # of that card 
    if not empty:
        if discard_suit in RED:
            colour = RED
        else:
            colour = BLACK 
        
        # If cards are the same colour, define 'colour_alt' as false and True 
        # if they are different colours 
        if play_suit in colour:  
            colour_alt = False
        else:
            colour_alt = True 
        
        # Define 'adjacent' as True if the cards are next to one another 
        # in VALUES and False if not
        if abs(play_index - discard_index) == 1:
            adjacent = True 
        elif (play_value in ['K', '2'] and discard_value in ['K', '2'] and
              play_value != discard_value):
            adjacent = True   
        else:
            adjacent = False
            
    # If card is an ace, the discard pile is empty and does not belong to the
    # play, the discard pile is empty and belongs to the player but is not 
    # playing from the hand or is illegal and not being played from the hand, 
    # return o
    if (ace or (empty and player_no != to_player_no) or 
       (empty and not from_hand) or (not from_hand and not 
       (adjacent and colour_alt))):
        return 0
    # If the discard pile is not empty and the play is legal, return 1
    elif (not empty) and colour_alt and adjacent:
        return 1
    # Otherwise return 2
    else:
        return 2
      
        
# automatically run each of the examples from the question
if __name__ == "__main__":
    tests = (
        # can start own discard pile with any card from hand (FINAL play)
        (VALID_FINAL_PLAY, '4S', [], 2, 2),

        # can't start the discard pile of another player
        (INVALID_PLAY, '4S', [], 2, 0),

        # can't start a discard stack from the stockpile/build pile
        (INVALID_PLAY, '4S', [], 2, 2, False),

        # can play a black 4 on a red 3 (to own discard pile; NON-FINAL)
        (VALID_NONFINAL_PLAY, '4S', ['3H'], 2, 2),

        # can play a black 4 on a red 3 (to another
        # player's discard pile; NON-FINAL)
        (VALID_NONFINAL_PLAY, '4S', ['3H'], 2, 3),

        # can play a black 4 on a red 3 (from discard/stockpile to
        # own discard pile; NON-FINAL)
        (VALID_NONFINAL_PLAY, '4S', ['3H'], 2, 3, False),

        # can't play an Ace on a discard pile
        (INVALID_PLAY, 'AH', ['KS'], 2, 3),

        # can play a red 2 on a black King (to another
        # player's discard pile; NON-FINAL
        (VALID_NONFINAL_PLAY, '2H', ['KS'], 2, 3),

        # can (illegally) play 2 on Q (from hand to another player's
        # discard pile; FINAL)
        (VALID_FINAL_PLAY, '2H', ['QS'], 2, 3), 

        # can't play 2 on Q (from stockpile/build pile to another player's
        # discard pile; FINAL)
        (INVALID_PLAY, '2H', ['QS'], 2, 3, False), 

        # can (illegally) play red 4 on red 3 (from hand to another player's
        # discard pile; FINAL)
        (VALID_FINAL_PLAY, '4H', ['3H'], 2, 3),

        # can't (illegally) play red 4 on red 3 (from source other
        # than hand to own discard pile; INVALID)
        (INVALID_PLAY, '4H', ['3H'], 2, 2, False),

    )

    for retval, *args in tests:
        if comp10001bo_match_discard(*args) == retval:
            result = "passed"
        else:
            result = "failed"
        print("Testing comp10001bo_match_discard{} ... {}".format(
            repr(tuple(args)), result))