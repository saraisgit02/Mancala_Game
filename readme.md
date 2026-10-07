

## 📋 Description du Projet

Implémentation complète du jeu **Mancala** (aussi connu sous le nom d'Awelé ou Oware) avec un algorithme de recherche adversariale utilisant **Minimax avec élagage Alpha-Beta**.

Le projet comprend :
- ✅ Architecture modulaire et POO
- ✅ Algorithme Minimax Alpha-Beta conforme aux spécifications
- ✅ Deux heuristiques différentes pour le mode IA vs IA
- ✅ Interface console complète et interactive
- ✅ Interface graphique web moderne et esthétique
- ✅ Mode Humain vs IA et IA vs IA

---

## 🗂️ Structure du Projet

```
mancala_project/
│
├── mancala_board.py       # Classe MancalaBoard (état du plateau)
├── game.py                # Classe Game (nœud de recherche)
├── minimax.py             # Algorithme Minimax Alpha-Beta
├── play.py                # Classe Play (gestion des tours)
├── main.py                # Programme principal (console)
├── gui.html               # Interface graphique (React)
└── README.md              # Documentation
```

---

## 🎯 Fonctionnalités

### 1. **Architecture Modulaire**

#### `mancala_board.py`
```python
class MancalaBoard:
    - board: dict               # État du plateau (A-F, G-L, 1, 2)
    - player1Pits: tuple        # Pits du joueur 1
    - player2Pits: tuple        # Pits du joueur 2
    - oppositePits: dict        # Correspondance des pits opposés
    - nextPit: dict             # Séquence anti-horaire
    
    - possibleMoves(player)     # Retourne les coups possibles
    - doMove(player, pit)       # Exécute un mouvement
    - copy()                    # Copie profonde du plateau
```

#### `game.py`
```python
class Game:
    - state: MancalaBoard       # État du jeu
    - playerSide: dict          # {'HUMAN': '1'/'2', 'COMPUTER': '1'/'2'}
    
    - gameOver()                # Vérifie la fin du jeu
    - findWinner()              # Détermine le gagnant
    - evaluate()                # Heuristique équilibrée
    - evaluateAggressive()      # Heuristique agressive
    - copy()                    # Copie profonde du jeu
```

#### `minimax.py`
```python
def MinimaxAlphaBetaPruning(game, player, depth, alpha, beta, heuristic):
    """
    Algorithme Minimax avec élagage Alpha-Beta
    
    Paramètres:
        - game: Instance de Game
        - player: MAX (1) ou MIN (-1)
        - depth: Profondeur de recherche
        - alpha: Meilleure valeur pour MAX
        - beta: Meilleure valeur pour MIN
        - heuristic: 'balanced' ou 'aggressive'
    
    Retour:
        - (bestValue, bestPit): Meilleure évaluation et meilleur coup
    """
```

#### `play.py`
```python
class Play:
    - game: Game                # Instance du jeu
    - game_mode: str            # 'hvai' ou 'aivai'
    - search_depth: int         # Profondeur de recherche
    - current_player: str       # 'player1' ou 'player2'
    
    - humanTurn()               # Tour du joueur humain
    - computerTurn(heuristic)   # Tour de l'IA
    - playGame()                # Lance une partie complète
```

### 2. **Heuristiques**

#### Heuristique Équilibrée
```python
def evaluate(self):
    return store_computer - store_human
```
- Simple et efficace
- Favorise l'accumulation dans le store

#### Heuristique Agressive
```python
def evaluateAggressive(self):
    return (store_computer - store_human) * 2 + seeds_in_pits
```
- Plus agressive
- Prend en compte les graines encore en jeu
- Favorise les positions offensives

### 3. **Modes de Jeu**

#### Mode Humain vs IA
- Le joueur choisit ses coups en entrant la lettre du pit
- L'IA utilise Minimax Alpha-Beta (heuristique équilibrée)
- Profondeur de recherche réglable (3, 5, 6, 8)

#### Mode IA vs IA (Simulation)
- IA 1 (Joueur 1) : Heuristique équilibrée
- IA 2 (Joueur 2) : Heuristique agressive
- Permet d'observer les différentes stratégies

---

## 🚀 Installation et Utilisation

### **Version Console**

```bash
# Lancer le jeu
python main.py
```

### **Version Graphique**

1. Ouvrir `gui.html` dans un navigateur moderne
2. Ou intégrer le code React dans votre projet

---

## 🎮 Règles du Jeu

### Objectif
Capturer plus de graines que votre adversaire.

### Déroulement
1. Chaque joueur choisit un pit de son côté contenant des graines
2. Les graines sont distribuées une par une dans le sens **anti-horaire**
3. On peut placer une graine dans son propre **store**, mais **pas** dans celui de l'adversaire
4. **Règle de capture** : Si la dernière graine tombe dans un pit vide de votre côté, vous capturez cette graine + toutes les graines du pit opposé
5. Le jeu se termine quand tous les pits d'un joueur sont vides
6. Le joueur avec le plus de graines dans son store gagne

### Notation
- **Pits Joueur 1** : A, B, C, D, E, F
- **Pits Joueur 2** : G, H, I, J, K, L
- **Store Joueur 1** : 1
- **Store Joueur 2** : 2

---

## 🧠 Algorithme Minimax Alpha-Beta

### Principe
L'algorithme explore l'arbre de jeu en alternant entre :
- **MAX** (ordinateur) : maximise l'évaluation
- **MIN** (adversaire) : minimise l'évaluation

### Élagage Alpha-Beta
- **Alpha** : Meilleure valeur garantie pour MAX
- **Beta** : Meilleure valeur garantie pour MIN
- Coupe les branches qui ne peuvent pas influencer la décision finale

### Complexité
- Sans élagage : O(b^d)
- Avec élagage : O(b^(d/2)) en moyenne
- Où b = facteur de branchement, d = profondeur

### Implémentation
```python
if player == MAX:
    bestValue = -∞
    for each move:
        value = MinimaxAlphaBeta(child, MIN, depth-1, α, β)
        bestValue = max(bestValue, value)
        if bestValue >= β:  # Élagage Beta
            break
        α = max(α, bestValue)
else:
    bestValue = +∞
    for each move:
        value = MinimaxAlphaBeta(child, MAX, depth-1, α, β)
        bestValue = min(bestValue, value)
        if bestValue <= α:  # Élagage Alpha
            break
        β = min(β, bestValue)
```

---

## 📊 Performances

### Profondeur de Recherche
- **Profondeur 3** : Facile (~100 nœuds explorés)
- **Profondeur 5** : Moyen (~1000 nœuds explorés)
- **Profondeur 6** : Difficile (~5000 nœuds explorés)
- **Profondeur 8** : Expert (~20000 nœuds explorés)

### Temps de Calcul (approximatif)
- Profondeur 3 : < 0.1s
- Profondeur 5 : 0.5-1s
- Profondeur 6 : 1-3s
- Profondeur 8 : 5-15s

---


### Technologies
- **React** pour l'interactivité
- **Tailwind CSS** pour le style
- **Lucide React** pour les icônes
- **Animations CSS** personnalisées

---

## 🧪 Exemples d'Utilisation

### Console
```python
from play import Play

# Mode Humain vs IA (profondeur 6)
game = Play(game_mode='hvai', search_depth=6)
game.playGame()

# Mode IA vs IA
game = Play(game_mode='aivai', search_depth=6)
game.playGame()
```

### Accès Direct aux Classes
```python
from mancala_board import MancalaBoard
from game import Game
from minimax import MinimaxAlphaBetaPruning, MAX

# Créer un jeu
player_side = {'HUMAN': '1', 'COMPUTER': '2'}
game = Game(player_side)

# Trouver le meilleur coup
best_value, best_pit = MinimaxAlphaBetaPruning(
    game, MAX, depth=6, alpha=float('-inf'), beta=float('+inf')
)

print(f"Meilleur coup: {best_pit}, Évaluation: {best_value}")
```






---


