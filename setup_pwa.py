import os
import json
import shutil
from pathlib import Path

def create_pwa_files(base_dir):
    """Crée tous les fichiers nécessaires pour la PWA"""
    
    # Création du répertoire pour les icônes
    icons_dir = os.path.join(base_dir, "icons")
    os.makedirs(icons_dir, exist_ok=True)
    
    # 1. Création du manifest.json
    manifest_content = {
        "name": "SDBSN Code",
        "short_name": "SDBSN",
        "description": "Application SDBSN Code",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#000000",
        "orientation": "any",
        "icons": [
            {
                "src": "icons/icon-72x72.jpg",
                "sizes": "72x72",
                "type": "image/jpeg"
            },
            {
                "src": "icons/icon-96x96.jpg",
                "sizes": "96x96",
                "type": "image/jpeg"
            },
            {
                "src": "icons/icon-128x128.jpg",
                "sizes": "128x128",
                "type": "image/jpeg"
            },
            {
                "src": "icons/icon-144x144.jpg",
                "sizes": "144x144",
                "type": "image/jpeg"
            },
            {
                "src": "icons/icon-152x152.jpg",
                "sizes": "152x152",
                "type": "image/jpeg"
            },
            {
                "src": "icons/icon-192x192.jpg",
                "sizes": "192x192",
                "type": "image/jpeg"
            },
            {
                "src": "icons/icon-384x384.jpg",
                "sizes": "384x384",
                "type": "image/jpeg"
            },
            {
                "src": "icons/icon-512x512.jpg",
                "sizes": "512x512",
                "type": "image/jpeg"
            }
        ]
    }
    
    with open(os.path.join(base_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest_content, f, indent=2)
    
    # 2. Création du service worker (sw.js)
    sw_content = """const CACHE_NAME = 'sdbsn-app-v1';
const urlsToCache = [
  '/',
  '/css/style.css',
  '/js/main.js',
  '/manifest.json',
  '/icons/icon-192x192.jpg',
  '/icons/icon-512x512.jpg'
];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Cache ouvert');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});
"""
    
    with open(os.path.join(base_dir, "sw.js"), "w", encoding="utf-8") as f:
        f.write(sw_content)
    
    # 3. Création du CSS pour PWA (pwa.css)
    css_content = """/* Styles PWA */
.pwa-install-banner {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: #333;
    color: white;
    padding: 15px 20px;
    border-radius: 10px;
    z-index: 10000;
    display: none;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.pwa-install-banner button {
    background: #007bff;
    color: white;
    border: none;
    padding: 8px 16px;
    margin: 0 5px;
    border-radius: 5px;
    cursor: pointer;
}

.pwa-install-banner button:hover {
    background: #0056b3;
}

/* Améliorations pour le mode standalone */
@media all and (display-mode: standalone) {
    body {
        height: 100vh;
        overflow: hidden;
    }
}
"""
    
    css_dir = os.path.join(base_dir, "css")
    os.makedirs(css_dir, exist_ok=True)
    
    with open(os.path.join(css_dir, "pwa.css"), "w", encoding="utf-8") as f:
        f.write(css_content)
    
    # 4. Création du JavaScript PWA (pwa.js)
    js_content = """// Service Worker Registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker enregistré avec succès');
            })
            .catch(function(error) {
                console.log('Erreur ServiceWorker:', error);
            });
    });
}

// Gestion de l'installation PWA
let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    showInstallBanner();
});

function showInstallBanner() {
    // Vérifie si l'app n'est pas déjà installée
    if (window.matchMedia('(display-mode: standalone)').matches) {
        return;
    }
    
    const banner = document.createElement('div');
    banner.className = 'pwa-install-banner';
    banner.id = 'pwa-banner';
    banner.innerHTML = `
        <span>Installer SDBSN Code comme application ?</span>
        <button onclick="installPWA()">Installer</button>
        <button onclick="dismissBanner()">Plus tard</button>
    `;
    document.body.appendChild(banner);
    banner.style.display = 'block';
    
    // Cache automatique après 10 secondes
    setTimeout(() => {
        dismissBanner();
    }, 10000);
}

function installPWA() {
    if (deferredPrompt) {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
                console.log('Utilisateur a accepté l\\'installation');
                dismissBanner();
            }
            deferredPrompt = null;
        });
    }
}

function dismissBanner() {
    const banner = document.getElementById('pwa-banner');
    if (banner) {
        banner.style.display = 'none';
    }
}

// Détection du mode standalone
window.addEventListener('load', function() {
    if (window.matchMedia('(display-mode: standalone)').matches) {
        console.log('App en mode standalone');
    }
});
"""
    
    js_dir = os.path.join(base_dir, "js")
    os.makedirs(js_dir, exist_ok=True)
    
    with open(os.path.join(js_dir, "pwa.js"), "w", encoding="utf-8") as f:
        f.write(js_content)

def find_and_use_existing_icon(base_dir):
    """Cherche et utilise l'icône existante dans le dossier icons"""
    
    icons_dir = os.path.join(base_dir, "icons")
    
    # Noms possibles pour l'icône
    possible_names = [
        "icon.jpg", "icon.jpeg", "icon.png",
        "icone.jpg", "icone.jpeg", "icone.png",
        "logo.jpg", "logo.jpeg", "logo.png"
    ]
    
    # Chercher l'icône dans le dossier icons
    for icon_name in possible_names:
        icon_path = os.path.join(icons_dir, icon_name)
        if os.path.exists(icon_path):
            print(f"✅ Icône trouvée: {icon_path}")
            return icon_path
    
    return None

def create_icon_variants(base_dir):
    """Crée les différentes tailles d'icônes à partir de l'icône principale"""
    
    # CORRECTION : Appel correct de la fonction (sans "and" en trop)
    icon_path = find_and_use_existing_icon(base_dir)
    
    if not icon_path:
        print("❌ Aucune icône trouvée dans le dossier 'icons'")
        print("📌 Placez votre icône nommée 'icon.jpg' dans le dossier 'icons/'")
        return False
    
    icons_dir = os.path.join(base_dir, "icons")
    
    try:
        # Si l'icône existe, créez des copies avec les noms requis
        from PIL import Image
        
        original_icon = Image.open(icon_path)
        
        # Tailles requises pour PWA
        sizes = [72, 96, 128, 144, 152, 192, 384, 512]
        
        for size in sizes:
            # Redimensionner l'image
            resized_icon = original_icon.resize((size, size), Image.Resampling.LANCZOS)
            
            # Sauvegarder en JPG
            output_path = os.path.join(icons_dir, f"icon-{size}x{size}.jpg")
            resized_icon.save(output_path, "JPEG", quality=95)
            print(f"✅ Icône {size}x{size} créée")
        
        print("🎉 Toutes les icônes ont été créées automatiquement !")
        return True
        
    except ImportError:
        # Si PIL n'est pas disponible, créez juste un message d'instructions
        print("📋 Instructions pour les icônes :")
        print("   Votre icône principale est: icon.jpg")
        print("   Créez manuellement ces fichiers dans le dossier 'icons/':")
        print("   - icon-72x72.jpg, icon-96x96.jpg, icon-128x128.jpg")
        print("   - icon-144x144.jpg, icon-152x152.jpg, icon-192x192.jpg")
        print("   - icon-384x384.jpg, icon-512x512.jpg")
        
        # Créer un fichier d'instructions
        instructions = """# INSTRUCTIONS ICÔNES PWA

Votre icône principale a été détectée: icon.jpg

Pour compléter la configuration PWA, vous devez créer les fichiers suivants 
dans ce dossier 'icons/' :

- icon-72x72.jpg    (72x72 pixels)
- icon-96x96.jpg    (96x96 pixels)
- icon-128x128.jpg  (128x128 pixels)
- icon-144x144.jpg  (144x144 pixels)
- icon-152x152.jpg  (152x152 pixels)
- icon-192x192.jpg  (192x192 pixels)
- icon-384x384.jpg  (384x384 pixels)
- icon-512x512.jpg  (512x512 pixels)

Vous pouvez :
1. Renommer et redimensionner manuellement votre icon.jpg
2. Utiliser un outil en ligne comme : https://www.pwabuilder.com/imageGenerator
3. Installer PIL: pip install Pillow

Votre PWA fonctionnera une fois ces fichiers créés.
"""
        
        with open(os.path.join(icons_dir, "INSTRUCTIONS_ICONES.txt"), "w", encoding="utf-8") as f:
            f.write(instructions)
        
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la création des icônes: {e}")
        return False

def modify_index_html(base_dir):
    """Modifie uniquement le index.html pour ajouter les balises PWA"""
    
    index_path = os.path.join(base_dir, "index.html")
    
    if not os.path.exists(index_path):
        print("❌ index.html non trouvé")
        return False
    
    # Lecture du contenu actuel
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Vérification si déjà modifié
    if 'manifest.json' in content:
        print("✅ index.html a déjà les balises PWA")
        return True
    
    # Préparation des balises à ajouter (adaptées pour JPG)
    pwa_head = """
    <!-- PWA Configuration -->
    <link rel="manifest" href="/manifest.json">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="SDBSN Code">
    <link rel="apple-touch-icon" href="/icons/icon-152x152.jpg">
    <meta name="theme-color" content="#000000">
    <link rel="stylesheet" href="/css/pwa.css">
    """
    
    pwa_body = """
    <!-- PWA Scripts -->
    <script src="/js/pwa.js"></script>
    """
    
    # Insertion dans le head
    if '</head>' in content:
        content = content.replace('</head>', f'{pwa_head}\n</head>')
    elif '<head>' in content:
        content = content.replace('<head>', f'<head>\n{pwa_head}')
    
    # Insertion avant </body>
    if '</body>' in content:
        content = content.replace('</body>', f'{pwa_body}\n</body>')
    
    # Sauvegarde
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ index.html modifié avec succès")
    return True

def main():
    """Fonction principale"""
    print("🚀 Configuration PWA pour SDBSN Code")
    
    # Détermine le répertoire de travail
    base_dir = input("Entrez le chemin de votre site web (ou laissez vide pour le dossier actuel): ").strip()
    if not base_dir:
        base_dir = "."
    
    if not os.path.exists(base_dir):
        print(f"❌ Le dossier '{base_dir}' n'existe pas")
        return
    
    try:
        # Vérifier si l'icône existe déjà
        icons_dir = os.path.join(base_dir, "icons")
        icon_path = os.path.join(icons_dir, "icon.jpg")
        
        if os.path.exists(icon_path):
            print(f"✅ Icône détectée: {icon_path}")
        else:
            print("📌 Votre icône 'icon.jpg' doit être placée dans le dossier 'icons/'")
        
        # Création des fichiers PWA
        create_pwa_files(base_dir)
        print("✅ Fichiers PWA créés")
        
        # Tentative de création des variantes d'icônes
        create_icon_variants(base_dir)
        
        # Modification du index.html
        modify_index_html(base_dir)
        
        print("\n🎉 Configuration PWA terminée !")
        print("\n📋 Statut :")
        print("✅ Structure PWA créée")
        print("✅ Manifest configuré pour JPG")
        print("✅ Service Worker prêt")
        print("📌 Icônes : Vérifiez que toutes les tailles sont créées dans 'icons/'")
        
        print("\n🔧 Si les icônes manquent :")
        print("1. Renommez manuellement votre icon.jpg en différentes tailles")
        print("2. Ou utilisez: https://www.pwabuilder.com/imageGenerator")
        print("3. Ou installez Pillow: pip install Pillow")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()