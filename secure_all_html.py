import os

security_js = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Bloquer le clic droit
    document.addEventListener('contextmenu', function(e) { e.preventDefault(); return false; });

    // Bloquer copier/couper/coller
    ['copy', 'cut', 'paste'].forEach(function(evt) {
        document.addEventListener(evt, function(e) { e.preventDefault(); return false; });
    });

    // Bloquer la sélection de texte
    document.addEventListener('selectstart', function(e) { e.preventDefault(); return false; });

    // Bloquer le drag & drop d'images
    document.addEventListener('dragstart', function(e) {
        if (e.target.tagName === 'IMG') { e.preventDefault(); return false; }
    });

    // Bloquer toutes les touches F1 à F12 et autres combinaisons
    document.addEventListener('keydown', function(e) {
        // Bloquer touches F1 à F12
        if (e.key.match(/^F[1-9]$|^F1[0-2]$/) || (e.keyCode >= 112 && e.keyCode <= 123)) {
            e.preventDefault(); return false;
        }
        // Ctrl+U, Ctrl+Shift+I, Ctrl+Shift+C, Ctrl+S, Ctrl+Alt+I, Ctrl+Alt+J, Ctrl+Alt+C
        if (
            (e.ctrlKey && e.key.toLowerCase() === 'u') ||
            (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === 'i') ||
            (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === 'c') ||
            (e.ctrlKey && e.key.toLowerCase() === 's') ||
            (e.ctrlKey && e.altKey && e.key.toLowerCase() === 'i') ||
            (e.ctrlKey && e.altKey && e.key.toLowerCase() === 'j') ||
            (e.ctrlKey && e.altKey && e.key.toLowerCase() === 'c')
        ) {
            e.preventDefault(); return false;
        }
    });

    // Détection DevTools par resize
    setInterval(function() {
        if (window.outerWidth - window.innerWidth > 160 ||
            window.outerHeight - window.innerHeight > 160) {
            document.body.innerHTML = '<h1 style="color:red;text-align:center;margin-top:20vh;">Accès restreint : DevTools détecté !</h1>';
        }
    }, 1000);
});
</script>
"""

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            # Ajoute le script juste avant </body> si pas déjà présent
            if security_js.strip() not in content:
                new_content = content.replace('</body>', security_js + '\n</body>')
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)