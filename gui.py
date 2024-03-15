import customtkinter as ctk
from tkinter import filedialog, Text, messagebox
import src.plctranslator.tia_translator as tia_translator
import src.plctranslator.tia_helpers as tia_helpers
import logging
import logging.config
from config.config import get_config

_CONFIG = get_config()
_LOGGER = logging.getLogger(__name__)
if _CONFIG.logging is not None:
    logging.config.dictConfig(_CONFIG.logging)

ctk.set_appearance_mode("dark")  # "Dark" eller "Light"
ctk.set_default_color_theme("dark-blue")  # Endre temaet etter behov

def velg_kildefil():
    filsti = filedialog.askopenfilename(filetypes=[("SCL files", "*.scl")])
    if filsti:
        kildefil_var.set(filsti)
        if tia_translator.check(filsti):
            status_label.configure(text="Konvertering er mulig", fg_color='green')  # Endret fra config til configure
            # Tømmer tekstboksen før ny tekst legges til
            tekstboks.delete("1.0", "end")

            # Anta at `resultat` er teksten du ønsker å vise i tekstboksen. Hvis funksjonen
            # `translate` returnerer teksten du vil vise, kan du bruke den direkte. Ellers,
            # erstatte `resultat` med riktig variabel eller streng du vil vise.
            tekstboks.insert("1.0", tia_translator.log_stream.getvalue())
            
        else:
            status_label.configure(text="Konvertering er ikke mulig", fg_color='red')  # Endret fra config til configure
            konverter_btn.configure(state="disabled")


def velg_malmappe():
    mappesti = filedialog.askdirectory()
    if mappesti:
        malmappe_var.set(mappesti)
        sjekk_konvertering()

def sjekk_konvertering():
    kildefil = kildefil_var.get()
    malmappe = malmappe_var.get()
    er_mulig = kildefil != None and malmappe != None
    
    if er_mulig:
        status_label.configure(text="Konvertering er mulig", fg_color='green')
        konverter_btn.configure(state="normal")
    else:
        status_label.configure(text="Konvertering er ikke mulig", fg_color='red')
        konverter_btn.configure(state="disabled")

def konverter():
    fulltext = tia_helpers.read_scl_file(kildefil_var.get())
    resultat = tia_translator.translate(fulltext, malmappe_var.get())
    end_index = tekstboks.index(ctk.END)
    lines = tekstboks.get("1.0", end_index).count("\n")
    tekstboks.insert(float(lines), tia_translator.log_stream.getvalue())
    messagebox.showinfo("Suksess", "Konvertering startet!")


root = ctk.CTk()
root.title("SCL til TwinCAT Konverterer")
root.geometry("850x350")  # Oppdatert for ekstra plass
root.resizable(width=False, height=False)

# Opprette rammer for layout-separasjon
left_frame = ctk.CTkFrame(master=root)
left_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

right_frame = ctk.CTkFrame(master=root)
right_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)

kildefil_var = ctk.StringVar()
malmappe_var = ctk.StringVar()

# Kildefil-delen
ctk.CTkLabel(left_frame, text="Velg kildefil:").pack(pady=(10, 0), padx=20)
ctk.CTkEntry(left_frame, textvariable=kildefil_var, state='readonly').pack()
ctk.CTkButton(left_frame, text="Bla gjennom...", command=velg_kildefil).pack()

# Målmappe-delen
ctk.CTkLabel(left_frame, text="Velg målmappe:").pack(padx=20)
ctk.CTkEntry(left_frame, textvariable=malmappe_var, state='readonly').pack()
ctk.CTkButton(left_frame, text="Bla gjennom...", command=velg_malmappe).pack(padx=30)

# Tekstboks i right_frame
tekstboks = Text(right_frame, height=20, width=50)
tekstboks.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

status_label = ctk.CTkLabel(left_frame, text="Venter på input...", fg_color='gray', padx=20)
status_label.pack(fill=ctk.X, pady=15)

konverter_btn = ctk.CTkButton(left_frame, text="Konverter", command=konverter, state="disabled")
konverter_btn.pack()

root.mainloop()
