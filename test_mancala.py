"""
Script de Test Complet pour le Projet Mancala
Teste toutes les fonctionnalités et détecte les erreurs
"""

import sys
import traceback

def print_section(title):
    """Affiche un titre de section"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_imports():
    """Test 1: Vérifier que tous les modules peuvent être importés"""
    print_section("TEST 1: IMPORTS")
    
    try:
        from mancala_board import MancalaBoard
        print("✅ mancala_board.py importé avec succès")
    except Exception as e:
        print(f"❌ Erreur import mancala_board.py: {e}")
        return False
    
    try:
        from game import Game
        print("✅ game.py importé avec succès")
    except Exception as e:
        print(f"❌ Erreur import game.py: {e}")
        return False
    
    try:
        from minimax import minimax_alpha_beta_pruning, MAX, MIN
        print("✅ minimax.py importé avec succès")
    except Exception as e:
        print(f"❌ Erreur import minimax.py: {e}")
        return False
    
    try:
        from play import Play
        print("✅ play.py importé avec succès")
    except Exception as e:
        print(f"❌ Erreur import play.py: {e}")
        return False
    
    return True

def test_mancala_board():
    """Test 2: Tester la classe MancalaBoard"""
    print_section("TEST 2: MANCALA BOARD")
    
    try:
        from mancala_board import MancalaBoard
        
        # Création d'un board
        board = MancalaBoard()
        print("✅ MancalaBoard créé")
        
        # Vérifier l'état initial
        assert board.board['A'] == 4, "Pit A devrait avoir 4 graines"
        assert board.board['1'] == 0, "Store 1 devrait être vide"
        print("✅ État initial correct")
        
        # Tester possibleMoves
        moves = board.possibleMoves('player1')
        assert len(moves) == 6, "Player1 devrait avoir 6 coups possibles"
        assert 'A' in moves, "A devrait être dans les coups possibles"
        print(f"✅ Coups possibles player1: {moves}")
        
        # Tester doMove
        board.doMove('player1', 'A')
        assert board.board['A'] == 0, "Pit A devrait être vide après le coup"
        assert board.board['B'] == 5, "Pit B devrait avoir 5 graines"
        print("✅ doMove fonctionne correctement")
        
        # Tester la copie
        board2 = board.copy()
        board2.board['C'] = 10
        assert board.board['C'] != 10, "La copie devrait être indépendante"
        print("✅ copy() fonctionne correctement")
        
        # Afficher le board
        print("\nAffichage du board:")
        print(board)
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans MancalaBoard: {e}")
        traceback.print_exc()
        return False

def test_game():
    """Test 3: Tester la classe Game"""
    print_section("TEST 3: GAME CLASS")
    
    try:
        from game import Game
        
        # Création d'un jeu
        player_side = {'HUMAN': 'player1', 'COMPUTER': 'player2'}
        game = Game(player_side=player_side)
        print("✅ Game créé")
        
        # Tester game_over
        assert not game.game_over(), "Le jeu ne devrait pas être terminé au début"
        print("✅ game_over() fonctionne")
        
        # Tester evaluate
        eval_score = game.evaluate()
        print(f"✅ evaluate() retourne: {eval_score}")
        
        # Tester evaluate_aggressive
        eval_aggressive = game.evaluate_aggressive()
        print(f"✅ evaluate_aggressive() retourne: {eval_aggressive}")
        
        # Tester copy
        game2 = game.copy()
        game2.state.board['A'] = 10
        assert game.state.board['A'] != 10, "La copie devrait être indépendante"
        print("✅ copy() fonctionne")
        
        # Simuler une fin de partie
        for pit in game.state.player1Pits:
            game.state.board[pit] = 0
        assert game.game_over(), "Le jeu devrait être terminé"
        print("✅ Détection de fin de partie fonctionne")
        
        # Tester find_winner
        winner = game.find_winner()
        print(f"✅ find_winner() retourne: {winner}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans Game: {e}")
        traceback.print_exc()
        return False

def test_minimax():
    """Test 4: Tester l'algorithme Minimax"""
    print_section("TEST 4: MINIMAX ALPHA-BETA")
    
    try:
        from game import Game
        from minimax import minimax_alpha_beta_pruning, MAX
        
        player_side = {'HUMAN': 'player1', 'COMPUTER': 'player2'}
        game = Game(player_side=player_side)
        
        # Test avec heuristique balanced
        print("\nTest avec heuristique BALANCED (profondeur 3)...")
        value, pit = minimax_alpha_beta_pruning(
            game, MAX, depth=3, 
            alpha=float('-inf'), 
            beta=float('inf'),
            heuristic='balanced'
        )
        print(f"✅ Balanced - Meilleur coup: {pit}, Évaluation: {value}")
        
        # Test avec heuristique aggressive
        print("\nTest avec heuristique AGGRESSIVE (profondeur 3)...")
        value2, pit2 = minimax_alpha_beta_pruning(
            game, MAX, depth=3, 
            alpha=float('-inf'), 
            beta=float('inf'),
            heuristic='aggressive'
        )
        print(f"✅ Aggressive - Meilleur coup: {pit2}, Évaluation: {value2}")
        
        # Vérifier que les deux heuristiques donnent des résultats
        assert pit is not None, "Balanced devrait retourner un coup"
        assert pit2 is not None, "Aggressive devrait retourner un coup"
        print("\n✅ Les deux heuristiques fonctionnent!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans Minimax: {e}")
        traceback.print_exc()
        return False

def test_play():
    """Test 5: Tester la classe Play"""
    print_section("TEST 5: PLAY CLASS")
    
    try:
        from play import Play
        
        # Créer une instance en mode hvai
        play_hvai = Play(game_mode='hvai', search_depth=3)
        print("✅ Play créé en mode hvai")
        
        # Créer une instance en mode aivai
        play_aivai = Play(game_mode='aivai', search_depth=3)
        print("✅ Play créé en mode aivai")
        
        # Tester computerTurn avec balanced
        print("\nTest computerTurn avec heuristique balanced...")
        success = play_hvai.computerTurn('balanced')
        if success:
            print("✅ computerTurn(balanced) fonctionne")
        
        # Tester computerTurn avec aggressive
        print("\nTest computerTurn avec heuristique aggressive...")
        success = play_aivai.computerTurn('aggressive')
        if success:
            print("✅ computerTurn(aggressive) fonctionne")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans Play: {e}")
        traceback.print_exc()
        return False

def test_flask_imports():
    """Test 6: Vérifier que Flask peut charger l'app"""
    print_section("TEST 6: FLASK APP")
    
    try:
        # Essayer d'importer l'app Flask
        import app
        print("✅ app.py importé avec succès")
        
        # Vérifier que l'app Flask existe
        assert hasattr(app, 'app'), "app.py devrait contenir une variable 'app'"
        print("✅ Variable Flask 'app' trouvée")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans Flask app: {e}")
        traceback.print_exc()
        return False

def run_simulation():
    """Test 7: Simuler une partie complète IA vs IA"""
    print_section("TEST 7: SIMULATION COMPLETE (3 tours)")
    
    try:
        from game import Game
        from minimax import minimax_alpha_beta_pruning, MAX
        
        player_side = {'COMPUTER': 'player1', 'HUMAN': 'player2'}
        game = Game(player_side=player_side)
        
        print("\n🎮 Début de la simulation...")
        print(game)
        
        for turn in range(1, 4):  # 3 tours seulement pour le test
            if game.game_over():
                break
            
            current_player = 'player1' if turn % 2 == 1 else 'player2'
            heuristic = 'balanced' if current_player == 'player1' else 'aggressive'
            
            print(f"\n--- Tour {turn} : {current_player} ({heuristic}) ---")
            
            value, pit = minimax_alpha_beta_pruning(
                game, MAX, depth=3, 
                alpha=float('-inf'), 
                beta=float('inf'),
                heuristic=heuristic
            )
            
            if pit:
                print(f"Coup joué: {pit}, Évaluation: {value}")
                game.state.doMove(current_player, pit)
                print(game)
            else:
                print("Aucun coup possible")
                break
        
        print("\n✅ Simulation terminée avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans la simulation: {e}")
        traceback.print_exc()
        return False

def main():
    """Fonction principale - Lance tous les tests"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "SCRIPT DE TEST MANCALA" + " " * 30 + "║")
    print("╚" + "=" * 68 + "╝")
    
    tests = [
        ("Imports", test_imports),
        ("MancalaBoard", test_mancala_board),
        ("Game", test_game),
        ("Minimax", test_minimax),
        ("Play", test_play),
        ("Flask", test_flask_imports),
        ("Simulation", run_simulation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ ERREUR CRITIQUE dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé final
    print_section("RÉSUMÉ DES TESTS")
    
    total = len(results)
    passed = sum(1 for _, success in results if success)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}  {test_name}")
    
    print("\n" + "=" * 70)
    print(f"Résultat: {passed}/{total} tests réussis ({passed*100//total}%)")
    print("=" * 70)
    
    if passed == total:
        print("\n🎉 FÉLICITATIONS! Tous les tests sont passés!")
        print("Votre projet est prêt à être utilisé.")
    else:
        print("\n⚠️  Certains tests ont échoué.")
        print("Vérifiez les erreurs ci-dessus et corrigez votre code.")
    
    print("\n")

if __name__ == "__main__":
    main()