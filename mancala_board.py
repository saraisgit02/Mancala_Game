"""
Classe MancalaBoard - Modélisation de l'état du jeu Mancala
Auteur: Projet 4 - Problem Solving
VERSION CORRIGÉE
"""

class MancalaBoard:
    """Représente l'état du plateau de jeu Mancala"""
    
    def __init__(self):
        """Initialise le plateau avec 4 graines dans chaque pit"""
        self.board = {
            'A': 4, 'B': 4, 'C': 4, 'D': 4, 'E': 4, 'F': 4,
            '1': 0,
            'G': 4, 'H': 4, 'I': 4, 'J': 4, 'K': 4, 'L': 4,
            '2': 0
        }
        
        # Garder camelCase pour compatibilité
        self.player1Pits = ('A', 'B', 'C', 'D', 'E', 'F')
        self.player2Pits = ('G', 'H', 'I', 'J', 'K', 'L')
        
        # Dictionnaire des pits opposés
        self.oppositePits = {
            'A': 'L', 'B': 'K', 'C': 'J', 'D': 'I', 'E': 'H', 'F': 'G',
            'G': 'F', 'H': 'E', 'I': 'D', 'J': 'C', 'K': 'B', 'L': 'A'
        }
        
        # Dictionnaire de séquence (sens anti-horaire)
        self.nextPit = {
            'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F', 'F': '1',
            '1': 'G', 'G': 'H', 'H': 'I', 'I': 'J', 'J': 'K', 'K': 'L',
            'L': '2', '2': 'A'
        }
    
    def copy(self):
        """Crée une copie profonde du plateau"""
        new_board = MancalaBoard()
        new_board.board = self.board.copy()
        return new_board
    
    def possibleMoves(self, player):
        """
        Retourne les coups possibles pour un joueur
        
        Args:
            player (str): 'player1' ou 'player2'
            
        Returns:
            list: Liste des indices de pits contenant des graines
        """
        pits = self.player1Pits if player == 'player1' else self.player2Pits
        return [pit for pit in pits if self.board[pit] > 0]
    
    def doMove(self, player, pit):
        """
        Exécute un mouvement pour un joueur
        
        Args:
            player (str): 'player1' ou 'player2'
            pit (str): Indice du pit à jouer (A-F ou G-L)
        """
        # Récupérer les graines du pit choisi
        seeds = self.board[pit]
        self.board[pit] = 0
        
        current_pit = pit
        opponent_store = '2' if player == 'player1' else '1'
        player_store = '1' if player == 'player1' else '2'
        player_pits = self.player1Pits if player == 'player1' else self.player2Pits
        
        # Distribuer les graines dans le sens anti-horaire
        while seeds > 0:
            current_pit = self.nextPit[current_pit]
            
            # Sauter le store de l'adversaire
            if current_pit == opponent_store:
                continue
            
            self.board[current_pit] += 1
            seeds -= 1
        
        # Règle de capture: si dernière graine tombe dans pit vide du joueur
        if current_pit in player_pits and self.board[current_pit] == 1:
            opposite_pit = self.oppositePits[current_pit]
            if self.board[opposite_pit] > 0:
                # Capturer les graines
                self.board[player_store] += self.board[current_pit] + self.board[opposite_pit]
                self.board[current_pit] = 0
                self.board[opposite_pit] = 0
    
    def __str__(self):
        """Représentation textuelle du plateau"""
        result = "\n"
        result += "      L    K    J    I    H    G\n"
        result += f"  {self.board['2']:2d} "
        for pit in ['L', 'K', 'J', 'I', 'H', 'G']:
            result += f"[{self.board[pit]:2d}] "
        result += "\n"
        result += "     "
        for pit in ['A', 'B', 'C', 'D', 'E', 'F']:
            result += f"[{self.board[pit]:2d}] "
        result += f"{self.board['1']:2d}\n"
        result += "      A    B    C    D    E    F\n"
        return result