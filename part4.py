from common import *
# TEST FROM STOCK PILE


def play_from_stockpile(my_stock_pile_card, desired_outcome, player_no, hand, 
                        stockpiles, discard_piles, build_piles):
    """
    play_from_stockpile takes a 2 character string representing the card on top
    of the stockpile, a digit representing the desired play type and all the 
    elements within the main function comp10001bo_play call that define the 
    game state. This function returns a 3-tuple 'play' representing a valid 
    play that has been made using the top card from the stockpile 
    (validated by comp10001bp_is_valid_play) and has returned 'desired_outcome' 
    """
   
    # Test for a valid move that takes card and places it on a build pile. 
    # If not valid 'play' equals the tuple that stipulates no possible/
    # invalid play ((3, None, (None, None)))
    for y in range(4):
        play = (2, my_stock_pile_card, (0, y))
        val = comp10001bo_is_valid_play(play, player_no, hand, stockpiles,
                                        discard_piles, build_piles)
        # If above returns desired_outcome then return that play 
        if val in desired_outcome:
            return play
        else:
            play = (3, None, (None, None))
    
    # Test for a valid move that takes the card and places it on a discard pile    
    for a in range(4):
        for b in range(4):
            play = (2, my_stock_pile_card, (1, (a, b)))
            val = comp10001bo_is_valid_play(play, player_no, hand, stockpiles,
                                            discard_piles, build_piles)
            if val in desired_outcome:
                return play 
            else:
                play = (3, None, (None, None))
                
    # If no valid plays return 'invalid' 'play'            
    return play 


def play_from_hand(desired_outcome, player_no, hand, 
                   stockpiles, discard_piles, build_piles, play_to):
    """
    play_from_hand takes a digit representing the desired play type and all the 
    elements within the main function comp10001bo_play call that define the 
    game state and 'play_to', a list used to determine what destination to 
    test when this function is called. This function returns a 3-tuple 'play' 
    represting a valid play that has used a card from 'hand' 
    (validated by comp10001bp_is_valid_play) and has returned 'desired_outcome' 
    """
     
    for card in hand: 
        if 'bp' in play_to:
            # Test for valid play using each card in hand and playing to
            # any build pile
            for y in range(4):
                play = (0, card, (0, y))
                val = comp10001bo_is_valid_play(play, player_no, hand, 
                                                stockpiles, discard_piles, 
                                                build_piles)
            
                if val in desired_outcome:
                    return play 
                else: 
                    play = (3, None, (None, None))
                    
        if 'dp' in play_to:
            # Test for valid play using each card in hand and playing to any 
            # discard pile
            for a in range(4):
                for b in range(4):
                    play = (0, card, (1, (a, b)))
                    val = comp10001bo_is_valid_play(play, player_no, hand, 
                                                    stockpiles, discard_piles,
                                                    build_piles)
                    if val in desired_outcome:
                        return play 
                    else:
                        play = (3, None, (None, None))
    return play 
                     
    
def play_from_discard_pile(desired_outcome, player_no, hand, 
                           stockpiles, discard_piles, build_piles):
    """
    play_from_discard_pile takes a list of integers representing the desired
    play type and all the elements within the main function comp10001bo_play
    call that define the game state. This function returns a 3-tuple 'play' 
    represting a valid play that has used a card from the top of a discard pile
    (validated by comp10001bp_is_valid_play) and has returned 'desired_outcome' 
    """
    
    # Test for valid play from any discard pile to any build pile
    j = 0 
    for player in discard_piles:
        i = 0 
        for pile in player:
            if pile:
                card = pile[-1]
                
                for y in range(4):
                    play = (1, (card, (j, i)), (0, y))
                    val = comp10001bo_is_valid_play(play, player_no, hand, 
                                                    stockpiles, discard_piles,
                                                    build_piles)
                    if val in desired_outcome:
                        return play
                        
                    else:
                        play = (3, None, (None, None))
                      
                # Test for valid play from any discard pile to any other 
                # discard pile
                for a in range(4):
                    for b in range(4):
                        play = (1, (card, (j, i)), (1, (a, b)))
                        val =  comp10001bo_is_valid_play(play, player_no,
                                                         hand, stockpiles,
                                                         discard_piles,
                                                         build_piles)
                        if val in desired_outcome:
                            return play 
                        else: 
                            play = (3, None, (None, None))
          
            else:
                play = (3, None, (None, None))  
                
            i += 1        
        j += 1
        
    return play          


def comp10001bo_play(player_no, hand, stockpiles, discard_piles, build_piles,
                     play_history):
    """
    comp10001bo_play takes as input an integer representing the assigned player
    number, a list of cards held by the player, a 4-tuple 'stockpiles' 
    representing the stockpiles of every player, a 4-tuple 'discard_piles' of 
    lists representing the contents of each player's discard pile, a 4-tuple
    'build_piles' of lists descriving the content of each of the build piles 
    and a 2-tuple 'play_history' specifying the sequence of plays to the 
    current point in the game. This function returns a 3-tuple that stipulates
    the desired play given the input. 
    """
    
    
    # Pre-define any variables used within function calls  
    MY_STOCK_PILE_CARD = stockpiles[player_no][0]
    EMPTY_DISCARDS = (([], [], [], []), ([], [], [], []), ([], [], [], []),
                      ([], [], [], []))
    NO_PLAY = (3, None, (None, None))
    
    
    # First, test for any valid plays from the stockpile
    if play_from_stockpile(MY_STOCK_PILE_CARD, [1, 2], player_no, hand, 
                           stockpiles, discard_piles, build_piles) != NO_PLAY:
        return play_from_stockpile(MY_STOCK_PILE_CARD, [1, 2], player_no, hand,  
                                   stockpiles, discard_piles, build_piles)
    
    # Secondly, if cards in hand, test for any valid move using a card that 
    # could potentially help place a stockpile card next play
    if hand:
        for card in hand:
            if comp10001bo_match_build(card, [MY_STOCK_PILE_CARD]):
                if play_from_hand([1], player_no, [card], 
                                  stockpiles, discard_piles, build_piles,
                                  ['bp']) != NO_PLAY:
                    return play_from_hand([1], player_no, [card], 
                                          stockpiles, discard_piles,
                                          build_piles, ['bp']) 
           
    if hand:
        for card in hand:              
            if comp10001bo_match_discard(card, [MY_STOCK_PILE_CARD], 0,
                                         0, from_hand=True) == 1:
                if play_from_hand([1], player_no, [card], 
                                  stockpiles, discard_piles, build_piles,
                                  ['dp']) != NO_PLAY: 
                    return play_from_hand([1], player_no, [card], 
                                          stockpiles, discard_piles,
                                          build_piles, ['dp'])
    
    # Thirdly, test for a valid non-turn-ending move from a hand to either
    # a build pile or discard pile 
    if hand:
        if play_from_hand([1], player_no, hand, 
                          stockpiles, discard_piles, build_piles, 
                          ['bp', 'dp']) != NO_PLAY:
            return play_from_hand([1], player_no, hand, 
                                  stockpiles, discard_piles,
                                  build_piles, ['bp', 'dp'])
    
    # if cards in hand, test for any valid move using a card that 
    # could potentially help place a stockpile card next turn
    if hand:
        for card in hand:
        
            if comp10001bo_match_build(card, [MY_STOCK_PILE_CARD]):
                if play_from_hand([2], player_no, [card], 
                                  stockpiles, discard_piles, build_piles,
                                  ['bp']) != NO_PLAY:
                    return play_from_hand([2], player_no, [card], 
                                          stockpiles, discard_piles,
                                          build_piles, ['bp']) 
           
        
    if hand:
        for card in hand:
            
            if comp10001bo_match_discard(card, [MY_STOCK_PILE_CARD], 0,
                                         0, from_hand=True) == 2:
                if play_from_hand([2], player_no, [card], 
                                  stockpiles, discard_piles, build_piles,
                                  ['dp']) != NO_PLAY: 
                    return play_from_hand([2], player_no, [card], 
                                          stockpiles, discard_piles,
                                          build_piles, ['dp'])
    
    # Next test for a valid non-turn-ending move from a discard pile to another
    # discard pile 
    if play_from_discard_pile([1], player_no, hand, 
                              stockpiles, discard_piles,
                              build_piles)!= NO_PLAY:
        return play_from_discard_pile([1], player_no, hand, 
                                      stockpiles, discard_piles, build_piles)
    
    # Test for other valid turn-ending moves 
    # From hand
    if hand:   
        if play_from_hand([2], player_no, hand, 
                          stockpiles, discard_piles, build_piles, 
                          ['bp', 'dp']) != NO_PLAY:
            return play_from_hand([2], player_no, hand, 
                                  stockpiles, discard_piles, build_piles,
                                  ['bp', 'dp'])
        
    # Then from discard pile 
    if play_from_discard_pile([2], player_no, hand, 
                              stockpiles, discard_piles,
                              build_piles) != NO_PLAY:
        return play_from_discard_pile([2], player_no, hand, 
                                      stockpiles, discard_piles, build_piles)
    
    
    

    # Lastly, if all options have been exhausted and there are no valid plays, 
    # return 'no_play'
    return NO_PLAY
        
    
# automatically run each of the examples from the question
if __name__ == "__main__":
    tests = (
        # no possible play
        ((3, None, (None, None)), 0, [], (('7H', 7), ('3C', 8), ('3H', 8), ('KD', 8)), ((['7H'], [], [], []), ([], [], [], []), ([], [], [], []), ([], [], [], [])), (['2C'], [], [], []), [(0, (2, '2C', (0, 0)))]),

        # play from stockpile to build pile
        ((2, '3C', (0, 0)), 1, [], (('7H', 7), ('3C', 8), ('3H', 8), ('KD', 8)), ((['7H'], [], [], []), ([], [], [], []), ([], [], [], []), ([], [], [], [])), (['2C'], [], [], []), [(0, (2, '2C', (0, 0))), (0, (3, None, (None, None))), (1, (2, '3C', (0, 0)))]),

        # play from stockpile to build pile
        ((2, '4S', (0, 0)), 1, [], (('7H', 7), ('4S', 7), ('3H', 8), ('KD', 8)), ((['7H'], [], [], []), ([], [], [], []), ([], [], [], []), ([], [], [], [])), (['2C', '3C'], [], [], []), [(0, (2, '2C', (0, 0))), (0, (3, None, (None, None))), (1, (2, '3C', (0, 0)))]),

        # play from stockpile to build pile, with example play
        ((2, '3S', (0, 0)), 1, [], (('7H', 7), ('3S', 6), ('3H', 8), ('KD', 8)), ((['7H'], [], [], []), ([], [], [], []), ([], [], [], []), ([], [], [], [])), (['2C', '3C', '4S'], [], [], []), [(0, (2, '2C', (0, 0))), (0, (3, None, (None, None))), (1, (2, '3C', (0, 0))), (1, (2, '4S', (0, 0)))]),

        # no valid play possible
        ((3, None, (None, None)), 1, [], (('7H', 7), ('0D', 5), ('3H', 8), ('KD', 8)), ((['7H'], [], [], []), ([], [], [], []), ([], [], [], []), ([], [], [], [])), (['2C', '3C', '4S'], [], [], []), [(0, (2, '2C', (0, 0))), (0, (3, None, (None, None))), (1, (2, '3C', (0, 0))), (1, (2, '4S', (0, 0))), (1, (2, '3S', (0, 0)))])
    )

    for retval, *args in tests:
        if comp10001bo_play(*args) == retval:
            result = "passed"
        else:
            result = "failed"
        print("Testing comp10001bo_play{} ... {}".format(
            repr(tuple(args)), result))