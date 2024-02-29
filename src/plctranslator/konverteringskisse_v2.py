"""This module contains functions for reading and generating code from SCL files."""

import re
import sys

from klasser_skisse import SCLConvertion, Tcdut


def read_scl_file(scl_file_path: str) -> None:
    """Read the SCL file from the given file path and store the content in SCLConvertion.SCL_Full_Text."""
    try:
        with open(scl_file_path, encoding="utf-8-sig") as fil:
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
    SCLConvertion.SCL_Code = SCLConvertion.SCL_Code.replace("#", "")


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
            dut += "\nEND_TYPE"
            dut = dut.replace("VERSION : 0.1", '')
            dut = dut.replace("\n\n", '')
            stopp_index = dut.find('"', 6)
            dut_name = dut[6:stopp_index]
            dut = dut[:stopp_index+1] + " :\n" + dut[stopp_index+1:]                #Legger til en linje etter navnet

            lines = dut.split('\n')
            lines[0] = lines[0].replace(';', '')
            lines[0] = lines[0].replace('"','')

            for line in range(len(lines)):
                if "END_STRUCT" in lines[line]:
                    lines[line] = lines[line].replace(';', '')
                    

            dut = '\n'.join(lines)
            SCLConvertion.dut_list.append(Tcdut(dut_name,dut))


def generate_dut_files(file_path):
    """Generate the dut files based on the provided file path."""
    for dut in SCLConvertion.dut_list:
        filsti = rf"{file_path}\{dut.name}.Tcdut"
        with open(filsti, "w", encoding="utf-8-sig") as file:
            file.write(dut.header())
            file.write(dut.code)
            file.write(dut.footer)
            


def generate_tcpou_file(folder_path):
    """Generate the TcPOU file based on the provided folder path."""
    filsti = rf"{folder_path}\{SCLConvertion.project_name}.TcPOU"
    with open(filsti, "w", encoding="UTF-8") as file:
        file.write(SCLConvertion.header())
        file.write(SCLConvertion.variable_text())
        file.write(SCLConvertion.code())


def find_all_ton_variables_and_append_to_ton_list() -> None:
    """Convert the TON function to a TcPOU file."""
    variable_lines = SCLConvertion.variable_text().split("\n")
    for line in variable_lines:
        if "TON" in line:
            words = line.split()
            SCLConvertion.ton_list.append(words[0])


def main() -> None:
    """Entry point of the program."""
    scl_file_path = r"C:\Users\47974\Desktop\Tia SCL FILER\MOJO_MB_V2.scl"
    scl_file_path = r"C:\Users\47974\Desktop\Tia SCL FILER\MOJO_MB_V2.scl"
    new_file_path_tcpou = r"C:\Users\47974\Documents\TcXaeShell\TwinCAT Project1\TwinCAT Project1\Untitled2\POUs"
    new_file_path_tcdut = r"C:\Users\47974\Documents\TcXaeShell\TwinCAT Project1\TwinCAT Project1\Untitled2\duts"
    

    read_scl_file(scl_file_path)
    generate_variable_text()
    generate_code()
    find_project_name()
    generate_dut_list()
    generate_tcpou_file(new_file_path_tcpou)
    generate_dut_files(new_file_path_tcdut)


if __name__ == "__main__":
    main()
