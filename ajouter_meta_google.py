import os

def ajouter_meta_simple(dossier):
    """Version simplifiée pour un usage rapide"""
    
    meta_tag = '<meta name="google-site-verification" content="7OCwSNaLeEeHm82sAVrKzi0jWCevcYh-05eiK_bEDfg" />'
    
    for racine, dossiers, fichiers in os.walk(dossier):
        for fichier in fichiers:
            if fichier.endswith('.html'):
                chemin = os.path.join(racine, fichier)
                
                try:
                    with open(chemin, 'r', encoding='utf-8') as f:
                        contenu = f.read()
                    
                    if 'google-site-verification' not in contenu:
                        nouveau = contenu.replace('<head>', f'<head>\n    {meta_tag}')
                        
                        if nouveau != contenu:
                            with open(chemin, 'w', encoding='utf-8') as f:
                                f.write(nouveau)
                            print(f"✅ {chemin}")
                        else:
                            print(f"❌ <head> non trouvé dans {chemin}")
                            
                except Exception as e:
                    print(f"❌ Erreur: {chemin} - {e}")

# Utilisation
dossier = "."  # Dossier courant, ou remplacez par votre chemin
ajouter_meta_simple(dossier)