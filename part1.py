from common import VALUES, RED, BLACK

def comp10001bo_match_build(play_card, build_pile):
    """
    comp10001bo_match_build takes as input, a string representation of the card
    in question and a list of strings each representing a card within a pile
    in order from the bottom to the top of the pile. This function will return 
    True if the play_card and top card in build_pile prove a valid match and
    False if not. 
    """
    
    # Define my_suit and my_value as value and suit of the card
    my_value, my_suit = play_card
    
    # If the pile is empty and play_card is not a king or 2 return False 
    if not build_pile:
        if my_value is '2' or my_value is 'K':
            return True
        else:
            return False
    
    # Define the value and suit of the top build card accordingly 
    build_card = build_pile[-1]
    build_value = build_card[0]
    build_suit = build_card[1]
    
    # Assign index values to each card according to it's position in VALUES 
    card_index = VALUES.index(my_value)
    build_index = VALUES.index(build_value)

    # If card is an ace, return True 
    if my_value is 'A':
        ace = True 
    else:
        ace = False 
    
    # Test if the cards are the same colour, if so 'colour_match' is True
    if build_suit in RED:
        colour = RED
    else:
        colour = BLACK 
        
    if my_suit in colour:
        
        colour_match = True
    else:
        colour_match = False 
    
    # Test if the cards are next to eachother in VALUES, if so 'adjacent'
    # is True
    if abs(card_index - build_index) == 1:
        adjacent = True 
    else:
        adjacent = False
        
    # Finally, if cards are of the same colour and in order return True, 
    # otherwise return False 
    if colour_match and (adjacent or ace):
        return True
    else:
        return False 
