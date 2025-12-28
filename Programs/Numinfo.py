import requests
from bs4 import BeautifulSoup
import time

# Écrire le numéro
numero = input("Entre le numéro de téléphone (format international, ex: +33123456789): ").strip()
print(f"\nLancement de la recherche pour: {numero}")
print("Scraping des sources publiques...\n")
time.sleep(1)

def scraper_source_1(num):
    # Source publique fictive exemple 1
    url = f"https://www.annuaires-inverse.com/numero/{num}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        nom = soup.find('h1', {'class': 'name'})
        return nom.text.strip() if nom else "Aucun résultat (Source 1)"
    except:
        return "Source inaccessible (Source 1)"

def scraper_source_2(num):
    # Source publique fictive exemple 2
    url = f"https://www.tel-search.fr/{num}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        div = soup.find('div', {'id': 'result'})
        return div.text.strip() if div else "Aucun résultat (Source 2)"
    except:
        return "Source inaccessible (Source 2)"

def scraper_source_3(num):
    # Scrap Google search (très basique)
    url = f"https://www.google.com/search?q={num}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        # Cherche un résultat commun
        for texte in soup.find_all('span'):
            if num.replace('+', '') in texte.text:
                return texte.text[:100]
        return "Aucune mention trouvée (Google)"
    except:
        return "Google inaccessible"

# Exécution des scrapers
print("=== RÉSULTATS ===")
print(f"Source 1 (Annuaire inversé): {scraper_source_1(numero)}")
print(f"Source 2 (Tel-search): {scraper_source_2(numero)}")
print(f"Source 3 (Moteur de recherche): {scraper_source_3(numero)}")
print("\nRecherche terminée.")