import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from src.plctranslator.tia_translator import check
import src.plctranslator.tia_translator as tia_translator
def velg_kildefil():
    filsti = filedialog.askopenfilename(filetypes=[("SCL files", "*.scl")])
    if filsti:
        kildefil_var.set(filsti)
        # Anta at check() er en funksjon som tar filstien som argument og returnerer True eller False
        if check(filsti):
            status_label.config(text="Konvertering er mulig", bg='green')
            konverter_btn.config(state="normal")
        else:
            status_label.config(text="Konvertering er ikke mulig", bg='red')
            konverter_btn.config(state="disabled")

def velg_malmappe():
    mappesti = filedialog.askdirectory()
    if mappesti:
        malmappe_var.set(mappesti)
        sjekk_konvertering()

def sjekk_konvertering():
    kildefil = kildefil_var.get()
    malmappe = malmappe_var.get()
    print("Kildefil: "+kildefil+"\n"+"Målmappe:"+ malmappe)
    # Implementer logikk for å faktisk sjekke om konvertering er mulig her
    # For eksempel:
    er_mulig = kildefil != "" and malmappe != ""
    
    if er_mulig:
        status_label.config(text="Konvertering er mulig", bg='green')
        konverter_btn.config(state="normal")
    else:
        status_label.config(text="Konvertering er ikke mulig", bg='red')
        konverter_btn.config(state="disabled")

def konverter():
    # Kall din konverteringsfunksjon her
    # Fra src/plctranslator/tia_translator.py: translate(read_scl_file(scl_file_path), new_file_path_tc)
    fulltext = tia_translator.read_scl_file(kildefil_var.get())
    tia_translator.translate(fulltext, malmappe_var.get())
    messagebox.showinfo("Suksess", "Konvertering startet!")

root = tk.Tk()
root.title("SCL til TwinCAT Konverterer")
root.geometry("500x300")

kildefil_var = tk.StringVar()
malmappe_var = tk.StringVar()

tk.Label(root, text="Velg kildefil:").pack()
tk.Entry(root, textvariable=kildefil_var, state='readonly').pack()
tk.Button(root, text="Bla gjennom...", command=velg_kildefil).pack()

tk.Label(root, text="Velg målmappe:").pack()
tk.Entry(root, textvariable=malmappe_var, state='readonly').pack()
tk.Button(root, text="Bla gjennom...", command=velg_malmappe).pack()

status_label = tk.Label(root, text="Venter på input...", bg='gray')
status_label.pack(fill=tk.X)

konverter_btn = tk.Button(root, text="Konverter", command=konverter, state="disabled")
konverter_btn.pack()

root.mainloop()
