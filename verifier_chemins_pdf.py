#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification des chemins des fichiers PDF
Vérifie que tous les chemins référencés dans les fichiers HTML correspondent 
à des fichiers existants dans les dossiers ASSETS et files.
"""

import os
import re
import glob
from pathlib import Path
from typing import List, Dict, Set, Tuple

class PDFPathChecker:
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.assets_dir = self.base_dir / "ASSETS"
        self.files_dir = self.base_dir / "files"
        
        # Statistiques
        self.stats = {
            'total_references': 0,
            'valid_paths': 0,
            'broken_paths': 0,
            'missing_files': 0,
            'case_mismatches': 0
        }
        
        # Résultats
        self.broken_paths = []
        self.missing_files = []
        self.case_mismatches = []
        self.valid_paths = []

    def get_existing_pdf_files(self) -> Dict[str, Set[str]]:
        """Récupère tous les fichiers PDF existants dans ASSETS et files"""
        existing_files = {
            'ASSETS': set(),
            'files': set()
        }
        
        # Fichiers dans ASSETS
        if self.assets_dir.exists():
            for pdf_file in self.assets_dir.glob("*.pdf"):
                existing_files['ASSETS'].add(pdf_file.name)
        
        # Fichiers dans files
        if self.files_dir.exists():
            for pdf_file in self.files_dir.glob("*.pdf"):
                existing_files['files'].add(pdf_file.name)
        
        return existing_files

    def extract_pdf_references_from_html(self, html_file: Path) -> List[Tuple[str, str, int]]:
        """Extrait les références PDF d'un fichier HTML"""
        references = []
        
        try:
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Pattern pour trouver les liens vers des fichiers PDF
            # Cherche href="ASSETS/..." ou href="files/..."
            pattern = r'href=["\'](ASSETS|files)/([^"\']*\.pdf)["\']'
            matches = re.finditer(pattern, content, re.IGNORECASE)
            
            for match in matches:
                folder = match.group(1)
                filename = match.group(2)
                line_num = content[:match.start()].count('\n') + 1
                references.append((folder, filename, line_num))
                
        except Exception as e:
            print(f"Erreur lors de la lecture de {html_file}: {e}")
            
        return references

    def check_path_validity(self, folder: str, filename: str, existing_files: Dict[str, Set[str]]) -> Dict:
        """Vérifie si un chemin PDF est valide"""
        result = {
            'valid': False,
            'issue': None,
            'suggested_fix': None
        }
        
        if folder not in existing_files:
            result['issue'] = f"Dossier '{folder}' n'existe pas"
            return result
            
        # Vérification exacte
        if filename in existing_files[folder]:
            result['valid'] = True
            return result
            
        # Vérification insensible à la casse
        filename_lower = filename.lower()
        for existing_file in existing_files[folder]:
            if existing_file.lower() == filename_lower:
                result['issue'] = "Différence de casse"
                result['suggested_fix'] = existing_file
                return result
                
        # Le fichier n'existe pas
        result['issue'] = "Fichier introuvable"
        return result

    def scan_html_files(self) -> None:
        """Scanne tous les fichiers HTML et vérifie les références PDF"""
        html_files = list(self.base_dir.glob("*.html"))
        
        if not html_files:
            print("Aucun fichier HTML trouvé dans le répertoire courant.")
            return
            
        print(f"Scan de {len(html_files)} fichiers HTML...")
        
        # Récupérer les fichiers PDF existants
        existing_files = self.get_existing_pdf_files()
        
        print(f"Fichiers PDF trouvés:")
        print(f"  - ASSETS: {len(existing_files['ASSETS'])} fichiers")
        print(f"  - files: {len(existing_files['files'])} fichiers")
        print()
        
        # Scanner chaque fichier HTML
        for html_file in html_files:
            print(f"Analyse de {html_file.name}...")
            references = self.extract_pdf_references_from_html(html_file)
            
            if not references:
                print(f"  Aucune référence PDF trouvée")
                continue
                
            print(f"  {len(references)} référence(s) PDF trouvée(s)")
            
            for folder, filename, line_num in references:
                self.stats['total_references'] += 1
                
                result = self.check_path_validity(folder, filename, existing_files)
                
                if result['valid']:
                    self.stats['valid_paths'] += 1
                    self.valid_paths.append({
                        'file': html_file.name,
                        'line': line_num,
                        'path': f"{folder}/{filename}"
                    })
                else:
                    self.stats['broken_paths'] += 1
                    
                    if result['issue'] == "Fichier introuvable":
                        self.stats['missing_files'] += 1
                        self.missing_files.append({
                            'file': html_file.name,
                            'line': line_num,
                            'path': f"{folder}/{filename}",
                            'issue': result['issue']
                        })
                    elif result['issue'] == "Différence de casse":
                        self.stats['case_mismatches'] += 1
                        self.case_mismatches.append({
                            'file': html_file.name,
                            'line': line_num,
                            'path': f"{folder}/{filename}",
                            'suggested': result['suggested_fix'],
                            'issue': result['issue']
                        })
                    else:
                        self.broken_paths.append({
                            'file': html_file.name,
                            'line': line_num,
                            'path': f"{folder}/{filename}",
                            'issue': result['issue']
                        })

    def generate_report(self) -> str:
        """Génère un rapport détaillé des vérifications"""
        report = []
        report.append("=" * 80)
        report.append("RAPPORT DE VÉRIFICATION DES CHEMINS PDF")
        report.append("=" * 80)
        report.append("")
        
        # Statistiques générales
        report.append("STATISTIQUES GÉNÉRALES:")
        report.append("-" * 40)
        report.append(f"Total des références PDF: {self.stats['total_references']}")
        report.append(f"Chemins valides: {self.stats['valid_paths']}")
        report.append(f"Chemins cassés: {self.stats['broken_paths']}")
        report.append(f"  - Fichiers manquants: {self.stats['missing_files']}")
        report.append(f"  - Différences de casse: {self.stats['case_mismatches']}")
        report.append("")
        
        # Fichiers manquants
        if self.missing_files:
            report.append("FICHIERS MANQUANTS:")
            report.append("-" * 40)
            for item in self.missing_files:
                report.append(f"❌ {item['file']}:{item['line']} - {item['path']}")
            report.append("")
        
        # Différences de casse
        if self.case_mismatches:
            report.append("DIFFÉRENCES DE CASSE:")
            report.append("-" * 40)
            for item in self.case_mismatches:
                report.append(f"⚠️  {item['file']}:{item['line']} - {item['path']}")
                report.append(f"   → Suggestion: {item['suggested']}")
            report.append("")
        
        # Autres problèmes
        if self.broken_paths:
            report.append("AUTRES PROBLÈMES:")
            report.append("-" * 40)
            for item in self.broken_paths:
                report.append(f"❌ {item['file']}:{item['line']} - {item['path']}")
                report.append(f"   → Problème: {item['issue']}")
            report.append("")
        
        # Résumé
        if self.stats['broken_paths'] == 0:
            report.append("✅ TOUS LES CHEMINS PDF SONT VALIDES!")
        else:
            report.append(f"❌ {self.stats['broken_paths']} PROBLÈME(S) TROUVÉ(S)")
            
        report.append("=" * 80)
        
        return "\n".join(report)

    def save_report(self, filename: str = "rapport_verification_pdf.txt") -> None:
        """Sauvegarde le rapport dans un fichier"""
        report = self.generate_report()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
            
        print(f"Rapport sauvegardé dans: {filename}")

def main():
    """Fonction principale"""
    print("🔍 Vérification des chemins des fichiers PDF...")
    print()
    
    # Créer le vérificateur
    checker = PDFPathChecker()
    
    # Scanner les fichiers HTML
    checker.scan_html_files()
    
    # Générer et afficher le rapport
    report = checker.generate_report()
    print(report)
    
    # Sauvegarder le rapport
    checker.save_report()
    
    # Code de sortie
    if checker.stats['broken_paths'] > 0:
        print(f"\n❌ {checker.stats['broken_paths']} problème(s) trouvé(s)")
        return 1
    else:
        print("\n✅ Tous les chemins PDF sont valides!")
        return 0

if __name__ == "__main__":
    exit(main())
