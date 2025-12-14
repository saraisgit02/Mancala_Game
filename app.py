"""
Serveur Flask pour l'interface web Mancala
Connecte l'interface graphique avec les algorithmes Python
Auteur: Projet 4 - Problem Solving
VERSION CORRIGÉE
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import uuid
import copy

# Import de vos classes Python
from mancala_board import MancalaBoard
from game import Game
from minimax import minimax_alpha_beta_pruning, MAX

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_ici_changez_la'
CORS(app)

# Stockage des parties en cours (en mémoire)
games = {}


@app.route('/')
def index():
    """Page d'accueil - Affiche l'interface web"""
    return render_template('index.html')


@app.route('/api/new_game', methods=['POST'])
def new_game():
    """
    Crée une nouvelle partie
    
    Body JSON:
        {
            "mode": "hvai" ou "aivai",
            "depth": 6 (profondeur de recherche)
        }
    
    Returns:
        {
            "game_id": "uuid",
            "board": {...},
            "current_player": "player1",
            "mode": "hvai"
        }
    """
    try:
        data = request.json
        mode = data.get('mode', 'hvai')
        depth = data.get('depth', 6)
        
        # Créer un ID unique pour la partie
        game_id = str(uuid.uuid4())
        
        # Configurer playerSide selon le mode
        if mode == 'hvai':
            player_side = {'HUMAN': 'player1', 'COMPUTER': 'player2'}
        else:  # aivai
            player_side = {'COMPUTER': 'player1', 'HUMAN': 'player2'}
        
        # Créer la partie
        game = Game(player_side=player_side)
        
        # Stocker la partie avec ses métadonnées
        games[game_id] = {
            'game': game,
            'mode': mode,
            'depth': depth,
            'current_player': 'player1',
            'move_history': []
        }
        
        return jsonify({
            'game_id': game_id,
            'board': game.state.board,
            'current_player': 'player1',
            'mode': mode,
            'game_over': False
        })
    
    except Exception as e:
        print(f"❌ Erreur new_game: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/get_state/<game_id>', methods=['GET'])
def get_state(game_id):
    """
    Récupère l'état actuel d'une partie
    
    Returns:
        {
            "board": {...},
            "current_player": "player1",
            "game_over": false,
            "winner": null
        }
    """
    try:
        if game_id not in games:
            return jsonify({'error': 'Partie non trouvée'}), 404
        
        game_data = games[game_id]
        game = game_data['game']
        
        is_game_over = game.game_over()
        winner = game.find_winner() if is_game_over else None
        
        return jsonify({
            'board': game.state.board,
            'current_player': game_data['current_player'],
            'game_over': is_game_over,
            'winner': winner,
            'move_history': game_data['move_history']
        })
    
    except Exception as e:
        print(f"❌ Erreur get_state: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/human_move/<game_id>', methods=['POST'])
def human_move(game_id):
    """
    Exécute un coup du joueur humain
    
    Body JSON:
        {
            "pit": "A"
        }
    
    Returns:
        État mis à jour de la partie
    """
    try:
        if game_id not in games:
            return jsonify({'error': 'Partie non trouvée'}), 404
        
        data = request.json
        pit = data.get('pit')
        
        game_data = games[game_id]
        game = game_data['game']
        
        # Vérifier que c'est le tour du joueur humain
        if game_data['mode'] == 'hvai' and game_data['current_player'] != 'player1':
            return jsonify({'error': 'Ce n\'est pas votre tour'}), 400
        
        # Vérifier que le coup est valide
        moves = game.state.possibleMoves(game_data['current_player'])
        if pit not in moves:
            return jsonify({'error': 'Coup invalide'}), 400
        
        # Exécuter le coup
        game.state.doMove(game_data['current_player'], pit)
        
        # Ajouter à l'historique
        game_data['move_history'].append({
            'player': game_data['current_player'],
            'pit': pit,
            'type': 'Human'
        })
        
        # Changer de joueur
        game_data['current_player'] = 'player2' if game_data['current_player'] == 'player1' else 'player1'
        
        # Vérifier fin de partie
        is_game_over = game.game_over()
        winner = game.find_winner() if is_game_over else None
        
        return jsonify({
            'board': game.state.board,
            'current_player': game_data['current_player'],
            'game_over': is_game_over,
            'winner': winner,
            'move_history': game_data['move_history']
        })
    
    except Exception as e:
        print(f"❌ Erreur human_move: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/ai_move/<game_id>', methods=['POST'])
def ai_move(game_id):
    """
    Calcule et exécute un coup de l'IA
    
    Body JSON (optionnel):
        {
            "heuristic": "balanced" ou "aggressive"
        }
    
    Returns:
        État mis à jour de la partie avec le meilleur coup
    """
    try:
        if game_id not in games:
            return jsonify({'error': 'Partie non trouvée'}), 404
        
        data = request.json or {}
        heuristic = data.get('heuristic', 'balanced')
        
        game_data = games[game_id]
        game = game_data['game']
        depth = game_data['depth']
        current_player = game_data['current_player']
        
        # Vérifier qu'il y a des coups possibles
        moves = game.state.possibleMoves(current_player)
        if not moves:
            return jsonify({'error': 'Aucun coup possible'}), 400
        
        # Calculer le meilleur coup avec Minimax Alpha-Beta
        best_value, best_pit = minimax_alpha_beta_pruning(
            game, 
            MAX, 
            depth, 
            float('-inf'), 
            float('+inf'),
            heuristic
        )
        
        if not best_pit:
            return jsonify({'error': 'Aucun coup trouvé'}), 500
        
        # Exécuter le coup
        game.state.doMove(current_player, best_pit)
        
        # Ajouter à l'historique
        game_data['move_history'].append({
            'player': current_player,
            'pit': best_pit,
            'type': 'AI',
            'evaluation': best_value
        })
        
        # Changer de joueur
        game_data['current_player'] = 'player2' if current_player == 'player1' else 'player1'
        
        # Vérifier fin de partie
        is_game_over = game.game_over()
        winner = game.find_winner() if is_game_over else None
        
        return jsonify({
            'board': game.state.board,
            'current_player': game_data['current_player'],
            'game_over': is_game_over,
            'winner': winner,
            'best_pit': best_pit,
            'evaluation': best_value,
            'move_history': game_data['move_history']
        })
    
    except Exception as e:
        print(f"❌ Erreur ai_move: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/possible_moves/<game_id>', methods=['GET'])
def possible_moves(game_id):
    """
    Retourne les coups possibles pour le joueur actuel
    
    Returns:
        {
            "moves": ["A", "B", "C", ...],
            "player": "player1"
        }
    """
    try:
        if game_id not in games:
            return jsonify({'error': 'Partie non trouvée'}), 404
        
        game_data = games[game_id]
        game = game_data['game']
        current_player = game_data['current_player']
        
        moves = game.state.possibleMoves(current_player)
        
        return jsonify({
            'moves': moves,
            'player': current_player
        })
    
    except Exception as e:
        print(f"❌ Erreur possible_moves: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/delete_game/<game_id>', methods=['DELETE'])
def delete_game(game_id):
    """
    Supprime une partie de la mémoire
    """
    try:
        if game_id in games:
            del games[game_id]
            return jsonify({'message': 'Partie supprimée'})
        else:
            return jsonify({'error': 'Partie non trouvée'}), 404
    
    except Exception as e:
        print(f"❌ Erreur delete_game: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def stats():
    """
    Retourne des statistiques sur les parties en cours
    """
    return jsonify({
        'active_games': len(games),
        'games': [{
            'game_id': gid,
            'mode': data['mode'],
            'current_player': data['current_player'],
            'moves': len(data['move_history'])
        } for gid, data in games.items()]
    })


if __name__ == '__main__':
    print("="*60)
    print("🎮 Serveur Mancala démarré!")
    print("="*60)
    print("\n📍 Accédez à l'interface web sur:")
    print("   👉 http://localhost:5000")
    print("\n🔌 API endpoints disponibles:")
    print("   POST   /api/new_game          - Créer une nouvelle partie")
    print("   GET    /api/get_state/<id>    - État de la partie")
    print("   POST   /api/human_move/<id>   - Coup du joueur")
    print("   POST   /api/ai_move/<id>      - Coup de l'IA")
    print("   GET    /api/possible_moves/<id> - Coups possibles")
    print("   DELETE /api/delete_game/<id>  - Supprimer une partie")
    print("   GET    /api/stats             - Statistiques")
    print("\n" + "="*60)
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)