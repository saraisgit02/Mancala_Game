"""
Programme Principal - Version Console
Auteur: Projet 4 - Problem Solving
Master 1, Visual Computing - USTHB
"""

from play import Play
import os


def clear_screen():
    """Nettoie l'écran du terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    """Affiche la bannière du jeu"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║                     🎮  M A N C A L A  🎮                     ║
    ║                                                               ║
    ║                  Jeu Stratégique Africain                     ║
    ║                    (Awelé / Kalaha / Oware)                   ║
    ║                                                               ║
    ║              Algorithme: Minimax Alpha-Beta Pruning           ║
    ║                     Profondeur: 6 niveaux                     ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def display_menu():
    """Affiche le menu principal"""
    print("\n" + "="*60)
    print("                       MENU PRINCIPAL")
    print("="*60)
    print("\n  1. 🎮 Humain vs IA")
    print("  2. 🤖 IA vs IA (Simulation)")
    print("  3. ℹ️  Règles du jeu")
    print("  4. 🚪 Quitter")
    print("\n" + "="*60)


def display_rules():
    """Affiche les règles du jeu"""
    clear_screen()
    print("\n" + "="*60)
    print("                      RÈGLES DU MANCALA")
    print("="*60)
    print("""
📋 OBJECTIF:
   Capturer plus de graines que votre adversaire

🎯 RÈGLES:
   1. Chaque joueur choisit un pit de son côté contenant des graines
   2. Les graines sont distribuées une par une dans le sens anti-horaire
   3. On peut placer une graine dans son propre store, mais pas dans
      celui de l'adversaire
   4. Si la dernière graine tombe dans un pit vide de votre côté,
      vous capturez cette graine + toutes les graines du pit opposé
   5. Le jeu se termine quand tous les pits d'un joueur sont vides
   6. Le joueur avec le plus de graines dans son store gagne

📊 NOTATION:
   - Pits Joueur 1: A, B, C, D, E, F
   - Pits Joueur 2: G, H, I, J, K, L
   - Store Joueur 1: 1
   - Store Joueur 2: 2

🤖 IA:
   - Utilise l'algorithme Minimax avec élagage Alpha-Beta
   - Profondeur de recherche: 6 niveaux
   - Deux heuristiques différentes pour le mode IA vs IA
    """)
    print("="*60)
    input("\nAppuyez sur Entrée pour revenir au menu...")


def select_difficulty():
    """Permet de choisir le niveau de difficulté"""
    print("\n" + "="*60)
    print("                  NIVEAU DE DIFFICULTÉ")
    print("="*60)
    print("\n  1. 😊 Facile    (Profondeur: 3)")
    print("  2. 😐 Moyen     (Profondeur: 5)")
    print("  3. 😤 Difficile (Profondeur: 6)")
    print("  4. 😈 Expert    (Profondeur: 8)")
    print("\n" + "="*60)
    
    while True:
        choice = input("\nChoisissez le niveau (1-4): ").strip()
        if choice == '1':
            return 3
        elif choice == '2':
            return 5
        elif choice == '3':
            return 6
        elif choice == '4':
            return 8
        else:
            print("❌ Choix invalide! Veuillez choisir entre 1 et 4.")


def main():
    """Fonction principale du programme"""
    while True:
        clear_screen()
        print_banner()
        display_menu()
        
        choice = input("\n👉 Votre choix: ").strip()
        
        if choice == '1':
            # Mode Humain vs IA
            clear_screen()
            print_banner()
            depth = select_difficulty()
            clear_screen()
            print_banner()
            print("\n🎮 Mode: HUMAIN vs IA")
            print(f"⚙️  Niveau de difficulté: Profondeur {depth}")
            input("\nAppuyez sur Entrée pour commencer...")
            
            game = Play(game_mode='hvai', search_depth=depth)
            game.playGame()
            
            input("\n\nAppuyez sur Entrée pour revenir au menu...")
        
        elif choice == '2':
            # Mode IA vs IA
            clear_screen()
            print_banner()
            print("\n🤖 Mode: IA vs IA (Simulation)")
            print("⚙️  Profondeur de recherche: 6 niveaux")
            print("\n📊 Heuristiques:")
            print("   - IA 1 (Joueur 1): Heuristique équilibrée")
            print("   - IA 2 (Joueur 2): Heuristique agressive")
            input("\nAppuyez sur Entrée pour lancer la simulation...")
            
            game = Play(game_mode='aivai', search_depth=6)
            game.playGame()
            
            input("\n\nAppuyez sur Entrée pour revenir au menu...")
        
        elif choice == '3':
            # Afficher les règles
            display_rules()
        
        elif choice == '4':
            # Quitter
            clear_screen()
            print("\n" + "="*60)
            print("          Merci d'avoir joué à MANCALA! 🎮")
            print("              À bientôt! 👋")
            print("="*60 + "\n")
            break
        
        else:
            print("\n❌ Choix invalide! Veuillez choisir entre 1 et 4.")
            input("\nAppuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("\n\n" + "="*60)
        print("          Programme interrompu par l'utilisateur")
        print("              À bientôt! 👋")
        print("="*60 + "\n")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        input("\nAppuyez sur Entrée pour quitter...")