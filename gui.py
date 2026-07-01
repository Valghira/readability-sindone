import customtkinter as ctk
from tkinter import filedialog
from src.core import (
    load_data, inspect_json,
    generate_csv_report, generate_excel_report,
    INDEX_REGISTRY, DEFAULT_JSON_PATH,
)

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Analisi Leggibilità – Museo della Sindone")
        self.geometry("820x740")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.data = None
        self.structure = {}

        self._build_file_section()
        self._build_config_section()
        self._build_category_section()
        self._build_run_section()
        self._build_log_section()

        ctk.CTkLabel(
            self,
            text="Sviluppato da Valerio Ghirardotto",
            font=ctk.CTkFont(size=11),
            text_color="gray",
        ).grid(row=5, column=0, pady=(0, 6))

        # Load the default JSON on startup
        self._load_json(DEFAULT_JSON_PATH)

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_file_section(self):
        frame = ctk.CTkFrame(self)
        frame.grid(row=0, column=0, padx=12, pady=(12, 4), sticky="ew")
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="File JSON", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, columnspan=3, padx=12, pady=(10, 4), sticky="w"
        )

        self.json_path_var = ctk.StringVar(value=DEFAULT_JSON_PATH)
        ctk.CTkEntry(frame, textvariable=self.json_path_var).grid(
            row=1, column=0, columnspan=2, padx=12, pady=4, sticky="ew"
        )
        ctk.CTkButton(frame, text="Sfoglia", width=90, command=self._browse_json).grid(
            row=1, column=2, padx=(0, 12), pady=4
        )

        self.corpus_info = ctk.CTkTextbox(frame, height=56, state="disabled",
                                          font=ctk.CTkFont(size=12))
        self.corpus_info.grid(row=2, column=0, columnspan=3, padx=12, pady=(4, 10), sticky="ew")

    def _build_config_section(self):
        frame = ctk.CTkFrame(self)
        frame.grid(row=1, column=0, padx=12, pady=4, sticky="ew")
        frame.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(frame, text="Configurazione", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, columnspan=3, padx=12, pady=(10, 4), sticky="w"
        )

        # --- Indices ---
        idx_frame = ctk.CTkFrame(frame, fg_color="transparent")
        idx_frame.grid(row=1, column=0, padx=12, pady=(0, 10), sticky="nw")

        ctk.CTkLabel(idx_frame, text="Indici", font=ctk.CTkFont(size=13)).pack(anchor="w", pady=(0, 4))

        self.index_vars = {}
        for name in INDEX_REGISTRY:
            var = ctk.BooleanVar(value=True)
            self.index_vars[name] = var
            ctk.CTkCheckBox(idx_frame, text=name, variable=var).pack(anchor="w", pady=2)

        btn_row = ctk.CTkFrame(idx_frame, fg_color="transparent")
        btn_row.pack(anchor="w", pady=(8, 0))
        ctk.CTkButton(btn_row, text="Tutti", width=70, height=26,
                      command=lambda: [v.set(True) for v in self.index_vars.values()]).pack(side="left", padx=(0, 4))
        ctk.CTkButton(btn_row, text="Nessuno", width=70, height=26,
                      command=lambda: [v.set(False) for v in self.index_vars.values()]).pack(side="left")

        # --- Language ---
        lang_frame = ctk.CTkFrame(frame, fg_color="transparent")
        lang_frame.grid(row=1, column=1, padx=12, pady=(0, 10), sticky="nw")

        ctk.CTkLabel(lang_frame, text="Lingua", font=ctk.CTkFont(size=13)).pack(anchor="w", pady=(0, 4))

        self.lang_var = ctk.StringVar(value="all")
        for val, label in [("all", "Tutte"), ("it", "Italiano"), ("en", "Inglese")]:
            ctk.CTkRadioButton(lang_frame, text=label, variable=self.lang_var,
                               value=val, command=self._on_lang_change).pack(anchor="w", pady=2)

        # --- Format ---
        fmt_frame = ctk.CTkFrame(frame, fg_color="transparent")
        fmt_frame.grid(row=1, column=2, padx=12, pady=(0, 10), sticky="nw")

        ctk.CTkLabel(fmt_frame, text="Formato output", font=ctk.CTkFont(size=13)).pack(anchor="w", pady=(0, 4))

        self.fmt_csv = ctk.BooleanVar(value=True)
        self.fmt_excel = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(fmt_frame, text="CSV", variable=self.fmt_csv).pack(anchor="w", pady=2)
        ctk.CTkCheckBox(fmt_frame, text="Excel (.xlsx)", variable=self.fmt_excel).pack(anchor="w", pady=2)

    def _build_category_section(self):
        frame = ctk.CTkFrame(self)
        frame.grid(row=2, column=0, padx=12, pady=4, sticky="ew")

        ctk.CTkLabel(frame, text="Categorie", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, columnspan=5, padx=12, pady=(10, 4), sticky="w"
        )

        self.cat_mode_var = ctk.StringVar(value="all")
        ctk.CTkRadioButton(frame, text="Tutte le categorie",
                           variable=self.cat_mode_var, value="all",
                           command=self._on_cat_mode_change).grid(row=1, column=0, padx=12, pady=(0, 10), sticky="w")
        ctk.CTkRadioButton(frame, text="Seleziona:",
                           variable=self.cat_mode_var, value="select",
                           command=self._on_cat_mode_change).grid(row=1, column=1, padx=4, pady=(0, 10), sticky="w")

        self.cat_menu = ctk.CTkOptionMenu(frame, values=["—"], width=140,
                                          command=self._on_cat_select, state="disabled")
        self.cat_menu.grid(row=1, column=2, padx=4, pady=(0, 10))

        ctk.CTkLabel(frame, text="/").grid(row=1, column=3, padx=2)

        self.subcat_menu = ctk.CTkOptionMenu(frame, values=["—"], width=140, state="disabled")
        self.subcat_menu.grid(row=1, column=4, padx=(4, 12), pady=(0, 10))

    def _build_run_section(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=3, column=0, padx=12, pady=8, sticky="ew")

        self.run_btn = ctk.CTkButton(
            frame, text="Genera Report", height=46,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self._run
        )
        self.run_btn.pack(fill="x", padx=4)

    def _build_log_section(self):
        frame = ctk.CTkFrame(self)
        frame.grid(row=4, column=0, padx=12, pady=(4, 12), sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="Log", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, padx=12, pady=(10, 4), sticky="w"
        )
        self.log_box = ctk.CTkTextbox(frame, state="disabled", font=ctk.CTkFont(size=12))
        self.log_box.grid(row=1, column=0, padx=12, pady=(0, 10), sticky="nsew")

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _log(self, msg):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")
        self.update_idletasks()

    def _browse_json(self):
        path = filedialog.askopenfilename(
            title="Seleziona il file JSON del corpus",
            filetypes=[("JSON files", "*.json"), ("Tutti i file", "*.*")]
        )
        if path:
            self.json_path_var.set(path)
            self._load_json(path)

    def _load_json(self, path):
        try:
            self.data = load_data(path)
            self.structure = inspect_json(self.data)
            self._update_corpus_info()
            self._update_category_menus()
            self._log(f"JSON caricato: {path}")
        except Exception as e:
            self._log(f"ERRORE caricamento JSON: {e}")

    def _update_corpus_info(self):
        langs = list(self.structure.keys())
        lines = [f"Corpus: {len(langs)} {'lingua' if len(langs) == 1 else 'lingue'}"]
        for lang, groups in self.structure.items():
            parts = [f"{grp}({len(subs)} sub-cat)" for grp, subs in groups.items()]
            lines.append(f"  {lang}: " + ",  ".join(parts))

        self.corpus_info.configure(state="normal")
        self.corpus_info.delete("1.0", "end")
        self.corpus_info.insert("1.0", "\n".join(lines))
        self.corpus_info.configure(state="disabled")

    def _update_category_menus(self):
        lang = self.lang_var.get()
        if lang == "all":
            merged = {}
            for groups in self.structure.values():
                for grp, subs in groups.items():
                    merged.setdefault(grp, set()).update(subs)
            cats = sorted(merged.keys())
        else:
            cats = sorted(self.structure.get(lang, {}).keys())

        if cats:
            self.cat_menu.configure(values=cats)
            self.cat_menu.set(cats[0])
            self._on_cat_select(cats[0])
        else:
            self.cat_menu.configure(values=["—"])
            self.cat_menu.set("—")
            self.subcat_menu.configure(values=["—"])
            self.subcat_menu.set("—")

    def _on_lang_change(self):
        self._update_category_menus()

    def _on_cat_mode_change(self):
        state = "normal" if self.cat_mode_var.get() == "select" else "disabled"
        self.cat_menu.configure(state=state)
        self.subcat_menu.configure(state=state)

    def _on_cat_select(self, selected_cat):
        lang = self.lang_var.get()
        subs: set = set()
        if lang == "all":
            for groups in self.structure.values():
                subs.update(groups.get(selected_cat, []))
        else:
            subs = set(self.structure.get(lang, {}).get(selected_cat, []))

        subs_list = sorted(subs)
        if subs_list:
            self.subcat_menu.configure(values=subs_list)
            self.subcat_menu.set(subs_list[0])
        else:
            self.subcat_menu.configure(values=["—"])
            self.subcat_menu.set("—")

    def _run(self):
        if self.data is None:
            self._log("ERRORE: nessun file JSON caricato.")
            return

        selected_indices = [name for name, var in self.index_vars.items() if var.get()]
        if not selected_indices:
            self._log("ATTENZIONE: seleziona almeno un indice.")
            return

        if not self.fmt_csv.get() and not self.fmt_excel.get():
            self._log("ATTENZIONE: seleziona almeno un formato di output (CSV o Excel).")
            return

        lang = self.lang_var.get()
        process_all = self.cat_mode_var.get() == "all"
        category = None if process_all else self.cat_menu.get()
        sub_category = None if process_all else self.subcat_menu.get()

        self.run_btn.configure(state="disabled", text="Generazione in corso…")
        self.update()

        try:
            if self.fmt_csv.get():
                generate_csv_report(
                    self.data, selected_indices, lang,
                    process_all, category, sub_category,
                    log_fn=self._log
                )
            if self.fmt_excel.get():
                generate_excel_report(
                    self.data, selected_indices, lang,
                    process_all, category, sub_category,
                    log_fn=self._log
                )
            self._log("Fatto.")
        except Exception as e:
            self._log(f"ERRORE: {e}")
        finally:
            self.run_btn.configure(state="normal", text="Genera Report")


if __name__ == "__main__":
    app = App()
    app.mainloop()
