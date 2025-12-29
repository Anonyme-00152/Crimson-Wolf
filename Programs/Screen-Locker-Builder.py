#!/usr/bin/env python3
# Lanceur simple pour village_builder.py

import os
import sys
import subprocess

# Chemin du script à lancer
script_path = "Programs/ScreenLocker-Builder/village_builder.py"

print(f"Lancement de: {script_path}")

# Vérifier si le fichier existe
if not os.path.exists(script_path):
    print(f"ERREUR: Fichier non trouvé: {script_path}")
    print("Création du répertoire...")
    
    # Créer le répertoire si il n'existe pas
    os.makedirs("Programs/ScreenLocker-Builder", exist_ok=True)
    
    # Créer un fichier village_builder.py minimal
    with open(script_path, "w") as f:
        f.write('''#!/usr/bin/env python3
print("=== VILLAGE BUILDER ===")
print("ScreenLocker Builder est lancé!")
print("Ceci est un script placeholder.")
input("Appuyez sur Entrée pour continuer...")
''')
    
    print(f"Fichier créé: {script_path}")

# Lancer le script
try:
    if os.name == 'nt':  # Windows
        subprocess.run(['python', script_path], check=True)
    else:  # Linux/Mac
        # Rendre exécutable si besoin
        os.chmod(script_path, 0o755)
        subprocess.run(['python3', script_path], check=True)
    
    print("Script exécuté avec succès!")
    
except FileNotFoundError:
    print("ERREUR: Python n'est pas installé ou n'est pas dans le PATH")
except subprocess.CalledProcessError as e:
    print(f"ERREUR: Le script a retourné une erreur: {e}")
except Exception as e:
    print(f"ERREUR inattendue: {e}")

# Attendre avant de quitter
if os.name == 'nt':
    os.system("pause")