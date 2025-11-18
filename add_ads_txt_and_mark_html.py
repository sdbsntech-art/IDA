import os
import re
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
ADS_LINE = "google.com, pub-3830476419469874, DIRECT, f08c47fec0942fa0"
ADS_TXT = ROOT / "ads.txt"
HTML_MARK_COMMENT = f"<!-- ads.txt: {ADS_LINE} -->"

def ensure_ads_txt():
    """
    Lit ads.txt de façon robuste (utf-8 puis fallback latin-1).
    Ajoute ADS_LINE si elle est absente. Retourne True si fichier créé/modifié.
    """
    # Si n'existe pas -> créer en utf-8
    if not ADS_TXT.exists():
        try:
            ADS_TXT.write_text(ADS_LINE + "\n", encoding="utf-8")
            return True
        except Exception:
            # dernier recours en binaire
            with open(ADS_TXT, "wb") as f:
                f.write((ADS_LINE + "\n").encode("utf-8", errors="replace"))
            return True

    # Si existe -> lire de façon robuste
    text = None
    try:
        text = ADS_TXT.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            text = ADS_TXT.read_text(encoding="latin-1")
        except Exception:
            # fallback: lire en binaire et décoder en remplaçant les caractères invalides
            try:
                raw = ADS_TXT.read_bytes()
                text = raw.decode("utf-8", errors="replace")
            except Exception:
                # si tout échoue, on considère qu'on ne peut pas lire proprement
                text = ""

    if ADS_LINE in text:
        return False

    # Ajoute la ligne en fin de fichier (écrit en utf-8)
    try:
        with open(ADS_TXT, "a", encoding="utf-8", errors="replace") as f:
            if not text.endswith("\n"):
                f.write("\n")
            f.write(ADS_LINE + "\n")
        return True
    except Exception:
        # dernier recours binaire
        try:
            with open(ADS_TXT, "ab") as f:
                f.write(("\n" + ADS_LINE + "\n").encode("utf-8", errors="replace"))
            return True
        except Exception:
            return False

def mark_html_files():
    modified = []
    for p in ROOT.rglob("*.html"):
        try:
            content = p.read_text(encoding="utf-8")
        except Exception:
            try:
                content = p.read_text(encoding="latin-1")
            except Exception:
                continue
        # Detect pages that "should" contain the ads info (contain AdSense-related scripts)
        if re.search(r"(adsbygoogle|googlesyndication|pagead2\.googlesyndication|amp-auto-ads)", content, re.IGNORECASE):
            if ADS_LINE in content or HTML_MARK_COMMENT in content:
                continue
            # insert comment just after opening <head>
            m = re.search(r"<head[^>]*>", content, re.IGNORECASE)
            if m:
                insert_pos = m.end()
                new_content = content[:insert_pos] + "\n    " + HTML_MARK_COMMENT + "\n" + content[insert_pos:]
            else:
                # fallback: prepend to file
                new_content = HTML_MARK_COMMENT + "\n" + content
            # backup and write
            shutil.copy2(p, p.with_suffix(p.suffix + ".bak"))
            p.write_text(new_content, encoding="utf-8")
            modified.append(str(p.relative_to(ROOT)))
    return modified

def main():
    changed_ads_txt = ensure_ads_txt()
    modified_pages = mark_html_files()
    print("ads.txt créé/actualisé:" , changed_ads_txt)
    if modified_pages:
        print("Pages modifiées (comment ajouté) :")
        for f in modified_pages:
            print(" -", f)
    else:
        print("Aucune page .html nécessitant le marqueur n'a été modifiée.")

if __name__ == "__main__":
    main()