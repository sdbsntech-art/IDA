import os
import re
from pathlib import Path
import shutil

# ...existing code...
HEAD_SNIPPET = (
    '<script async custom-element="amp-auto-ads"\n'
    '        src="https://cdn.ampproject.org/v0/amp-auto-ads-0.1.js">\n'
    '</script>\n'
)

# Nouveau snippet demandé (client = ca-pub-3830476419469874)
ADSENSE_SNIPPET = (
    '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3830476419469874"\n'
    '     crossorigin="anonymous"></script>\n'
)

BODY_SNIPPET = (
    '<amp-auto-ads type="adsense"\n'
    '        data-ad-client="ca-pub-3942650991755175">\n'
    '</amp-auto-ads>\n'
)

ROOT = Path(__file__).resolve().parent

def already_has_adsense(text: str) -> bool:
    # vérifie la présence du client spécifique
    return 'ca-pub-3830476419469874' in text

def already_has_head(text: str) -> bool:
    return 'amp-auto-ads-0.1.js' in text

def already_has_body(text: str) -> bool:
    return '<amp-auto-ads' in text

def inject_snippets(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    new_text = text
    changed = False

    # Insère ADSENSE_SNIPPET juste après l'ouverture <head> si le client demandé n'est pas présent
    if not already_has_adsense(text):
        m_head = re.search(r'<head[^>]*>', text, flags=re.IGNORECASE)
        if m_head:
            insert_pos = m_head.end()
            new_text = new_text[:insert_pos] + "\n" + ADSENSE_SNIPPET + new_text[insert_pos:]
            changed = True
        elif re.search(r'</head>', text, flags=re.IGNORECASE):
            # fallback : avant </head>
            new_text = re.sub(r'(</head>)', ADSENSE_SNIPPET + r'\1', new_text, flags=re.IGNORECASE)
            changed = True
        else:
            # pas de <head> détecté : insère en début
            new_text = ADSENSE_SNIPPET + new_text
            changed = True

    # Reste des insertions existantes (HEAD_SNIPPET pour amp auto-ads et BODY_SNIPPET)
    # Insère HEAD_SNIPPET juste après <head> si non présent
    if not already_has_head(new_text):
        m = re.search(r'<head[^>]*>', new_text, flags=re.IGNORECASE)
        if m:
            insert_pos = m.end()
            new_text = new_text[:insert_pos] + "\n" + HEAD_SNIPPET + new_text[insert_pos:]
            changed = True
        elif re.search(r'</head>', new_text, flags=re.IGNORECASE):
            new_text = re.sub(r'(</head>)', HEAD_SNIPPET + r'\1', new_text, flags=re.IGNORECASE)
            changed = True

    # Insère BODY_SNIPPET juste après <body> si non présent
    if not already_has_body(new_text):
        m2 = re.search(r'<body[^>]*>', new_text, flags=re.IGNORECASE)
        if m2:
            insert_pos = m2.end()
            new_text = new_text[:insert_pos] + "\n" + BODY_SNIPPET + new_text[insert_pos:]
            changed = True
        elif re.search(r'</body>', new_text, flags=re.IGNORECASE):
            new_text = re.sub(r'(</body>)', BODY_SNIPPET + r'\1', new_text, flags=re.IGNORECASE)
            changed = True
        else:
            new_text = new_text + "\n" + BODY_SNIPPET
            changed = True

    if changed:
        bak = path.with_suffix(path.suffix + ".bak")
        shutil.copy2(path, bak)
        path.write_text(new_text, encoding="utf-8")
        return True

    return False

def main():
    modified = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        for fname in filenames:
            if fname.lower().endswith(".html"):
                p = Path(dirpath) / fname
                try:
                    if inject_snippets(p):
                        modified.append(str(p.relative_to(ROOT)))
                except Exception as e:
                    print(f"Erreur sur {p}: {e}")

    print("\nInjection terminée.")
    if modified:
        print("Fichiers modifiés:")
        for f in modified:
            print("  -", f)
        print("\nCopies .bak créées pour chaque fichier modifié.")
    else:
        print("Aucun fichier modifié (le snippet existe peut‑être déjà).")

if __name__ == "__main__":
    main()
# ...existing code...