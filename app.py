"""This module contains the GUI code for the PLC Translator."""

import logging
import logging.config
from tkinter import Text, filedialog

import customtkinter as ctk  # type : ignore

import src.plctranslator.tia_helpers as tia_helpers  # noqa: PLR0402
import src.plctranslator.tia_translator as tia_translator  # noqa: PLR0402
from config.config import get_config

_CONFIG = get_config()
_LOGGER = logging.getLogger(__name__)
if _CONFIG.logging is not None:
    logging.config.dictConfig(_CONFIG.logging)

ctk.set_appearance_mode("dark")  # "Dark" eller "Light"
ctk.set_default_color_theme("dark-blue")  # Endre temaet etter behov


def choose_sourcefile():
    """Open a file dialog to select a source file."""
    filepath = filedialog.askopenfilename(filetypes=[("SCL files", "*.scl")])
    if filepath:
        sourcefile_var.set(filepath)
        if tia_translator.check(tia_helpers.read_scl_file(filepath)):
            print(tia_translator.log_stream.getvalue())
            status_label.configure(text="Convertion is possible", fg_color="green")  # Endret fra config til configure
            # Tømmer textboxen før ny tekst legges til
            textbox.delete("1.0", "end")

            # Anta at `resultat` er teksten du ønsker å vise i textboxen. Hvis funksjonen
            # `translate` returnerer teksten du vil vise, kan du bruke den direkte. Ellers,
            # erstatte `resultat` med riktig variabel eller streng du vil vise.
            textbox.insert("1.0", tia_translator.log_stream.getvalue())
            tia_translator.log_stream.truncate()
            tia_translator.log_stream.seek(0)

        else:
            textbox.delete("1.0", "end")
            status_label.configure(text="Convertion is not possible", fg_color="red")  # Endret fra config til configure
            konverter_btn.configure(state="disabled")
            textbox.insert("1.0", tia_translator.log_stream.getvalue())
            tia_translator.log_stream.truncate()
            tia_translator.log_stream.seek(0)

    check_convertion()


def choose_destinationfolder():
    """Open a file dialog to select a target folder."""
    mappesti = filedialog.askdirectory()
    if mappesti:
        destinationfolder_var.set(mappesti)
        check_convertion()


def check_convertion():
    """Check if conversion is possible based on the selected source file and target folder."""
    sourcefile = sourcefile_var.get()
    destinationfolder = destinationfolder_var.get()
    is_possible = (
        (sourcefile != "") and (destinationfolder != "") and tia_translator.check(tia_helpers.read_scl_file(sourcefile))
    )

    if is_possible:
        konverter_btn.configure(state="normal")


def konverter():
    """Converts the source file to the target folder."""
    fulltext = tia_helpers.read_scl_file(sourcefile_var.get())
    tia_translator.translate(fulltext, destinationfolder_var.get())
    end_index = textbox.index(ctk.END)
    lines = textbox.get("1.0", end_index).count("\n")
    textbox.insert(float(lines), tia_translator.log_stream.getvalue())
    tia_translator.log_stream.truncate()
    tia_translator.log_stream.seek(0)
    status_label.configure(text="Convertion successful", fg_color="magenta")
    konverter_btn.configure(state="disabled")


root = ctk.CTk()
root.title("Tia Portal to TwinCAT converter")
root.geometry("850x350")  # Oppdatert for ekstra plass
root.resizable(width=False, height=False)

# Opprette rammer for layout-separasjon
left_frame = ctk.CTkFrame(master=root)
left_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

right_frame = ctk.CTkFrame(master=root)
right_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)

sourcefile_var = ctk.StringVar()
destinationfolder_var = ctk.StringVar()

# sourcefile part
ctk.CTkLabel(left_frame, text="Choose sourcefile:").pack(pady=(10, 0), padx=20)
ctk.CTkEntry(left_frame, textvariable=sourcefile_var, state="readonly").pack()
ctk.CTkButton(left_frame, text="Browse", command=choose_sourcefile).pack()

# destination folder part
ctk.CTkLabel(left_frame, text="Choose destination folder:").pack(padx=20)
ctk.CTkEntry(left_frame, textvariable=destinationfolder_var, state="readonly").pack()
ctk.CTkButton(left_frame, text="Browse", command=choose_destinationfolder).pack(padx=30)

# Textboks in right_frame
textbox = Text(right_frame, height=20, width=50)
textbox.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

status_label = ctk.CTkLabel(left_frame, text="Waiting For Input", fg_color="gray", padx=20)
status_label.pack(fill=ctk.X, pady=15)

konverter_btn = ctk.CTkButton(left_frame, text="Convert", command=konverter, state="disabled")
konverter_btn.pack()

root.mainloop()
