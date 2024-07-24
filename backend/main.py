from flask import Flask, Response, make_response
from flask_cors import CORS

from app import configure_logger
from app.chopstick_controller import get_board_state, get_current_player, get_player_hand, init_game, move, swap


app = Flask(__name__)
CORS(app)


configure_logger()


@app.route("/chopsticks/health", methods=["GET"])
@app.route("/chopsticks/healthcheck", methods=["GET"])
def health_check() -> Response:
    return make_response("OK", 200)

@app.route("/chopsticks/get_board_state", methods=["GET"])
def board_state() -> Response:
    return get_board_state()

@app.route("/chopsticks/get_current_player", methods=["GET"])
def current_player() -> Response:
    return get_current_player()

@app.route("/chopsticks/get_player_hand/<player>/<hand>", methods=["GET"])
def player_hand(player: str, hand: str) -> Response:
    return get_player_hand(player, hand)

@app.route('/chopsticks/move/<player>/<from_hand>/<to_hand>', methods=['GET'])
def make_move(player: str, from_hand: str, to_hand: str) -> Response:
    move(player, from_hand, to_hand)
    return make_response("OK", 200)

@app.route("/chopsticks/swap/<player>/<hand>/<fingers>", methods=["GET"])
def make_swap(player: str, hand: str, fingers: str) -> Response:
    swap(player, hand, fingers)
    return make_response("OK", 200)

@app.route("/chopsticks/reset", methods=["GET"])
def reset_game() -> Response:
    init_game()
    return make_response("OK", 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
