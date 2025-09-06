import argparse
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog
from typing import Literal

from search import Search, MultiTemplate, PartsTemplate


def run_resources(mode: Literal["array", "column"]):
    s = Search()
    s.resources(mode)


def run_templates(parts: bool = False):
    refs = []
    print("👉 Mode sélection de références (tape 'stop' pour finir)")
    while True:
        raw = input("Saisir (id_surah,start_v[,end_v]) ou 'stop' : ")
        if raw.strip().lower() == "stop":
            break
        try:
            parts_split = raw.split(",")
            id_surah = int(parts_split[0])
            start_v = int(parts_split[1])
            end_v = int(parts_split[2]) if len(parts_split) > 2 else None
            refs.append((id_surah, start_v, end_v))
        except Exception as e:
            print(f"❌ Entrée invalide: {e}")

    if not refs:
        print("⚠️ Aucune référence donnée, arrêt.")
        return

    # 🔹 Choisir la classe selon le flag
    if parts:
        tpl = PartsTemplate(refs)
    else:
        tpl = MultiTemplate(refs)

    html = tpl.get_template()

    # 🔹 Demander un nom de fichier valide
    while True:
        filename = input("👉 Nom du fichier (sans extension) : ").strip()
        if not filename:
            print("❌ Nom vide, réessaie.")
            continue
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
    parser.add_argument(
        "--parts",
        "-p",
        action="store_true",
        help="Générer un template partiel (copiable dans une page)",
    )

    args = parser.parse_args()

    if args.resources:
        run_resources(args.resources)
    elif args.templates:
        run_templates(parts=args.parts)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
