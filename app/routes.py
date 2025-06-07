from flask import Blueprint, jsonify, request
from .game import GameState
from .ia_agent import AIAgent


game_state = GameState()
ai_agent = AIAgent(game_state)

bp = Blueprint('api', __name__)


@bp.route('/estado', methods=['GET'])
def estado():
    return jsonify(game_state.to_dict())


@bp.route('/accion_jugador', methods=['POST'])
def accion_jugador():
    data = request.json
    accion = data.get('accion')
    if accion == 'mover':
        game_state.move_unit('human', data['tipo'], data['origen'], data['destino'])
    elif accion == 'atacar':
        game_state.attack('human', data['origen'], data['destino'])
    return jsonify(game_state.to_dict())


@bp.route('/accion_ia', methods=['POST'])
def accion_ia():
    ai_agent.decide_and_act()
    return jsonify(game_state.to_dict())


@bp.route('/puntuacion', methods=['GET'])
def puntuacion():
    return jsonify({'score': game_state.score})


@bp.route('/reiniciar', methods=['GET'])
def reiniciar():
    game_state.reset()
    return jsonify(game_state.to_dict())
