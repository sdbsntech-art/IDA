// Service Worker Registration
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
                console.log('Utilisateur a accepté l\'installation');
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
