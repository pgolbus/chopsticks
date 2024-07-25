from flask import Flask, Response, make_response
from flask_cors import CORS

from flask_service import configure_logger
from flask_service.chopstick_controller import get_board_state, get_current_player, get_player_hand, init_game, move, swap


app = Flask(__name__)
CORS(app)

configure_logger()


@app.route("/chopsticks/health", methods=["GET", "OPTIONS"])
@app.route("/chopsticks/healthcheck", methods=["GET", "OPTIONS"])
def health_check() -> Response:
    return make_response("OK", 200)

@app.route("/chopsticks/get_board_state", methods=["GET", "OPTIONS"])
def board_state() -> Response:
    return make_response("OK", 200) # get_board_state()

@app.route("/chopsticks/get_current_player", methods=["GET", "OPTIONS"])
def current_player() -> Response:
    return get_current_player()

@app.route("/chopsticks/get_player_hand/<player>/<hand>", methods=["GET", "OPTIONS"])
def player_hand(player: str, hand: str) -> Response:
    return get_player_hand(player, hand)

@app.route("/chopsticks/move/<player>/<from_hand>/<to_hand>", methods=["GET", "OPTIONS"])
def make_move(player: str, from_hand: str, to_hand: str) -> Response:
    move(player, from_hand, to_hand)
    return make_response("OK", 200)

@app.route("/chopsticks/swap/<player>/<hand>/<fingers>", methods=["GET", "OPTIONS"])
def make_swap(player: str, hand: str, fingers: str) -> Response:
    swap(player, hand, fingers)
    return make_response("OK", 200)

@app.route("/chopsticks/reset", methods=["GET", "OPTIONS"])
def reset_game() -> Response:
    init_game()
    return make_response("OK", 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)