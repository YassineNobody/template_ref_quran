import argparse
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog
from typing import Literal

from search.templates import Search, MultiTemplate


def run_resources(mode: Literal["array", "column"]):
    s = Search()  # id arbitraire juste pour avoir accès à resources()
    s.resources(mode)


def run_templates():
    refs = []
    print("👉 Mode sélection de références (tape 'stop' pour finir)")
    while True:
        raw = input("Saisir (id_surah,start_v[,end_v]) ou 'stop' : ")
        if raw.strip().lower() == "stop":
            break
        try:
            parts = raw.split(",")
            id_surah = int(parts[0])
            start_v = int(parts[1])
            end_v = int(parts[2]) if len(parts) > 2 else None
            refs.append((id_surah, start_v, end_v))
        except Exception as e:
            print(f"❌ Entrée invalide: {e}")

    if not refs:
        print("⚠️ Aucune référence donnée, arrêt.")
        return

    tpl = MultiTemplate(refs)
    html = tpl.get_template()

    # 🔹 Demander un nom de fichier valide
    while True:
        filename = input("👉 Nom du fichier (sans extension) : ").strip()
        if not filename:
            print("❌ Nom vide, réessaie.")
            continue
        # caractères interdits dans les noms de fichiers (Windows / cross-platform)
        if any(c in filename for c in r'\/:*?"<>|'):
            print("❌ Nom invalide (caractères interdits). Réessaie.")
            continue
        break

    filename += ".html"

    # 🔹 Boîte de dialogue pour choisir un dossier
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Choisir un dossier de destination")
    if not folder:
        print("⚠️ Aucun dossier choisi, arrêt.")
        return

    path = Path(folder) / filename
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✔ Fichier HTML généré : {path}")

    # 🔹 Ouvrir automatiquement le fichier
    open_choice = input("👉 Voulez-vous ouvrir le fichier ? (o/n) ").lower()
    if open_choice != "o":
        return

    if shutil.which("code"):
        subprocess.run(["code", str(path)])
    else:
        system = platform.system()
        if system == "Windows":
            os.startfile(path)  # type: ignore
        elif system == "Darwin":
            subprocess.run(["open", str(path)])
        else:
            subprocess.run(["xdg-open", str(path)])


def main():
    parser = argparse.ArgumentParser(description="Quran CLI")
    parser.add_argument(
        "--resources",
        "-r",
        choices=["array", "column"],
        help="Afficher les sourates (array ou column)",
    )
    parser.add_argument(
        "--templates",
        "-t",
        action="store_true",
        help="Générer un template HTML à partir de références",
    )

    args = parser.parse_args()

    if args.resources:
        run_resources(args.resources)
    elif args.templates:
        run_templates()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
