"""This module contains functions for reading and generating code from SCL files."""

import re
from pathlib import Path

from plctranslator.tc_helpers import Tcdut
from plctranslator.tia_helpers import SCLConvertion, read_scl_file


def generate_variable_text(full_text: str) -> str:
    """Collect the variable declaration text from the SCL file.

    Args:
        full_text (str): The full text of the SCL file.

    Returns:
        str: The variable declaration text extracted from the SCL file.
    """
    return full_text[full_text.find("VAR_INPUT") + len("VAR_INPUT") : full_text.find("BEGIN") - len("BEGIN")].strip()


def generate_code(full_text: str) -> str:
    """Collect the code section from the SCL file.

    Args:
        full_text (str): The full text of the SCL file.

    Returns:
        str: The code section.
    """
    try:
        start_index = full_text.find("BEGIN") + len("VAR_INPUT")
        end_index = full_text.find("END_FUNCTION_BLOCK")
        code_section = full_text[start_index:end_index].strip().replace("#", "")
        return code_section
    except Exception as err:
        raise ValueError("The code section could not be extracted from the SCL file.") from err


def find_project_name(full_text: str) -> str:
    """Find and store the project name from the SCL file.

    Args:
        full_text (str): The full text of the SCL file.

    Returns:
        str: The project name extracted from the SCL file.
    """
    project_name = None
    for line in full_text.split("\n"):
        if "FUNCTION_BLOCK " in line:
            start_index = line.find('"')
            stop_index = line.find('"', 16)
            project_name = line[start_index + 1 : stop_index]

    if project_name is None:
        raise ValueError("Project name not found in the SCL file.")
    else:
        return project_name


def generate_dut_list(full_text: str) -> list[Tcdut]:
    """Generate the dut list from the SCL file.

    Args:
        full_text (str): The full text of the SCL file.

    Returns:
        list[Tcdut]: The list of Tcdut objects representing the DUTs extracted from the SCL file.

    Raises:
        ValueError: If no DUTs are found in the SCL file.
    """
    udt_text: str = full_text[: full_text.find("FUNCTION_BLOCK")].strip()
    udt_list: list[str] = re.split(r"END_TYPE", udt_text)
    dut_list: list[Tcdut] | None = None

    for udt in udt_list[:-1]:
        dut = udt
        dut += "\nEND_TYPE"
        dut = dut.replace("VERSION : 0.1", "")
        dut = dut.replace("\n\n", "")
        stopp_index = dut.find('"', 6)
        dut_name = dut[6:stopp_index]
        dut = dut[: stopp_index + 1] + " :\n" + dut[stopp_index + 1 :]

        lines = dut.split("\n")
        lines[0] = lines[0].replace(";", "")

        for line in range(len(lines)):
            if "END_STRUCT" in lines[line]:
                lines[line] = lines[line].replace(";", "")

        dut = "\n".join(lines)
        if dut_list is None:
            dut_list = [Tcdut(dut_name, dut)]
        else:
            dut_list.append(Tcdut(dut_name, dut))

    if dut_list is None:
        raise ValueError("No DUTs found in the SCL file.")
    else:
        return dut_list


def generate_dut_files(folder_path: str, dut_list: list[Tcdut]) -> None:
    """Generate the DUT (TC Data Unit Type) files based on the provided folder path.

    Args:
        folder_path (str): The path to the folder where the DUT files will be generated.
        dut_list (list[Tcdut]): The list of Tcdut objects representing the DUTs.

    Returns:
        None
    """
    for dut in dut_list:
        file_path = rf"{folder_path}\{dut.name}.Tcdut"
        with Path(file_path).open(mode="w", encoding="utf-8-sig") as file:
            file.write(dut.header())
            file.write(dut.code)
            file.write(dut.footer)


def generate_tcpou_file(folder_path: str, project_name: str, header: str, variable_text: str, code: str) -> None:
    """Generate the TcPOU file based on the provided folder path.

    Args:
        folder_path (str): The path to the folder where the TcPOU file will be generated.
        project_name (str): The name of the project.
        header (str): The header text to be written in the TcPOU file.
        variable_text (str): The variable decleration text to be written in the TcPOU file.
        code (str): The code section to be written in the TcPOU file.

    Returns:
        None
    """
    file_path = rf"{folder_path}\{project_name}.TcPOU"
    with Path(file_path).open(mode="w", encoding="UTF-8") as file:
        file.write(header)
        file.write(variable_text)
        file.write(code)


def make_ton_list() -> None:
    """Make a TON function block."""
    lines = SCLConvertion.variable_text().split("\n")  # Split the text into lines
    for line in lines:
        if "ton" in line.lower():  # Check if the line contains the word "ton"
            line = line.strip()
            line = line.split("\t")[0]
            SCLConvertion.ton_names.append(line.strip())


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


def writes_out_scl_ton_functions():
    """Write out the TON functions that needs to be converted."""
    get_the_ton_function_in_text(SCLConvertion.code(), SCLConvertion.ton_names)
    for i in SCLConvertion.unconverted_ton_function:
        print(i)


def main() -> None:
    """Entry point of the program."""
    # scl_file_path = r"C:\Users\47974\Desktop\Tia SCL FILER\MOJO_MB_V2.scl"
    # scl_file_path = r"C:\Users\47974\Desktop\Tia SCL FILER\MOJO_MB_V2.scl"
    # new_file_path_tcpou = r"C:\Users\47974\Documents\TcXaeShell\TwinCAT Project1\TwinCAT Project1\Untitled2\POUs"
    # new_file_path_tcdut = r"C:\Users\47974\Documents\TcXaeShell\TwinCAT Project1\TwinCAT Project1\Untitled2\duts"

    scl_file_path = r"C:\Users\jomar\OneDrive\Skrivebord\TIA Bachelor\MOJO_SBE_Error_Function_V2.scl"
    new_file_path_tcpou = r"C:\Users\jomar\OneDrive\Dokumenter\TcXaeShell\hello world\hello world\HelloWorldPLC\POUs"
    new_file_path_tcdut = r"C:\Users\jomar\OneDrive\Dokumenter\TcXaeShell\hello world\hello world\HelloWorldPLC\DUTs"

    read_scl_file(scl_file_path)
    generate_variable_text()
    generate_code()
    # New code-------------------------------
    make_ton_list()
    writes_out_scl_ton_functions()  # Writes out the TON functions that needs to be converted, not necessary
    get_the_ton_function_in_text(SCLConvertion.code(), SCLConvertion.ton_names)
    convert_ton_function_to_twincat_ton(SCLConvertion.unconverted_ton_function)
    # New code end---------------------------
    find_project_name()
    generate_dut_list()
    generate_tcpou_file(new_file_path_tcpou)
    generate_dut_files(new_file_path_tcdut)


if __name__ == "__main__":
    main()
