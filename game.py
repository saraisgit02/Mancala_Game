"""
Classe Game - Nœud dans l'arbre de recherche Minimax
VERSION CORRIGÉE avec deux heuristiques
"""

from mancala_board import MancalaBoard

class Game:
    """
    Classe représentant un état du jeu (nœud dans l'arbre Minimax)
    Contient l'état du plateau et les fonctions d'évaluation
    """
    
    def __init__(self, player_side=None, board=None):
        """
        Initialise une instance de jeu
        
        Args:
            player_side (dict): Dictionnaire assignant HUMAN/COMPUTER aux joueurs
            board (MancalaBoard): État du plateau (None = nouveau jeu)
        """
        self.state = board if board else MancalaBoard()
        
        # Attribution des côtés aux joueurs
        self.player_side = player_side if player_side else {
            'COMPUTER': 'player2',
            'HUMAN': 'player1'
        }
    
    def game_over(self):
        """
        Vérifie si la partie est terminée
        Une partie se termine quand tous les puits d'un joueur sont vides
        
        Returns:
            bool: True si le jeu est terminé, False sinon
        """
        # Vérifier si tous les puits du joueur 1 sont vides
        player1_empty = all(
            self.state.board[pit] == 0 
            for pit in self.state.player1Pits
        )
        
        # Vérifier si tous les puits du joueur 2 sont vides
        player2_empty = all(
            self.state.board[pit] == 0 
            for pit in self.state.player2Pits
        )
        
        # Si un joueur n'a plus de graines, la partie est terminée
        if player1_empty or player2_empty:
            # RÈGLE DE FIN : Collecter toutes les graines restantes
            if player1_empty:
                for pit in self.state.player2Pits:
                    self.state.board['2'] += self.state.board[pit]
                    self.state.board[pit] = 0
            else:
                for pit in self.state.player1Pits:
                    self.state.board['1'] += self.state.board[pit]
                    self.state.board[pit] = 0
            
            return True
        
        return False
    
    def find_winner(self):
        """
        Détermine le gagnant de la partie
        
        Returns:
            dict: {
                'winner': 'player1', 'player2', ou 'draw',
                'score1': score du joueur 1,
                'score2': score du joueur 2
            }
        """
        score1 = self.state.board['1']
        score2 = self.state.board['2']
        
        if score1 > score2:
            winner = 'player1'
        elif score2 > score1:
            winner = 'player2'
        else:
            winner = 'draw'
        
        return {
            'winner': winner,
            'score1': score1,
            'score2': score2
        }
    
    def evaluate(self):
        """
        HEURISTIQUE BALANCED (Équilibrée)
        
        Formule : value(n) = graines_COMPUTER - graines_HUMAN
        
        Returns:
            int: Score d'évaluation
        """
        computer_store = '1' if self.player_side['COMPUTER'] == 'player1' else '2'
        computer_seeds = self.state.board[computer_store]
        
        human_store = '1' if self.player_side['HUMAN'] == 'player1' else '2'
        human_seeds = self.state.board[human_store]
        
        return computer_seeds - human_seeds
    
    def evaluate_aggressive(self):
        """
        HEURISTIQUE AGGRESSIVE (Pour Computer vs Computer)
        
        Cette heuristique prend en compte :
        1. La différence de graines dans les stores (poids x2)
        2. Le nombre de graines encore en jeu du côté de l'ordinateur
        3. Les opportunités de capture
        
        Returns:
            int: Score d'évaluation
        """
        computer_side = self.player_side['COMPUTER']
        human_side = self.player_side['HUMAN']
        
        computer_store = '1' if computer_side == 'player1' else '2'
        human_store = '1' if human_side == 'player1' else '2'
        
        # 1. Différence dans les stores (priorité principale)
        store_diff = (self.state.board[computer_store] - 
                     self.state.board[human_store]) * 2
        
        # 2. Graines encore en jeu (favorise les positions offensives)
        computer_pits = (self.state.player1Pits if computer_side == 'player1' 
                        else self.state.player2Pits)
        seeds_in_play = sum(self.state.board[pit] for pit in computer_pits)
        
        # 3. Opportunités de capture (pits avec 1 graine face à des pits pleins)
        capture_opportunities = 0
        for pit in computer_pits:
            if self.state.board[pit] == 1:
                opposite = self.state.oppositePits[pit]
                if self.state.board[opposite] > 0:
                    capture_opportunities += self.state.board[opposite]
        
        return store_diff + (seeds_in_play // 2) + capture_opportunities
    
    def copy(self):
        """
        Crée une copie profonde du jeu (pour la simulation dans Minimax)
        
        Returns:
            Game: Nouvelle instance identique
        """
        new_game = Game(
            board=self.state.copy(),
            player_side=self.player_side.copy()
        )
        return new_game
    
    def __str__(self):
        """Représentation textuelle du jeu"""
        result = "\n=== État du Jeu ===\n"
        result += str(self.state)
        result += f"\nScores - Joueur 1: {self.state.board['1']}, "
        result += f"Joueur 2: {self.state.board['2']}\n"
        return result