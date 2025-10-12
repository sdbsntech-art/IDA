import os
import re

ASSETS_DIR = "ASSETS"
FILES_DIR = "files"

def find_pdf_path(pdf_name):
    # Cherche le PDF dans ASSETS puis files
    assets_path = os.path.join(ASSETS_DIR, pdf_name)
    files_path = os.path.join(FILES_DIR, pdf_name)
    if os.path.isfile(assets_path):
        return assets_path.replace("\\", "/")
    elif os.path.isfile(files_path):
        return files_path.replace("\\", "/")
    return None

for filename in os.listdir():
    if filename.endswith(".html"):
        with open(filename, encoding="utf-8") as f:
            html = f.read()

        # Trouve tous les liens PDF
        links = re.findall(r'href="([^"]+\.pdf)"', html)
        corrected = html

        for link in links:
            pdf_name = os.path.basename(link)
            correct_path = find_pdf_path(pdf_name)
            if correct_path and link != correct_path:
                corrected = corrected.replace(f'href="{link}"', f'href="{correct_path}"')

        # Sauvegarde si modifié
        if corrected != html:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(corrected)
            print(f"✅ Corrigé : {filename}")

print("Traitement terminé.")