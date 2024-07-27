from flask import Flask, jsonify, make_response, Response
from flask_cors import CORS

from chopsticks.chopstick_controller import get_board_state, get_current_player, get_player_hand, init_game, move, swap
from chopsticks.chopstick_view import ChopstickView

app = Flask(__name__)
CORS(app)  # This will allow the React front-end to communicate with the Flask back-end


VIEW = ChopstickView()


@app.route("/chopsticks/health", methods=["GET"])
@app.route("/chopsticks/healthcheck", methods=["GET"])
def health_check() -> Response:
    app.logger.info('Health check')
    return make_response(jsonify({"status": "OK"}), 200)

@app.route("/chopsticks/get_board_state", methods=["GET"])
def board_state() -> Response:
    app.logger.info('Get board state')
    return get_board_state()

@app.route("/chopsticks/get_current_player", methods=["GET"])
def current_player() -> Response:
    app.logger.info('Get current player')
    return get_current_player()

@app.route("/chopsticks/get_player_hand/<player>/<hand>", methods=["GET"])
def player_hand(player: str, hand: str) -> Response:
    app.logger.info('Get player hand')
    return get_player_hand(player, hand)

@app.route('/chopsticks/move/<player>/<from_hand>/<to_hand>', methods=['GET'])
def make_move(player: str, from_hand: str, to_hand: str) -> Response:
    app.logger.info('Make move')
    try:
        move(player, from_hand, to_hand)
    except ValueError as e:
        return VIEW.error(str(e))
    return make_response(jsonify({"message": "Move successful"}), 200)

@app.route("/chopsticks/reset", methods=["GET"])
def reset_game() -> Response:
    app.logger.info('Reset game')
    init_game()
    return make_response(jsonify({"message": "Game reset"}), 200)

@app.route("/chopsticks/swap/<player>/<hand>/<fingers>", methods=["GET"])
def swap_fingers(player: str, hand: str, fingers: str) -> Response:
    app.logger.info('Swap fingers')
    try:
        swap(player, hand, fingers)
    except ValueError as e:
        return VIEW.error(str(e))
    return make_response(jsonify({"message": "Swap successful"}), 200)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
