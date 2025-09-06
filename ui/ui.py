import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from pathlib import Path

from search import Search, MultiTemplate, PartsTemplate


class QuranUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quran Reference Generator")

        self.search = Search()
        self.refs = []

        # --- Onglets ---
        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True)

        # Onglet sélection
        frame_select = ttk.Frame(notebook)
        notebook.add(frame_select, text="Sélection")

        # Onglet sourates
        frame_sourates = ttk.Frame(notebook)
        notebook.add(frame_sourates, text="Sourates")

        # Onglet preview
        frame_preview = ttk.Frame(notebook)
        notebook.add(frame_preview, text="Preview HTML")

        # --- Input ID de sourate ---
        tk.Label(frame_select, text="ID de sourate :").grid(row=0, column=0, sticky="w")
        self.surah_id_entry = tk.Entry(frame_select, width=10, fg="grey")
        self.surah_id_entry.insert(0, "Ex: 2")
        self.surah_id_entry.bind("<FocusIn>", self._clear_placeholder)
        self.surah_id_entry.bind("<FocusOut>", self._add_placeholder)
        self.surah_id_entry.bind("<KeyRelease>", self._update_surah_name)
        self.surah_id_entry.grid(row=0, column=1, sticky="w")

        self.surah_name_label = tk.Label(frame_select, text="", fg="blue")
        self.surah_name_label.grid(row=0, column=2, sticky="w")

        # --- Versets ---
        tk.Label(frame_select, text="Verset début :").grid(row=1, column=0, sticky="w")
        self.start_entry = tk.Entry(frame_select, width=10)
        self.start_entry.grid(row=1, column=1, sticky="w")

        tk.Label(frame_select, text="Verset fin (optionnel) :").grid(
            row=2, column=0, sticky="w"
        )
        self.end_entry = tk.Entry(frame_select, width=10)
        self.end_entry.grid(row=2, column=1, sticky="w")

        # --- Boutons références ---
        self.add_button = tk.Button(
            frame_select, text="➕ Ajouter référence", command=self.add_reference
        )
        self.add_button.grid(row=3, column=0, pady=5)

        self.remove_button = tk.Button(
            frame_select, text="🗑 Supprimer sélection", command=self.remove_reference
        )
        self.remove_button.grid(row=3, column=1, pady=5)

        self.clear_button = tk.Button(
            frame_select, text="❌ Tout supprimer", command=self.clear_references
        )
        self.clear_button.grid(row=3, column=2, pady=5)

        # --- Liste des références ---
        tk.Label(frame_select, text="Références ajoutées :").grid(
            row=4, column=0, sticky="w"
        )
        self.listbox = tk.Listbox(frame_select, width=60, height=8)
        self.listbox.grid(row=5, column=0, columnspan=3, pady=5)

        # --- Options ---
        self.is_parts = tk.BooleanVar(value=False)
        tk.Checkbutton(
            frame_select, text="⚡ Mode bloc (PartsTemplate)", variable=self.is_parts
        ).grid(row=6, column=0, sticky="w")

        # --- Boutons action ---
        self.preview_button = tk.Button(
            frame_select, text="👁 Preview", command=self.preview_html
        )
        self.preview_button.grid(row=7, column=0, pady=5)

        self.generate_button = tk.Button(
            frame_select, text="💾 Générer fichier", command=self.generate_html
        )
        self.generate_button.grid(row=7, column=1, pady=5)

        self.copy_button = tk.Button(
            frame_select, text="📋 Copier HTML", command=self.copy_html
        )
        self.copy_button.grid(row=7, column=2, pady=5)

        self.reset_button = tk.Button(
            frame_select, text="🔄 Reset", command=self.reset_all
        )
        self.reset_button.grid(row=8, column=0, columnspan=3, pady=10)

        # --- Onglet sourates ---
        text_sourates = tk.Text(frame_sourates, wrap="none", height=25)
        text_sourates.pack(fill="both", expand=True)
        for ch in self.search.index_json:
            text_sourates.insert(
                tk.END,
                f"{ch['id']:>3} - {ch['name_simple']} ({ch['translated_name']['name']})\n",
            )
        text_sourates.config(state="disabled")

        # --- Onglet preview ---
        self.preview_text = tk.Text(
            frame_preview, wrap="word", height=25, state="disabled"
        )
        self.preview_text.pack(fill="both", expand=True)

        self.generated_html = ""

    # --- Gestion placeholder ---
    def _clear_placeholder(self, event):
        if (
            self.surah_id_entry.get() == "Ex: 2"
            and self.surah_id_entry.cget("fg") == "grey"
        ):
            self.surah_id_entry.delete(0, tk.END)
            self.surah_id_entry.config(fg="black")

    def _add_placeholder(self, event):
        if not self.surah_id_entry.get():
            self.surah_id_entry.insert(0, "Ex: 2")
            self.surah_id_entry.config(fg="grey")

    def _update_surah_name(self, event):
        text = self.surah_id_entry.get().strip()
        if not text.isdigit():
            self.surah_name_label.config(text="")
            return
        surah_id = int(text)
        info = self.search.find_complete_surah_info("id", surah_id)
        if info:
            self.surah_name_label.config(
                text=f"{info['name_simple']} ({info['translated_name']['name']})"
            )
        else:
            self.surah_name_label.config(text="ID invalide", fg="red")

    # --- Gestion références ---
    def add_reference(self):
        text = self.surah_id_entry.get().strip()
        if not text.isdigit():
            messagebox.showerror("Erreur", "L’ID de sourate doit être un nombre.")
            return

        surah_id = int(text)
        info = self.search.find_complete_surah_info("id", surah_id)
        if not info:
            messagebox.showerror("Erreur", "Sourate introuvable.")
            return

        try:
            start_v = int(self.start_entry.get())
            end_v = int(self.end_entry.get()) if self.end_entry.get().strip() else None
        except ValueError:
            messagebox.showerror("Erreur", "Numéros de versets invalides.")
            return

        self.refs.append((surah_id, start_v, end_v))
        self.listbox.insert(
            tk.END, f"Sourate {surah_id}, v.{start_v}" + (f"-{end_v}" if end_v else "")
        )

        # ✅ reset uniquement les champs versets, pas la sourate
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)

    def remove_reference(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Info", "Sélectionnez une référence à supprimer.")
            return
        idx = sel[0]
        self.listbox.delete(idx)
        del self.refs[idx]

    def clear_references(self):
        self.refs.clear()
        self.listbox.delete(0, tk.END)

    def preview_html(self):
        if not self.refs:
            messagebox.showerror("Erreur", "Aucune référence sélectionnée.")
            return

        tpl = (
            PartsTemplate(self.refs)
            if self.is_parts.get()
            else MultiTemplate(self.refs)
        )
        html = tpl.get_template()
        self.generated_html = html

        self.preview_text.config(state="normal")
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert(tk.END, html)
        self.preview_text.config(state="disabled")

    def copy_html(self):
        if not self.generated_html:
            messagebox.showerror("Erreur", "Aucun HTML généré.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(self.generated_html)
        messagebox.showinfo("Copié", "HTML copié dans le presse-papier ✅")

    def generate_html(self):
        if not self.refs:
            messagebox.showerror("Erreur", "Aucune référence sélectionnée.")
            return
        if self.is_parts.get():
            messagebox.showerror("Erreur", "Mode bloc actif, utilisez Copier HTML.")
            return

        if not self.generated_html:
            self.preview_html()

        filename = simpledialog.askstring(
            "Nom du fichier", "Nom du fichier (sans extension) :"
        )
        if not filename:
            return
        if any(c in filename for c in r'\/:*?"<>|'):
            messagebox.showerror("Erreur", "Nom de fichier invalide.")
            return

        filename += ".html"

        folder = filedialog.askdirectory(title="Choisir un dossier de destination")
        if not folder:
            return

        path = Path(folder) / filename
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.generated_html)

        messagebox.showinfo("Succès", f"Fichier généré : {path}")

    def reset_all(self):
        self.refs.clear()
        self.listbox.delete(0, tk.END)

        # vider uniquement les champs versets
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)

        # vider le preview
        self.preview_text.config(state="normal")
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.config(state="disabled")

        self.generated_html = ""


def main():
    root = tk.Tk()
    app = QuranUI(root)
    root.mainloop()
