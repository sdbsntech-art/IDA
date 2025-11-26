import os
import sys
import shutil
import base64
from pathlib import Path

def create_icons_without_pillow(base_dir, source_image_path=None):
    """
    Crée la structure d'icônes sans dépendances externes
    """
    icons_dir = os.path.join(base_dir, "icons")
    os.makedirs(icons_dir, exist_ok=True)
    
    # Tailles d'icônes requises
    icon_sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    
    if source_image_path and os.path.exists(source_image_path):
        print(f"📁 Copie de l'image source comme icône principale...")
        # Copie l'image source comme icône 512x512 (la plus grande)
        try:
            shutil.copy2(source_image_path, os.path.join(icons_dir, "icon-512x512.png"))
            print("✅ Image source copiée comme icon-512x512.png")
        except Exception as e:
            print(f"❌ Erreur lors de la copie: {e}")
    
    # Crée un fichier README avec instructions
    create_icon_readme(icons_dir, icon_sizes)
    
    # Crée un script batch pour conversion facile
    create_conversion_script(icons_dir, source_image_path)

def create_icon_readme(icons_dir, sizes):
    """Crée un fichier README détaillé"""
    readme_content = f"""# ICÔNES PWA - SDBSN Code

## 📋 ICÔNES MANQUANTES

Les icônes suivantes doivent être créées dans le dossier '{icons_dir}':

{chr(10).join(f'- icon-{size}x{size}.png' for size in sizes)}

## 🛠️ SOLUTIONS RAPIDES

### Option 1: Convertisseur en ligne (Recommandé)
1. Allez sur: https://www.favicon-generator.org/
2. Téléchargez votre image
3. Téléchargez le pack d'icônes généré
4. Copiez les fichiers PNG dans ce dossier

### Option 2: Outils gratuits
- https://realfavicongenerator.net/
- https://www.favicon.cc/
- https://favicon.io/

### Option 3: Avec Paint (Windows)
1. Ouvrez votre image dans Paint
2. Cliquez sur "Redimensionner"
3. Décochez "Conserver les proportions" 
4. Mettez {sizes[0]} x {sizes[0]} (pour la première taille)
5. Sauvegardez comme "icon-{sizes[0]}x{sizes[0]}.png"
6. Répétez pour chaque taille

## 📁 STRUCTURE REQUISE
