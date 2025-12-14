"""
Classe Play - Gestion des tours de jeu
Auteur: Projet 4 - Problem Solving
VERSION CORRIGÉE
"""

from game import Game
from minimax import minimax_alpha_beta_pruning, MAX


class Play:
    """Gère le déroulement d'une partie de Mancala"""
    
    def __init__(self, game_mode='hvai', search_depth=6):
        """
        Initialise une partie
        
        Args:
            game_mode (str): 'hvai' (Human vs AI) ou 'aivai' (AI vs AI)
            search_depth (int): Profondeur de recherche pour l'algorithme
        """
        self.game_mode = game_mode
        self.search_depth = search_depth
        self.current_player = 'player1'
        
        # Configuration des côtés selon le mode
        if game_mode == 'hvai':
            self.player_side = {'HUMAN': 'player1', 'COMPUTER': 'player2'}
        else:  # aivai
            self.player_side = {'COMPUTER': 'player1', 'HUMAN': 'player2'}
        
        self.game = Game(player_side=self.player_side)
    
    def humanTurn(self):
        """
        Permet au joueur humain de jouer son tour
        
        Returns:
            bool: True si le coup a été joué, False sinon
        """
        print(self.game)
        print(f"\n🎮 Tour de {self.current_player}")
        
        # Obtenir les coups possibles
        moves = self.game.state.possibleMoves(self.current_player)
        
        if not moves:
            print("❌ Aucun coup possible!")
            return False
        
        print(f"Coups possibles: {moves}")
        
        # Demander le coup au joueur
        while True:
            try:
                pit = input("Choisissez un pit: ").upper()
                if pit in moves:
                    break
                print(f"❌ Choix invalide! Choisissez parmi: {moves}")
            except:
                print("❌ Entrée invalide!")
        
        # Exécuter le coup
        self.game.state.doMove(self.current_player, pit)
        return True
    
    def computerTurn(self, heuristic='balanced'):
        """
        Permet à l'ordinateur de jouer son tour
        
        Args:
            heuristic (str): Type d'heuristique ('balanced' ou 'aggressive')
            
        Returns:
            bool: True si le coup a été joué, False sinon
        """
        print(self.game)
        print(f"\n🤖 Tour de l'IA ({self.current_player})")
        
        # Obtenir les coups possibles
        moves = self.game.state.possibleMoves(self.current_player)
        
        if not moves:
            print("❌ Aucun coup possible pour l'IA!")
            return False
        
        # Calculer le meilleur coup avec Minimax Alpha-Beta
        print("🔍 L'IA réfléchit...")
        _, best_pit = minimax_alpha_beta_pruning(
            self.game, 
            MAX, 
            self.search_depth, 
            float('-inf'), 
            float('+inf'),
            heuristic
        )
        
        if best_pit:
            print(f"✅ L'IA choisit le pit: {best_pit}")
            self.game.state.doMove(self.current_player, best_pit)
            return True
        
        return False
    
    def switchPlayer(self):
        """Passe au joueur suivant"""
        self.current_player = 'player2' if self.current_player == 'player1' else 'player1'
    
    def playGame(self):
        """
        Lance une partie complète
        """
        print("=" * 50)
        print("🎮 MANCALA GAME - MODE:", self.game_mode.upper())
        print("=" * 50)
        
        while not self.game.game_over():
            if self.game_mode == 'hvai':
                # Mode Humain vs IA
                if self.current_player == 'player1':
                    success = self.humanTurn()
                else:
                    success = self.computerTurn('balanced')
            else:
                # Mode IA vs IA
                if self.current_player == 'player1':
                    success = self.computerTurn('balanced')
                else:
                    success = self.computerTurn('aggressive')
                
                input("\nAppuyez sur Entrée pour continuer...")
            
            if success:
                self.switchPlayer()
        
        # Afficher le résultat final
        print("\n" + "=" * 50)
        print("🏁 FIN DE LA PARTIE")
        print("=" * 50)
        print(self.game)
        
        winner_info = self.game.find_winner()
        if winner_info['winner'] == 'draw':
            print(f"\n🤝 MATCH NUL! Score: {winner_info['score1']}-{winner_info['score2']}")
        else:
            print(f"\n🏆 GAGNANT: {winner_info['winner'].upper()}")
            print(f"📊 Score: Player1={winner_info['score1']}, Player2={winner_info['score2']}")


if __name__ == "__main__":
    print("\n🎯 Bienvenue dans MANCALA!")
    print("\n1. Humain vs IA")
    print("2. IA vs IA")
    
    choice = input("\nChoisissez le mode (1 ou 2): ")
    
    if choice == '1':
        game = Play(game_mode='hvai', search_depth=6)
    else:
        game = Play(game_mode='aivai', search_depth=6)
    
    game.playGame()