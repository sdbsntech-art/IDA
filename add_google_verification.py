import os
import re

# Configuration
verification_code = "8WaeKM-mQAcuLhGP1eHzoO1Gr0IX9lq_NoNGavj0fB8"
site_url = "https://sdbsn-code.netlify.app/"
og_image = "https://sdbsn-code.netlify.app/ASSETS/téléchargement%20(2).jpg"

meta_verification = f'<meta name="google-site-verification" content="{verification_code}" />\n'

def update_html_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Ajoute la balise juste avant <title>
    if f'google-site-verification' not in content:
        content = re.sub(r'(<title>)', meta_verification + r'\1', content, flags=re.IGNORECASE)

    # Met à jour og:url et og:image si présents
    content = re.sub(r'(<meta property="og:url" content=")[^"]*(")', rf'\1{site_url}\2', content)
    content = re.sub(r'(<meta property="og:image" content=")[^"]*(")', rf'\1{og_image}\2', content)
    content = re.sub(r'(<meta name="twitter:image" content=")[^"]*(")', rf'\1{og_image}\2', content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

# Parcours tous les fichiers HTML du dossier courant
for filename in os.listdir():
    if filename.endswith(".html"):
        update_html_file(filename)
        print(f"✅ Balise ajoutée dans {filename}")

print("Terminé !")