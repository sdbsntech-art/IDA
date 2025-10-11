import os

description = '''
<!-- 🚀 Grafikart.fr Description Start -->
<div class="grafikart-footer-info" style="background:#f5f5fa;border-radius:8px;padding:18px;margin:20px 0;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.06);font-size:16px;">
    <strong>🚀 Apprenez le développement avec <a href="https://grafikart.fr/" target="_blank" style="color:#764ba2;text-decoration:underline;">Grafikart.fr</a></strong><br>
    La plateforme de Jonathan Boyer offre des centaines de tutoriels gratuits et formations en développement web.<br>
    Que vous soyez débutant ou expert, vous y trouverez des ressources de qualité sur tous les langages et technologies du web.<br><br>
    <span style="font-weight:bold;">📺 Suivez leur chaîne YouTube !</span><br>
    Pour aller plus loin, abonnez-vous à leur chaîne YouTube et découvrez de nouveaux contenus exclusifs.<br>
    Chaque abonné compte pour soutenir cette initiative francophone exceptionnelle !<br><br>
    👉 <a href="https://grafikart.fr/" target="_blank" style="color:#764ba2;">grafikart.fr</a> - 📺 YouTube : <a href="https://www.youtube.com/@grafikart" target="_blank" style="color:#764ba2;">@grafikart</a>
</div>
<!-- 🚀 Grafikart.fr Description End -->
'''

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            # Insère juste avant <div class="footer-bottom">
            if '<div class="footer-bottom">' in content and 'grafikart-footer-info' not in content:
                new_content = content.replace('<div class="footer-bottom">', description + '\n<div class="footer-bottom">')
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)