"""This module contains the GUI code for the PLC Translator."""

import logging
import logging.config
from tkinter import Text, filedialog
import customtkinter as ctk  # type : ignore
import os



import src.plctranslator.tia_helpers as tia_helpers  # noqa: PLR0402
import src.plctranslator.tia_translator as tia_translator  # noqa: PLR0402
from config.config import get_config

_CONFIG = get_config()

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
            converting_btn.configure(state="disabled")
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
    is_possible = (sourcefile != "") and (destinationfolder !="") and tia_translator.check(tia_helpers.read_scl_file(sourcefile))
    tia_translator.log_stream.truncate()
    tia_translator.log_stream.seek(0)
    if is_possible:
        converting_btn.configure(state="normal")
        open_file_explorer_button.configure(state="normal")
        show_full_info_button.configure(state="normal")



def converter():
    """Converts the source file to the target folder."""
    fulltext = tia_helpers.read_scl_file(sourcefile_var.get())
    tia_translator.translate(fulltext, destinationfolder_var.get())
    end_index = textbox.index(ctk.END)
    lines = textbox.get("1.0", end_index).count("\n")
    textbox.insert(float(lines), tia_translator.log_stream.getvalue())
    tia_translator.log_stream.truncate()
    tia_translator.log_stream.seek(0)
    status_label.configure(text="Convertion successful", fg_color="magenta" )
    converting_btn.configure(state="disabled")


def open_file_explorer_destenation_folder():
    """Opens the file explorer to the destination folder."""
    sourcefile = sourcefile_var.get()
    destinationfolder = destinationfolder_var.get()
    is_possible = (sourcefile != "") and (destinationfolder !="") and tia_translator.check(tia_helpers.read_scl_file(sourcefile))
    if is_possible:
        os.startfile(destinationfolder_var.get())


def show_full_info_from_converting():
    """Shows the full info from the converting in the textbox."""
    fulltext = tia_helpers.read_scl_file(sourcefile_var.get())
    sourcefile = sourcefile_var.get()
    destinationfolder = destinationfolder_var.get()
    is_possible = (sourcefile != "") and (destinationfolder !="") and tia_translator.check(tia_helpers.read_scl_file(sourcefile))
    if is_possible:
        textbox.delete("1.0", "end")
        textbox.insert("1.0", fulltext)
    print(fulltext)
    tia_translator.log_stream.truncate()


root = ctk.CTk()
root.title("Goodtech TIA to TwinCAT Translator")
script_dir = os.path.dirname(__file__)  # Henter mappen hvor scriptet ligger
icon_path = "final_gt_ico.ico"
try:
    root.iconbitmap(icon_path)
except Exception as e:
    print(f"Feil ved setting av ikon: {e}")

root.geometry("850x500")  # Oppdatert for ekstra plass
root.resizable(width=True, height=True)
root.minsize(850, 500)


# Opprette rammer for layout-separasjon
left_top_frame = ctk.CTkFrame(master=root)
left_top_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)


left_btm_f = ctk.CTkFrame(master=left_top_frame)
left_btm_f.pack(side=ctk.BOTTOM, fill=ctk.BOTH, expand=True)

left_btm_f_L = ctk.CTkFrame(master=left_btm_f)
left_btm_f_L.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
left_btm_f_R = ctk.CTkFrame(master=left_btm_f)
left_btm_f_R.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)



right_frame = ctk.CTkFrame(master=root)
right_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)


sourcefile_var = ctk.StringVar()
destinationfolder_var = ctk.StringVar()


"""Left frame"""
# sourcefile part
ctk.CTkLabel(left_top_frame, text="Choose sourcefile:").pack(pady=10)
ctk.CTkEntry(left_top_frame, textvariable=sourcefile_var, state="readonly").pack()
ctk.CTkButton(left_top_frame, text="Browse", command=choose_sourcefile).pack()

# destination folder part
ctk.CTkLabel(left_top_frame, text="Choose destination folder:").pack(padx=10)
ctk.CTkEntry(left_top_frame, textvariable=destinationfolder_var, state="readonly").pack()
ctk.CTkButton(left_top_frame, text="Browse", command=choose_destinationfolder).pack(padx=20)


# Statuslabel for converting, if possible or not
status_label = ctk.CTkLabel(left_top_frame, text="Waiting For Input", fg_color="gray")
status_label.pack(fill=ctk.X, pady=40, padx=5)

# Convert button
converting_btn = ctk.CTkButton(left_top_frame, text="Convert", command=converter, state="disabled")
converting_btn.pack(pady=3)


# Open file explorer button
open_file_explorer_button = ctk.CTkButton(left_btm_f_L, text="Open destination folder", command=open_file_explorer_destenation_folder,state="disabled")
open_file_explorer_button.pack(pady=25)


# Show full info from converting
show_full_info_button = ctk.CTkButton(left_btm_f_R, text="Show convertion result", command=show_full_info_from_converting, state="disabled")
show_full_info_button.pack(pady=25)


# clear button
clear_button = ctk.CTkButton(left_btm_f_L, text="Clear", command=lambda: textbox.delete("1.0", "end"))
clear_button.pack()


# Exit button
exit_button = ctk.CTkButton(left_btm_f_R, text="Exit", command=root.quit)
exit_button.pack()




"""Right frame"""
# Label for right_frame
ctk.CTkLabel(right_frame, text="Output window for checks:").pack(pady=10)

# Textboks in right_frame
textbox = Text(right_frame, height=20, width=50)
textbox.pack(fill=ctk.BOTH, expand=True, padx=(0,10), pady=(0,10))


root.mainloop()
