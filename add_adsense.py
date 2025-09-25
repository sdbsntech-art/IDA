import os

adsense_script = '''
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5462969054920766"
     crossorigin="anonymous"></script>
'''

def add_adsense_to_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Vérifie si le script est déjà présent
    if adsense_script.strip() in content:
        return
    # Ajoute le script juste avant </head>
    new_content = content.replace("</head>", adsense_script + "\n</head>")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"✅ Script ajouté à {file_path}")

# Parcours tous les fichiers HTML du dossier courant
for filename in os.listdir():
    if filename.endswith(".html"):
        add_adsense_to_html(filename)

print("Terminé !")
os.system('python add_adsense.py')