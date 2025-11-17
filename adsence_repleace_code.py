import os
import re
import shutil
from datetime import datetime

def remplacer_adsense_complet(repertoire):
    """
    Version complète avec détection de multiples patterns AdSense
    """
    nouveau_adsense = '''<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3830476419469874"
     crossorigin="anonymous"></script>'''
    
    # Patterns pour détecter différents formats d'AdSense
    patterns_adsense = [
        r'<script[^>]*adsbygoogle[^>]*>.*?</script>',
        r'<script[^>]*googlesyndication[^>]*>.*?</script>',
        r'<script[^>]*pagead2[^>]*>.*?</script>',
        r'<script[^>]*ca-pub-[^>]*>.*?</script>'
    ]
    
    # Créer le dossier de sauvegarde
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(repertoire, f"backup_adsense_{timestamp}")
    os.makedirs(backup_dir)
    
    stats = {'traites': 0, 'remplaces': 0, 'ajoutes': 0, 'erreurs': 0}
    
    for fichier in os.listdir(repertoire):
        if not fichier.endswith('.html'):
            continue
            
        chemin_original = os.path.join(repertoire, fichier)
        chemin_backup = os.path.join(backup_dir, fichier)
        
        try:
            # SAUVEGARDE AUTOMATIQUE
            shutil.copy2(chemin_original, chemin_backup)
            
            with open(chemin_original, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            stats['traites'] += 1
            modification_faite = False
            nouveau_contenu = contenu
            
            # Chercher et remplacer TOUS les AdSense trouvés
            for pattern in patterns_adsense:
                if re.search(pattern, nouveau_contenu, re.IGNORECASE | re.DOTALL):
                    nouveau_contenu = re.sub(pattern, nouveau_adsense, nouveau_contenu, flags=re.IGNORECASE | re.DOTALL)
                    modification_faite = True
            
            if modification_faite:
                with open(chemin_original, 'w', encoding='utf-8') as f:
                    f.write(nouveau_contenu)
                print(f"🔄 REMPLACÉ : {fichier}")
                stats['remplaces'] += 1
            else:
                # Ajouter si pas trouvé
                head_match = re.search(r'<head[^>]*>', nouveau_contenu, re.IGNORECASE)
                if head_match:
                    position = head_match.end()
                    nouveau_contenu = nouveau_contenu[:position] + '\n    ' + nouveau_adsense + '\n' + nouveau_contenu[position:]
                    
                    with open(chemin_original, 'w', encoding='utf-8') as f:
                        f.write(nouveau_contenu)
                    
                    print(f"✅ AJOUTÉ : {fichier}")
                    stats['ajoutes'] += 1
                else:
                    print(f"❌ PAS DE HEAD : {fichier}")
                    stats['erreurs'] += 1
                    
        except Exception as e:
            print(f"❌ ERREUR : {fichier} - {e}")
            stats['erreurs'] += 1
    
    # Rapport final
    print(f"\n📊 RAPPORT : {stats['traites']} fichiers traités")
    print(f"💾 Sauvegarde : {backup_dir}")
    print(f"🔄 Remplacés : {stats['remplaces']} | ✅ Ajoutés : {stats['ajoutes']} | ❌ Erreurs : {stats['erreurs']}")

if __name__ == "__main__":
    repertoire = input("Chemin du répertoire HTML : ").strip()
    if os.path.isdir(repertoire):
        remplacer_adsense_complet(repertoire)
    else:
        print("❌ Répertoire invalide")