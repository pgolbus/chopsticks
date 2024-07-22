from flask import Flask, Response

from backend import configure_logger
from backend.chopstick_controller import get_current_player, move, swap


app = Flask(__name__)


configure_logger()

@app.route("/chopsticks/get_current_player", methods=["GET"])
def current_player() -> Response:
    return get_current_player()

@app.route('/chopsticks/move/<player>/<from_hand>/<to_hand>', methods=['GET'])
def make_move(player: str, from_hand: str, to_hand: str) -> Response:
    return move(player, from_hand, to_hand)

@app.route("/chopsticks/swap/<player>/<hand>/<fingers>", methods=["GET"])
def make_swap(player: str, hand: str, fingers: str) -> Response:
    return swap(player, hand, fingers)


if __name__ == "__main__":
    app.run(debug=True)
