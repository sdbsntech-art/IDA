import os

adsense_script = '''
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5462969054920766"
     crossorigin="anonymous"></script>
'''

adsense_meta = '<meta name="google-adsense-account" content="ca-pub-3942650991755175">\n'

def add_adsense_to_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Ajoute la balise meta si absente
    if adsense_meta.strip() not in content:
        content = content.replace("</head>", adsense_meta + "</head>")
    # Ajoute le script si absent
    if adsense_script.strip() not in content:
        content = content.replace("</head>", adsense_script + "\n</head>")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Script et meta ajoutés à {file_path}")

# Parcours tous les fichiers HTML du dossier courant
for filename in os.listdir():
    if filename.endswith(".html"):
        add_adsense_to_html(filename)

print("Terminé !")