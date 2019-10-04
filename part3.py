from reference import comp10001bo_match_build, comp10001bo_match_discard

from common import INVALID_PLAY, VALID_FINAL_PLAY, NO_PLAY
from common import VALID_NONFINAL_PLAY

def comp10001bo_is_valid_play(play, player_no, hand, stockpiles, discard_piles,
                              build_piles):
    """
    comp10001bo_is_valid_play takes: a 3 tuple 'play' specifying the type, 
    source and destination of the play; an integer determing the number of 
    the player attempting the play; 'hand', a list of the cards held by the 
    current player; a 4 tuple 'stockpiles, describng the content of the 
    stockpiles for each of the four players; a 4 tuple 'discard_piles', 
    describing the content of each of the for piles of each of the four
    players; a 4-tuple 'build_piles' containing lists of cards describing the 
    contents of each pile. This function returns 0 if the play is invalid, 1 
    if the play is a non-turn-ending move, 2 if the play is a valid turn-ending 
    move and 3 if there is no possible play. 
    """
    
    # DETERMINING PLAYING CARD
    play_type, source, destination = play
    
    # If cards in hand, yet thinks there no possible play, return invalid play 
    if play_type == 3 and hand:
        return 0 
    # If source is None, return no possible play 
    elif source is None:
        return 3
    # define play_cardx as the 2 character string within source
    elif play_type == 1:
        play_cardx = source[0]
    else:
        play_cardx = source
            
    
    # DEFINING VARIABLES BY DESTINATION 
    
    # TO BUILD PILE
    if destination[0] == 0:
        build_no = destination[1]
        # if invalid build pile, return 0 
        if build_no > 3:
            return 0
        # Otherwise define build_pile as the particular pile in question 
        else:
            build_pile = build_piles[build_no]
            
    # TO DISCARD_PILE 
    else:
        # Define discard_pile as the particular discard pile in question
        to_player_no, pile_num = destination[1]
        discard_pile = discard_piles[to_player_no][pile_num]
        
    # TESTING VALIDITY BY SOURCE 
    # FROM HAND 
    
    if play_type == 0:
        # If trying to play a card that the player does not hold, return 0
        if play_cardx not in hand:
            return 0
        
        # Test play from hand to build pile
        elif destination[0] == 0:
            # If valid play return 1, otherwise return 0
            if comp10001bo_match_build(play_cardx, build_pile):
                return 1
            else:
                return 0 
      
        # Test play from hand to discard pile and return outcome    
        else:
            return comp10001bo_match_discard(play_cardx, discard_pile,
                                             player_no, to_player_no,
                                             from_hand=True)
           
    # FROM DISCARD PILE
    if play_type == 1:
        # Test play from discard pile to build pile
        if destination[0] == 0:
            # If valid, return 1 otherwise return 0
            if comp10001bo_match_build(play_cardx, build_pile):
                return 1
            else:
                return 0 
            
        # Test play from discard pile to discard pile and return outcome    
        else: 
            return comp10001bo_match_discard(play_cardx, discard_pile,
                                             player_no, to_player_no,
                                             from_hand=False)
    
    # FROM STOCKPILE
    if play_type == 2:
        # If trying to play a card that is not stockpile top, return 0
        if play_cardx is not stockpiles[player_no][0]:
            return 0 
        # Test play from stockpile to build pile 
        elif destination[0] == 0:
            # If valid return 1, otherwise return 0
            if comp10001bo_match_build(play_cardx, build_pile):
                return 1
            else:
                return 0
        # Test play from stockpile to discard pile and return outcome
        else:
            return comp10001bo_match_discard(play_cardx, discard_pile,
                                             player_no, to_player_no, 
                                             from_hand=False)
       

# automatically run each of the examples from the question
if __name__ == "__main__":
    tests = (
        # NON-FINAL VALID (from hand to build pile 0)
        (VALID_NONFINAL_PLAY, (0, '2C', (0, 0)), 0,
         ['2C', 'AS', '9D', '0D', '0S'],
         (('9C', 8), ('0D', 8), ('3H', 8), ('KD', 8)),
         (([], [], [], []), ([], [], [], []),
          ([], [], [], []), ([], [], [], [])), ([], [], [], [])),

        # INVALID: doesn't hold card
        (INVALID_PLAY, (0, '2C', (0, 0)), 0,
         ['3C', 'AS', '9D', '0D', '0S'],
         (('9C', 8), ('0D', 8), ('3H', 8), ('KD', 8)),
         (([], [], [], []), ([], [], [], []),
          ([], [], [], []), ([], [], [], [])), ([], [], [], [])),

        # INVALID: invalid pile (build pile 4)
        (INVALID_PLAY, (0, '3C', (0, 4)), 0,
         ['3C', 'AS', '9D', '0D', '0S'],
         (('9C', 8), ('0D', 8), ('3H', 8), ('KD', 8)),
         (([], [], [], []), ([], [], [], []), ([], [], [], []),
          ([], [], [], [])), ([], [], [], [])),

        # INVALID: can't play to build pile 0 (can't start with 3)
        (INVALID_PLAY, (0, '3C', (0, 0)), 0,
         ['3C', 'AS', '9D', '0D', '0S'],
         (('9C', 8), ('0D', 8), ('3H', 8), ('KD', 8)),
         (([], [], [], []), ([], [], [], []), ([], [], [], []),
          ([], [], [], [])), ([], [], [], [])),

        # NON-FINAL VALID (from hand to non-empty build pile 0)
        (VALID_NONFINAL_PLAY, (0, '3C', (0, 0)), 0,
         ['3C', 'AS', '9D', '0D', '0S'],
         (('9C', 8), ('0D', 8), ('3H', 8), ('KD', 8)),
         (([], [], [], []), ([], [], [], []), ([], [], [], []),
          ([], [], [], [])), (['2S'], [], [], [])),

        # NON-FINAL VALID (from stockpile to empty build pile 1)
        (VALID_NONFINAL_PLAY, (2, '2C', (0, 1)), 0,
         ['3C', 'AS', '9D', '0D', '0S'],
         (('2C', 8), ('0D', 8), ('3H', 8), ('KD', 8)),
         (([], [], [], []), ([], [], [], []), ([], [], [], []),
          ([], [], [], [])), (['2S'], [], [], [])),

        # INVALID: attempt to play card that is not top card of own stockpile
        (INVALID_PLAY, (2, '2H', (0, 1)), 0,
         ['3C', 'AS', '9D', '0D', '0S'],
         (('2C', 8), ('0D', 8), ('3H', 8), ('KD', 8)),
         (([], [], [], []), ([], [], [], []), ([], [], [], []),
          ([], [], [], [])), (['2S'], [], [], [])),

        # INVALID: attempt to play card that is not top card of
        # own stockpile (despite being top card of someone else's stockpile)
        (INVALID_PLAY, (2, '2H', (0, 1)), 0,
         ['3C', 'AS', '9D', '0D', '0S'],
         (('2C', 8), ('2H', 8), ('3H', 8), ('KD', 8)),
         (([], [], [], []), ([], [], [], []), ([], [], [], []),
          ([], [], [], [])), (['2S'], [], [], [])),

        # NON-FINAL VALID (from stockpile to non-empty build pile)
        (VALID_NONFINAL_PLAY, (2, 'QC', (0, 1)), 0,
         ['3C', 'AS', '9D', '0D', '0S'],
         (('QC', 8), ('0D', 8), ('3H', 8), ('KD', 8)),
         (([], [], [], []), ([], [], [], []), ([], [], [], []),
          ([], [], [], [])), ([], ['KS'], [], [])),

        # NON-FINAL VALID (from stockpile to *empty* build pile 1)
        (VALID_NONFINAL_PLAY, (2, 'KC', (0, 1)), 0,
         ['3C', 'AS', '9D', '0D', '0S'],
         (('KC', 8), ('0D', 8), ('3H', 8), ('KD', 8)),
         (([], [], [], []), ([], [], [], []), ([], [], [], []),
          ([], [], [], [])), ([], [], [], [])),

        # NON-FINAL VALID (from discard pile to empty build pile 0)
        (VALID_NONFINAL_PLAY, (1, ('2C', (1, 0)), (0, 1)), 0,
         ['3C', 'AS', '9D', '0D', '0S'],
         (('2C', 8), ('0D', 8), ('3H', 8), ('KD', 8)),
         (([], [], [], []), (['3C', '2C'], [], [], []), ([], [], [], []),
          ([], [], [], [])), (['2S'], [], [], [])),

        # INVALID: attempt to access non-top card from
        # discard stack 0 of player 1 
        (INVALID_PLAY, (1, ('3C', (1, 0)), (0, 1)), 0,
         ['3C', 'AS', '9D', '0D', '0S'],
         (('2C', 8), ('0D', 8), ('3H', 8), ('KD', 8)),
         (([], [], [], []), (['3C', '2C'], [], [], []), ([], [], [], []),
          ([], [], [], [])), (['2S'], [], [], [])),

        # INVALID: can't place 2C (from discard stack 0 of Player 1)
        # on 2S (build stack 0)
        (INVALID_PLAY, (1, ('2C', (1, 0)), (0, 0)), 0,
         ['3C', 'AS', '9D', '0D', '0S'],
         (('2C', 8), ('0D', 8), ('3H', 8), ('KD', 8)),
         (([], [], [], []), (['3C', '2C'], [], [], []), ([], [], [], []),
          ([], [], [], [])), (['2S'], [], [], [])),

        # FINAL VALID: can place 9D (from hand) on 5S (discard
        # stack 0 of Player 0), but final play for turn
        (VALID_FINAL_PLAY, (0, '9D', (1, (0, 0))), 0,
         ['AS', '9D', '0D', '0S'],
         (('9C', 8), ('0D', 8), ('3H', 8), ('KD', 8)),
         ((['5S'], [], [], []), ([], [], [], []), ([], [], [], []),
          ([], [], [], [])), ([], [], [], [])),

        # INVALID: can make a number of different plays
        (INVALID_PLAY, (3, None, (None, None)), 0, 
         ['AS', '9D', '0S'], 
         (('9C', 8), ('0D', 8), ('3H', 8), ('KD', 8)), 
         ((['5S'], [], [], []), ([], [], [], []), ([], [], [], []),
          ([], [], [], [])), ([], [], [], [])),

        # NO_PLAY: no move possible (yes, it's an impossible game
        # state, but it proves a point)
        (NO_PLAY, (3, None, (None, None)), 0, [], 
         (('9C', 8), ('0D', 8), ('3H', 8), ('KD', 8)), 
         ((['5S'], [], [], []), ([], [], [], []), ([], [], [], []), 
          ([], [], [], [])), ([], [], [], [])),

        # INVALID (attempt to move card from discard pile back to
        # same discard pile)
        (INVALID_PLAY, (1, ('2C', (1, 0)), (1, (1, 0))), 0,
         ['3C', 'AS', '9D', '0D', '0S'], 
         (('2C', 8), ('0D', 8), ('3H', 8), ('KD', 8)), 
         (([], [], [], []), (['3C', '2C'], [], [], []),
          ([], [], [], []), ([], [], [], [])), (['2S'], [], [], [])),


    )

    for retval, *args in tests:
        if comp10001bo_is_valid_play(*args) == retval:
            result = "passed"
        else:
            result = "failed"
        print("Testing comp10001bo_is_valid_play{} ... {}".format(
            repr(tuple(args)), result))