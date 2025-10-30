import os
import re
from pathlib import Path
import shutil

HEAD_SNIPPET = (
    '<script async custom-element="amp-auto-ads"\n'
    '        src="https://cdn.ampproject.org/v0/amp-auto-ads-0.1.js">\n'
    '</script>\n'
)

BODY_SNIPPET = (
    '<amp-auto-ads type="adsense"\n'
    '        data-ad-client="ca-pub-3942650991755175">\n'
    '</amp-auto-ads>\n'
)

ROOT = Path(__file__).resolve().parent

def already_has_head(text: str) -> bool:
    return 'amp-auto-ads-0.1.js' in text or '<script async custom-element="amp-auto-ads"' in text

def already_has_body(text: str) -> bool:
    return '<amp-auto-ads' in text

def inject_snippets(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    new_text = text
    changed = False

    # Insert HEAD_SNIPPET just after opening <head> if not present
    if not already_has_head(text):
        m = re.search(r'<head[^>]*>', text, flags=re.IGNORECASE)
        if m:
            insert_pos = m.end()
            new_text = new_text[:insert_pos] + "\n" + HEAD_SNIPPET + new_text[insert_pos:]
            changed = True
        else:
            # fallback: insert before closing </head> if exists
            if re.search(r'</head>', text, flags=re.IGNORECASE):
                new_text = re.sub(r'(</head>)', HEAD_SNIPPET + r'\1', new_text, flags=re.IGNORECASE)
                changed = True
            else:
                # no head tag: insert at top
                new_text = HEAD_SNIPPET + new_text
                changed = True

    # Refresh reference for body check/insertion
    text_after_head = new_text

    # Insert BODY_SNIPPET just after opening <body> if not present
    if not already_has_body(text_after_head):
        m2 = re.search(r'<body[^>]*>', text_after_head, flags=re.IGNORECASE)
        if m2:
            insert_pos = m2.end()
            new_text = text_after_head[:insert_pos] + "\n" + BODY_SNIPPET + text_after_head[insert_pos:]
            changed = True
        else:
            # fallback: insert before closing </body> if exists
            if re.search(r'</body>', text_after_head, flags=re.IGNORECASE):
                new_text = re.sub(r'(</body>)', BODY_SNIPPET + r'\1', text_after_head, flags=re.IGNORECASE)
                changed = True
            else:
                # no body tag: append at end
                new_text = text_after_head + "\n" + BODY_SNIPPET
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
        print("Aucun fichier modifié (les snippets existent peut‑être déjà).")

if __name__ == "__main__":
    main()