import os
import re

def remove_lien_utiles_from_html(directory):
    pattern = re.compile(
        r'<li><a href="https://grafikart\.fr/tutoriels/variables-441#autoplay"><i class="fas fa-user-graduate"></i>Liens-utiles</a></li>\s*',
        re.MULTILINE
    )
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                new_content = pattern.sub("", content)
                if new_content != content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"✅ Lien supprimé dans {path}")

# Utilisation
remove_lien_utiles_from_html(".")