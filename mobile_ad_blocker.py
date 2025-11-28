#!/usr/bin/env python3
import os
from pathlib import Path

# CSS de blocage
css = """<style>
@media (max-width: 767px) {
    .ad-container, .ads, .advertisement, .publicite, .pub,
    [class*="ad-"], [id*="ad-"], [class*="pub"] { 
        display: none !important; 
    }
}
@media (min-width: 768px) and (max-width: 1024px) {
    .ad-container, .ads, .advertisement, .publicite,
    [class*="ad-"], [id*="ad-"] { 
        display: none !important; 
    }
}
</style>"""

# Appliquer à tous les HTML
for html_file in Path('.').rglob('*.html'):
    with open(html_file, 'r+', encoding='utf-8') as f:
        content = f.read()
        if '<head>' in content and "Blocage des publicités" not in content:
            new_content = content.replace('<head>', '<head>\n' + css)
            f.seek(0)
            f.write(new_content)
            f.truncate()
            print(f"✅ {html_file} modifié")

print("🎉 Tous les fichiers HTML ont été mis à jour!")