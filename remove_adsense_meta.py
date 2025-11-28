#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour supprimer la meta tag Google AdSense de tous les fichiers HTML
sauf index.html
"""

import os
import re
from pathlib import Path

def remove_adsense_meta(directory=None):
    """
    Supprime la ligne <meta name="google-adsense-account" content="ca-pub-3942650991755175">
    de tous les fichiers .html sauf index.html
    
    Args:
        directory: Le répertoire à traiter (par défaut: le répertoire courant)
    """
    if directory is None:
        directory = Path(__file__).parent.resolve()
    else:
        directory = Path(directory).resolve()
    
    # Pattern regex pour matcher la ligne complète avec espaces/indentation
    pattern = r'^\s*<meta\s+name\s*=\s*["\']google-adsense-account["\']\s+content\s*=\s*["\']ca-pub-3942650991755175["\']\s*>\s*\n?'
    
    # Lister tous les fichiers .html
    html_files = sorted(directory.glob('*.html'))
    
    if not html_files:
        print(f"❌ Aucun fichier .html trouvé dans {directory}")
        return
    
    modified_count = 0
    skipped_count = 0
    error_count = 0
    
    print(f"📁 Répertoire: {directory}")
    print(f"📄 {len(html_files)} fichier(s) .html trouvé(s)\n")
    
    for html_file in html_files:
        filename = html_file.name
        
        # Ignorer index.html
        if filename.lower() == 'index.html':
            print(f"⏭️  {filename} - IGNORÉ (exception)")
            skipped_count += 1
            continue
        
        try:
            # Lire le fichier
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Chercher et compter les occurrences
            matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
            
            if matches:
                # Supprimer la ligne
                new_content = re.sub(pattern, '', content, flags=re.MULTILINE | re.IGNORECASE)
                
                # Écrire le fichier modifié
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✅ {filename} - MODIFIÉ ({len(matches)} occurrence(s) supprimée(s))")
                modified_count += 1
            else:
                print(f"⏭️  {filename} - AUCUNE META TROUVÉE")
                skipped_count += 1
        
        except Exception as e:
            print(f"❌ {filename} - ERREUR: {e}")
            error_count += 1
    
    # Résumé
    print("\n" + "="*60)
    print(f"📊 RÉSUMÉ")
    print("="*60)
    print(f"✅ Modifiés: {modified_count}")
    print(f"⏭️  Non modifiés: {skipped_count}")
    print(f"❌ Erreurs: {error_count}")
    print(f"📁 Total: {len(html_files)}")


if __name__ == '__main__':
    import sys
    
    # Argument optionnel pour spécifier le répertoire
    target_dir = sys.argv[1] if len(sys.argv) > 1 else None
    
    print("🔍 Suppression de la meta tag Google AdSense...\n")
    remove_adsense_meta(target_dir)
    print("\n✨ Opération terminée!")
