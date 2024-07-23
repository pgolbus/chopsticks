import logging
from flask import Response

from .chopstick_model import ChopstickModel
from .chopstick_view import ChopstickView

INVALID_HAND_ERROR_MSG = "Hand must be 'left' or 'right'"
INVALID_PLAYER_ERROR_MSG = "Player must be an integer, either 0 or 1."
WRONG_PLAYER_ERROR_MSG = "It is player {current_player}'s turn."

# Create module-level model and view instances
MODEL = ChopstickModel()
VIEW = ChopstickView()

logger = logging.getLogger(__name__)

def change_player() -> None:
    """
    Change the current player to the next player.
    """
    MODEL.change_player()
    logger.info(f"Changed current player to {MODEL.get_current_player()}.")

def check_win() -> bool:
    """
    Check if the current player has won the game.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    player = MODEL.get_player_hands(MODEL.get_current_player())
    win = player.left + player.right == 0
    logger.info(f"Checked win condition for player {MODEL.get_current_player()}: {'win' if win else 'no win'}.")
    return win

def get_winner() -> int:
    """
    Get the winner of the game.

    Returns:
        int: The winner (0 or 1) or -1 if no one has won.
    """
    return MODEL.get_winner()

def set_winner() -> None:
    """
    Inform the model of the current winner of the game
    """
    if check_win():
        change_player()
        winner = MODEL.get_current_player()
        logger.info(f"Player {winner} has won the game.")
        MODEL.set_winner(winner)
    else:
        logger.info("No player has won yet.")

def get_current_player() -> Response:
    """
    Get the current player.

    Returns:
        Response: Flask response object containing the current player.
    """
    current_player = MODEL.get_current_player()
    return VIEW.get_player(current_player)

def get_player_hand(player: str, hand: str) -> Response:
    """
    Get the value of a specific hand for a player.

    Args:
        player (str): The index of the player in the array of players.
        hand (str): The hand to get the value of.

    Returns:
        Response: Flask response object containing the value of the hand.
    """
    try:
        player = int(player)
    except ValueError:
        e = ValueError(INVALID_PLAYER_ERROR_MSG)
        logger.error(e)
        return VIEW.error(str(e))
    player_obj = MODEL.get_player_hands(player)
    return VIEW.get_hand(player_obj, hand)

def validate_player(player: str) -> None:
    """
    Validate the player.

    Args:
        player (str): The player to validate.

    Raises:
        ValueError: If player is not an integer 0 or 1.
        ValueError: If it is not the current player's turn.
    """
    try:
        player = int(player)
    except ValueError:
        logger.error(INVALID_PLAYER_ERROR_MSG)
        raise ValueError(INVALID_PLAYER_ERROR_MSG)
    if player not in (0, 1):
        logger.error(INVALID_PLAYER_ERROR_MSG)
        raise ValueError(INVALID_PLAYER_ERROR_MSG)
    if player != MODEL.get_current_player():
        display_player = MODEL.get_current_player() + 1
        logger.error(WRONG_PLAYER_ERROR_MSG.format(current_player=display_player))
        raise ValueError(WRONG_PLAYER_ERROR_MSG.format(current_player=display_player))

def validate_hand(hand: str) -> None:
    """
    Validate the hand.

    Args:
        hand (str): The hand to validate.

    Raises:
        ValueError: If hand is not "left" or "right".
    """
    if hand not in ("left", "right"):
        logger.error(INVALID_HAND_ERROR_MSG)
        raise ValueError(INVALID_HAND_ERROR_MSG)

def move(player: str, from_hand: str, to_hand: str) -> Response:
    """
    Execute a move in the game and check if the move results in a win.

    Args:
        player (str): The player making the move (should be "0" or "1").
        from_hand (str): The hand to move from (should be "left" or "right").
        to_hand (str): The hand to move to (should be "left" or "right").

    Returns:
        Response: The Flask response object containing the move result.

    Raises:
        ValueError: If player is not "0" or "1".
        ValueError: If from_hand or to_hand are not "left" or "right".
    """
    try:
        logger.info(f"Player {player} is attempting to move from {from_hand} to {to_hand}.")
        validate_player(player)
        validate_hand(from_hand)
        validate_hand(to_hand)
        MODEL.move(MODEL.get_current_player(), from_hand, to_hand)
        logger.info(f"Move completed.")
        return end_move()
    except ValueError as e:
        logger.error(e)
        return VIEW.error(str(e))

def swap(player: str, hand: str, fingers: str) -> Response:
    """
    Execute a swap of fingers between hands.

    Args:
        player (str): The player making the swap (should be "0" or "1").
        hand (str): The hand to swap from (should be "left" or "right").
        fingers (str): The number of fingers to swap (should be a string representing an integer).

    Returns:
        Response: The Flask response object containing the swap result.

    Raises:
        ValueError: If player is not "0" or "1".
        ValueError: If hand is not "left" or "right".
    """
    try:
        logger.info(f"Player {player} is attempting to swap {fingers} fingers from {hand}.")
        validate_player(player)
        validate_hand(hand)
        MODEL.swap(player, hand, fingers)
        logger.info(f"Swap completed for player {player}.")
        return end_move()
    except ValueError as e:
        logger.error(e)
        return VIEW.error(str(e))

def end_move() -> None:
    """
    Change players and check for a winner
    """
    change_player()
    set_winner()

def board_state() -> Response:
    """
    Get the current state of the board and display it using the view.

    Returns:
        Response: The Flask response object containing the board state.
    """
    player1 = MODEL.get_player_hands(0)
    player2 = MODEL.get_player_hands(1)
    winner = MODEL.get_winner()
    return VIEW.board_state(player1, player2, winner)
