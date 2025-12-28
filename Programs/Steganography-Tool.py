"""
ExeImageHider - Cacher un EXE derrière une image
"""

import os
import sys
import struct

def main():
    print("╔══════════════════════════════════════════╗")
    print("║         EXE in Image Hider v1.0         ║")
    print("╚══════════════════════════════════════════╝")
    print("\n[+] Cette technique cache un EXE derrière une image")
    print("[+] L'image reste fonctionnelle, l'EXE est invisible")
    
    try:
        # 1. Demander l'image
        while True:
            image = input("\n[?] Chemin de l'image (.jpg/.png) -> ").strip()
            if os.path.exists(image):
                break
            print("[!] Fichier introuvable!")
        
        # 2. Demander l'EXE
        while True:
            exe = input("[?] Chemin du fichier EXE -> ").strip()
            if os.path.exists(exe):
                if exe.lower().endswith('.exe'):
                    break
                else:
                    print("[!] Ce n'est pas un fichier .exe!")
            else:
                print("[!] Fichier introuvable!")
        
        # 3. Nom de sortie
        output = input("[?] Nom du fichier de sortie (ENTER pour 'output.exe') -> ").strip()
        if not output:
            output = "output.exe"
        
        # 4. Lire les fichiers
        print("\n[~] Lecture des fichiers...")
        with open(image, 'rb') as f:
            image_data = f.read()
        
        with open(exe, 'rb') as f:
            exe_data = f.read()
        
        # 5. Créer un header simple
        header = struct.pack('16s Q', b'EXEHIDDENv1.0', len(exe_data))
        
        # 6. Combiner : EXE + Header + Image
        print("[~] Combinaison des données...")
        combined_data = exe_data + header + image_data
        
        # 7. Sauvegarder
        with open(output, 'wb') as f:
            f.write(combined_data)
        
        # 8. Afficher les résultats
        print(f"\n[✓] Fichier créé avec succès!")
        print(f"    Image source: {image}")
        print(f"    EXE caché: {exe}")
        print(f"    Fichier final: {output}")
        print(f"    Taille: {os.path.getsize(output):,} octets")
        
        # 9. Chemin complet
        full_path = os.path.abspath(output)
        print(f"    Emplacement: {full_path}")
        
        # 10. Créer un extracteur
        create_extractor = input("\n[?] Créer un extracteur automatique? (o/n) -> ").strip().lower()
        if create_extractor in ['o', 'oui', 'y', 'yes']:
            extractor_code = f'''#!/usr/bin/env python3
import os
import struct
import sys
import subprocess
import tempfile

def extract_exe_from_image(image_file):
    with open(image_file, 'rb') as f:
        # Aller à la fin - taille du header (24 octets)
        f.seek(-24, 2)
        header = f.read(24)
        magic, exe_size = struct.unpack('16s Q', header)
        
        if magic != b'EXEHIDDENv1.0':
            print("Ce fichier ne contient pas d'EXE caché")
            return None
        
        # Aller au début de l'EXE
        f.seek(0)
        exe_data = f.read(exe_size)
        
        # Créer un fichier temporaire
        temp_dir = tempfile.gettempdir()
        temp_exe = os.path.join(temp_dir, "extracted_program.exe")
        
        with open(temp_exe, 'wb') as exe_file:
            exe_file.write(exe_data)
        
        return temp_exe

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extractor.py <fichier_image_avec_exe>")
        sys.exit(1)
    
    image_file = sys.argv[1]
    
    if not os.path.exists(image_file):
        print("Fichier introuvable!")
        sys.exit(1)
    
    extracted_exe = extract_exe_from_image(image_file)
    
    if extracted_exe:
        print(f"EXE extrait: {extracted_exe}")
        print("Exécution...")
        subprocess.run([extracted_exe])
'''
            
            extractor_name = "extract_exe.py"
            with open(extractor_name, 'w', encoding='utf-8') as f:
                f.write(extractor_code)
            
            print(f"\n[✓] Extracteur créé: {extractor_name}")
            print(f"    Pour extraire et exécuter: python {extractor_name} {output}")
        
        # 11. Instructions
        print("\n" + "═"*50)
        print("📋 INSTRUCTIONS:")
        print("═"*50)
        print("1. Le fichier", output, "est à la fois:")
        print("   - Une image valide (ouvrable avec tout visionneur)")
        print("   - Un EXE caché (exécutable)")
        print("\n2. Pour exécuter l'EXE caché:")
        print("   Méthode A: Renommez en .exe et exécutez")
        print("   Méthode B: Utilisez l'extracteur Python")
        print("\n3. Pour cacher dans d'autres formats:")
        print("   Renommez simplement le fichier en .jpg, .png, etc.")
        
        input("\n[ENTER] Pour quitter...")
        
    except Exception as e:
        print(f"\n[!] Erreur: {e}")
        input("[ENTER] Pour quitter...")

if __name__ == "__main__":
    main()