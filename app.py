from flask import Flask, Response
from flask_cors import CORS

from backend import configure_logger
from backend.chopstick_controller import get_current_player, get_player_hand, move, swap


app = Flask(__name__)
CORS(app)


configure_logger()

@app.route("/chopsticks/get_board_state", methods=["GET"])
def board_state() -> Response:
    return board_state()

@app.route("/chopsticks/get_current_player", methods=["GET"])
def current_player() -> Response:
    return get_current_player()

@app.route("/chopsticks/get_player_hand/<player>/<hand>", methods=["GET"])
def player_hand(player: str, hand: str) -> Response:
    return get_player_hand(player, hand)

@app.route('/chopsticks/move/<player>/<from_hand>/<to_hand>', methods=['GET'])
def make_move(player: str, from_hand: str, to_hand: str) -> Response:
    return move(player, from_hand, to_hand)

@app.route("/chopsticks/swap/<player>/<hand>/<fingers>", methods=["GET"])
def make_swap(player: str, hand: str, fingers: str) -> Response:
    return swap(player, hand, fingers)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
