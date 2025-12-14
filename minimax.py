"""
Algorithme Minimax avec élagage Alpha-Beta
VERSION CORRIGÉE avec support des deux heuristiques
"""

# Constantes pour représenter les joueurs
MAX = 1      # Ordinateur (cherche à maximiser)
MIN = -1     # Humain (cherche à minimiser)

def minimax_alpha_beta_pruning(game, player, depth, alpha, beta, heuristic='balanced'):
    """
    Algorithme Minimax avec élagage Alpha-Beta
    
    Args:
        game (Game): Instance du jeu actuel
        player (int): MAX (1) ou MIN (-1)
        depth (int): Profondeur restante à explorer
        alpha (float): Meilleure valeur garantie pour MAX
        beta (float): Meilleure valeur garantie pour MIN
        heuristic (str): 'balanced' ou 'aggressive'
        
    Returns:
        tuple: (best_value, best_pit)
    """
    
    # ========== CAS DE BASE ==========
    if game.game_over() or depth == 0:
        # Choisir la fonction d'évaluation selon l'heuristique
        if heuristic == 'aggressive':
            best_value = game.evaluate_aggressive()
        else:
            best_value = game.evaluate()
        return best_value, None
    
    # Déterminer quel joueur joue
    current_player_key = 'COMPUTER' if player == MAX else 'HUMAN'
    current_player = game.player_side[current_player_key]
    
    # Obtenir tous les coups possibles
    possible_moves = game.state.possibleMoves(current_player)
    
    # Si aucun coup possible, évaluer l'état
    if not possible_moves:
        if heuristic == 'aggressive':
            return game.evaluate_aggressive(), None
        else:
            return game.evaluate(), None
    
    best_pit = possible_moves[0]
    
    # ========== CAS RÉCURSIF - MAX (ORDINATEUR) ==========
    if player == MAX:
        best_value = float('-inf')
        
        for pit in possible_moves:
            child_game = game.copy()
            child_game.state.doMove(current_player, pit)
            
            value, _ = minimax_alpha_beta_pruning(
                child_game, 
                -player,
                depth - 1,
                alpha, 
                beta,
                heuristic
            )
            
            if value > best_value:
                best_value = value
                best_pit = pit
            
            # ÉLAGAGE BETA
            if best_value >= beta:
                break
            
            if best_value > alpha:
                alpha = best_value
    
    # ========== CAS RÉCURSIF - MIN (HUMAIN) ==========
    else:
        best_value = float('inf')
        
        for pit in possible_moves:
            child_game = game.copy()
            child_game.state.doMove(current_player, pit)
            
            value, _ = minimax_alpha_beta_pruning(
                child_game,
                -player,
                depth - 1,
                alpha,
                beta,
                heuristic
            )
            
            if value < best_value:
                best_value = value
                best_pit = pit
            
            # ÉLAGAGE ALPHA
            if best_value <= alpha:
                break
            
            if best_value < beta:
                beta = best_value
    
    return best_value, best_pit


def get_best_move(game, depth=6, heuristic='balanced'):
    """
    Interface simplifiée pour obtenir le meilleur coup pour l'ordinateur
    
    Args:
        game (Game): État actuel du jeu
        depth (int): Profondeur de recherche (par défaut 6)
        heuristic (str): 'balanced' ou 'aggressive'
        
    Returns:
        str: Indice du meilleur puits à jouer
    """
    value, pit = minimax_alpha_beta_pruning(
        game, 
        MAX,
        depth, 
        float('-inf'),
        float('inf'),
        heuristic
    )
    return pit