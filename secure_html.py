import os

security_js = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Bloquer le clic droit
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        return false;
    });

    // Bloquer copier/coller/couper
    ['copy', 'cut', 'paste'].forEach(function(evt) {
        document.addEventListener(evt, function(e) {
            e.preventDefault();
            return false;
        });
    });

    // Bloquer raccourcis DevTools et code source
    document.addEventListener('keydown', function(e) {
        // F12
        if (e.key === 'F12' || e.keyCode === 123) {
            e.preventDefault();
            return false;
        }
        // Ctrl+Shift+I / Cmd+Opt+I
        if ((e.ctrlKey && e.shiftKey && e.key.toLowerCase() === 'i') ||
            (e.metaKey && e.altKey && e.key.toLowerCase() === 'i')) {
            e.preventDefault();
            return false;
        }
        // Ctrl+U / Cmd+U
        if ((e.ctrlKey && e.key.toLowerCase() === 'u') ||
            (e.metaKey && e.key.toLowerCase() === 'u')) {
            e.preventDefault();
            return false;
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