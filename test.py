"""
Test de l'API Flask
Lancez ce script PENDANT que Flask tourne (dans un autre terminal)
"""

import requests
import json

print("🧪 Test de l'API Flask...")
print("=" * 60)

# Test 1: Créer une nouvelle partie
print("\n1️⃣ Test: Créer une nouvelle partie (POST /api/new_game)")
try:
    response = requests.post(
        'http://localhost:5000/api/new_game',
        json={'mode': 'hvai', 'depth': 6}
    )
    
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Succès!")
        print(f"   Game ID: {data.get('game_id', 'N/A')}")
        print(f"   Mode: {data.get('mode', 'N/A')}")
        print(f"   Board: {data.get('board', 'N/A')}")
        
        game_id = data.get('game_id')
        
        # Test 2: Récupérer l'état
        print("\n2️⃣ Test: Récupérer l'état (GET /api/get_state/<id>)")
        response2 = requests.get(f'http://localhost:5000/api/get_state/{game_id}')
        print(f"   Status Code: {response2.status_code}")
        if response2.status_code == 200:
            print(f"   ✅ État récupéré avec succès!")
        else:
            print(f"   ❌ Erreur: {response2.text}")
        
    else:
        print(f"   ❌ Erreur {response.status_code}")
        print(f"   Réponse: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("   ❌ ERREUR: Impossible de se connecter à Flask!")
    print("   Vérifiez que Flask tourne avec: python app.py")
    
except Exception as e:
    print(f"   ❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)