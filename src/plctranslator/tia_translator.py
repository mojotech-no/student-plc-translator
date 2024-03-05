"""This module contains functions for converting SCL files."""

import re
import sys
from pathlib import Path

from klasser_skisse import SCLConvertion, Tcdut


def read_scl_file(scl_file_path: str) -> None:
    """Read the SCL file from the given file path and store the content in SCLConvertion.SCL_Full_Text."""
    try:
        with Path(scl_file_path).open(encoding="utf-8-sig") as fil:
            SCLConvertion.SCL_Full_Text = fil.read()
    except FileNotFoundError:
        print(f"Filen {scl_file_path} ble ikke funnet.")
        sys.exit(1)
    except Exception as e:
        print(f"En uventet feil oppstod: {e}")


def generate_variable_text() -> None:
    """Generate the variable text from the SCL file."""
    start_index = SCLConvertion.SCL_Full_Text.find("VAR_INPUT")
    stop_index = SCLConvertion.SCL_Full_Text.find("BEGIN")

    SCLConvertion.variable_text1 = SCLConvertion.SCL_Full_Text[start_index + len("VAR_INPUT") : stop_index].strip()


def generate_code() -> None:
    """Generate the code from the SCL file."""
    start_index = SCLConvertion.SCL_Full_Text.find("BEGIN")
    stop_index = SCLConvertion.SCL_Full_Text.find("END_FUNCTION_BLOCK")

    SCLConvertion.SCL_Code = SCLConvertion.SCL_Full_Text[start_index + len("VAR_INPUT") : stop_index].strip()
    SCLConvertion.SCL_Code = SCLConvertion.SCL_Code.replace(" #", "")
    SCLConvertion.SCL_Code = SCLConvertion.SCL_Code.replace("(#", "")
    SCLConvertion.SCL_Code = SCLConvertion.SCL_Code.replace("\t#", "\t")


def find_project_name() -> None:
    """Find and store the project name from the SCL file."""
    linjer = SCLConvertion.SCL_Full_Text.split("\n")
    for i in range(len(linjer)):  #
        if "FUNCTION_BLOCK " in linjer[i]:
            start_index = linjer[i].find('"')
            stop_index = linjer[i].find('"', 16)
            SCLConvertion.project_name = linjer[i][start_index + 1 : stop_index]


def generate_dut_list() -> None:
    """Generate the dut list from the SCL file."""
    stop_index = SCLConvertion.SCL_Full_Text.find("FUNCTION_BLOCK")
    dut_text: str = SCLConvertion.SCL_Full_Text[:stop_index].strip()
    dut_list: list[str] = re.split(r"END_TYPE", dut_text)

    for dut in dut_list[:-1]:
        dutcode = dut
        dutcode += "\nEND_TYPE"
        dutcode = dutcode.replace("VERSION : 0.1", "")
        dutcode = dutcode.replace("\n\n", "")
        stopp_index = dutcode.find('"', 6)
        dut_name = dutcode[6:stopp_index]
        dutcode = dutcode[: stopp_index + 1] + " :\n" + dutcode[stopp_index + 1 :]  # Legger til en linje etter navnet

        lines = dutcode.split("\n")
        lines[0] = lines[0].replace(";", "")

        for line in range(len(lines)):
            if "END_STRUCT" in lines[line]:
                lines[line] = lines[line].replace(";", "")

        dutcode = "\n".join(lines)
        SCLConvertion.dut_list.append(Tcdut(dut_name, dutcode))


def generate_dut_files(file_path):
    """Generate the dut files based on the provided file path."""
    for dut in SCLConvertion.dut_list:
        filsti = rf"{file_path}\{dut.name}.Tcdut"
        with Path(filsti).open("w", encoding="utf-8-sig") as file:
            file.write(dut.header())
            file.write(dut.code)
            file.write(dut.footer)


def generate_tcpou_file(folder_path):
    """Generate the TcPOU file based on the provided folder path."""
    filsti = rf"{folder_path}\{SCLConvertion.project_name}.TcPOU"
    with Path(filsti).open("w", encoding="UTF-8") as file:
        file.write(SCLConvertion.header())
        file.write(SCLConvertion.variable_text())
        file.write(SCLConvertion.code())


def find_all_ton_variables_and_append_to_ton_list() -> None:
    """Convert the TON function to a TcPOU file."""
    variable_lines = SCLConvertion.variable_text().split("\n")
    for line in variable_lines:
        if "TON" in line:
            words = line.split()
            SCLConvertion.ton_names.append(words[0])


def get_the_ton_function_in_text(text, ton_word_list):
    """Get the TON function from the text file."""
    # Sjekk om listen allerede inneholder elementer for å unngå overskriving
    if not hasattr(SCLConvertion, "ton_function"):
        SCLConvertion.unconverted_ton_function = []

    for ton_word in ton_word_list:
        start_index = text.find(ton_word)
        if start_index != -1:  # Sjekker om søkeordet finnes.
            semicolon_index = text.find(";", start_index)
            if semicolon_index != -1:
                # Legger til teksten fra søkeordet til og med semikolonet i listen.
                SCLConvertion.unconverted_ton_function.append(text[start_index : semicolon_index + 1])
            else:
                # Legger til resten av teksten fra søkeordet hvis det ikke finnes et semikolon.
                SCLConvertion.unconverted_ton_function.append(text[start_index:])

    if not SCLConvertion.unconverted_ton_function:  # Hvis listen er tom, betyr det at ingen ton ord ble funnet.
        return ["Søkeordene ble ikke funnet i teksten."]

    return SCLConvertion.unconverted_ton_function


def convert_ton_function_to_twincat_ton(ton_functions: list[str]) -> None:
    """Convert the TON function to a TcPOU file and append to the converted_ton_functions list."""
    for ton in ton_functions:
        converted_ton = ""
        lines = ton.split("\n")  # Anta at hver ton er en lang streng som trenger å bli splittet i linjer.
        for line in lines:
            if "PT" in line:
                index = line.find(":=")
                if index != -1:
                    converted_line = line[: index + 2] + " real_to_time(" + line[index + 2 :].strip() + "*1000.0);"
                    converted_ton += converted_line + "\n"
                else:
                    converted_ton += line + "\n"
            else:
                converted_ton += line + "\n"
        # Legg til den konverterte TON-funksjonen i listen etter hver TON er behandlet.
        SCLConvertion.converted_ton_functions.append(converted_ton)


def replace_ton_diffences() -> None:
    """Replace the TON differences."""
    for i in range(len(SCLConvertion.unconverted_ton_function)):
        SCLConvertion.SCL_Code = SCLConvertion.SCL_Code.replace(
            SCLConvertion.unconverted_ton_function[i], SCLConvertion.converted_ton_functions[i]
        )


def main() -> None:
    """Entry point of the program."""
    scl_file_path = r"C:\Users\47974\Desktop\Tia SCL FILER\MOJO_MB_V2.scl"
    new_file_path_tcpou = r"C:\Users\47974\Documents\TcXaeShell\TwinCAT Project1\TwinCAT Project1\Untitled2\POUs"
    new_file_path_tcdut = r"C:\Users\47974\Documents\TcXaeShell\TwinCAT Project1\TwinCAT Project1\Untitled2\duts"

    # scl_file_path = r"C:\Users\jomar\OneDrive\Skrivebord\TIA Bachelor\MOJO_SBE_Error_Function_V2.scl"
    # new_file_path_tcpou = r"C:\Users\jomar\OneDrive\Dokumenter\TcXaeShell\hello world\hello world\HelloWorldPLC\POUs"
    # new_file_path_tcdut = r"C:\Users\jomar\OneDrive\Dokumenter\TcXaeShell\hello world\hello world\HelloWorldPLC\DUTs"

    read_scl_file(scl_file_path)
    generate_variable_text()
    generate_code()
    # New code-------------------------------
    find_all_ton_variables_and_append_to_ton_list()
    get_the_ton_function_in_text(SCLConvertion.code(), SCLConvertion.ton_names)
    convert_ton_function_to_twincat_ton(SCLConvertion.unconverted_ton_function)
    replace_ton_diffences()
    # New code end---------------------------
    find_project_name()
    generate_dut_list()
    generate_tcpou_file(new_file_path_tcpou)
    generate_dut_files(new_file_path_tcdut)


if __name__ == "__main__":
    main()
