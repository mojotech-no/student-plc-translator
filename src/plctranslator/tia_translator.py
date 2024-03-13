"""This module contains functions for converting SCL files."""

import logging
import re
from pathlib import Path

from plctranslator.tc_helpers import Tcdut
from plctranslator.tia_helpers import SCLConvertion

_LOGGER = logging.getLogger(__name__)


def generate_variable_text(full_text: str) -> str:
    """Generate the variable text from the SCL file."""
    start_index = full_text.find("VAR_INPUT")
    stop_index = full_text.find("BEGIN")
    converted_variable_text = full_text[start_index + len("VAR_INPUT") : stop_index].strip()
    SCLConvertion.variable_text1 = converted_variable_text
    return converted_variable_text



def convert_timers_and_counters_in_variabletext(variable_text: str) -> str:
    """Convert the timers and counters in the variable text."""
    variable_text_lines = variable_text.split("\n")
    for i in range(len(variable_text_lines)):
        if "TON_TIME" in variable_text_lines[i]:
            variable_text_lines[i] = variable_text_lines[i].strip()
            line_words = variable_text_lines[i].split(" ")
            variable_text_lines[i] = variable_text_lines[i].replace(variable_text_lines[i], "\t" + line_words[0] + ": TON;")
        if "TOF_TIME" in variable_text_lines[i]:
            variable_text_lines[i] = variable_text_lines[i].strip()
            line_words = variable_text_lines[i].split(" ")
            variable_text_lines[i] = variable_text_lines[i].replace(variable_text_lines[i], "\t" + line_words[0] + ": TOF;")
        if "TP_TIME" in variable_text_lines[i]:
            variable_text_lines[i] = variable_text_lines[i].strip()
            line_words = variable_text_lines[i].split(" ")
            variable_text_lines[i] = variable_text_lines[i].replace(variable_text_lines[i], "\t" + line_words[0] + ": TP;")
        if "CTU_INT" in variable_text_lines[i]:
            variable_text_lines[i] = variable_text_lines[i].strip()
            line_words = variable_text_lines[i].split(" ")
            variable_text_lines[i] = variable_text_lines[i].replace(variable_text_lines[i], "\t" + line_words[0] + ": CTU;")
    variable_text = "\n".join(variable_text_lines)
    SCLConvertion.variable_text1 = variable_text
    return SCLConvertion.variable_text1


def generate_code(full_text: str) -> str:
    """Generate the code from the SCL file."""
    try:
def check(full_text: str) -> bool:
    """Check the full text."""
    result = True
    _LOGGER.debug("Generating Variable Text...")
    try:
        convert_timers_and_counters_in_variabletext(generate_variable_text(full_text))
    except Exception as err:
        _LOGGER.critical(f"Error in generating variable text. {err}")

    _LOGGER.debug("Generating Variable Text...")

    try:
        generate_code(full_text)
    except Exception as err:
        _LOGGER.critical(f"Error in generating code. {err}")

    _LOGGER.debug("Finding Project Name...")
    try:
        find_project_name(full_text)
    except Exception as err:
        _LOGGER.critical(f"Error in finding project name. {err}")

    try:
        generate_dut_list(full_text)
        _LOGGER.debug(f"Generating DUT List.. dut's found: {len(SCLConvertion.dut_list)}...")
    except Exception as err:
        _LOGGER.critical(f"Error in generating DUT list. {err}")

    potential_converted_tcpou: str = SCLConvertion.header() + SCLConvertion.variable_text1 + SCLConvertion.code()
    potential_converted_dut: str = ""
    for dut in SCLConvertion.dut_list:
        potential_converted_dut += dut.header() + dut.code + dut.footer + "\n\n"

    potential_converted_full_info = potential_converted_dut + potential_converted_tcpou

    error_list = ["TON_TIME", "TOF_TIME", "TP_TIME", "CTU_INT"]
    found_errors = [keyword for keyword in error_list if keyword in potential_converted_full_info]

    if found_errors:
        result = False
        for error in found_errors:
            _LOGGER.error(f"Check Complete: Error found - {error}")
    else:
        _LOGGER.info("Check Complete: No Errors found")

    return result


def translate(full_text: str, new_file_path_tc: str) -> None:
    """Translate the SCL file and generate the TCPou and DUT files."""
    convert_timers_and_counters_in_variabletext(generate_variable_text(full_text))
    generate_code(full_text)
    find_project_name(full_text)
    generate_dut_list(full_text)

    _LOGGER.debug("Generating TcPOU files...")
    try:
        generate_tcpou_file(
            new_file_path_tc,
            SCLConvertion.project_name,
            SCLConvertion.header(),
            SCLConvertion.variable_text(),
            SCLConvertion.code(),
        )
        _LOGGER.info(f"TcPOU file generated successfully in {new_file_path_tc}")
    except Exception as err:
        _LOGGER.critical(f"Error in generating TCPou file. {err}")

    _LOGGER.debug("Generating DUT files...")
    try:
        generate_dut_files(new_file_path_tc, generate_dut_list(full_text))
        _LOGGER.info(f"DUT files generated successfully in {new_file_path_tc}")
    except Exception as err:
        _LOGGER.critical(f"Error in generating DUT files. {err}")

        start_index = full_text.find("BEGIN") + len("BEGIN")
        end_index = full_text.find("END_FUNCTION_BLOCK")
        code_section = full_text[start_index:end_index]
        code_section_done = code_section.replace(" #", " ")
        code_section_done = code_section_done.replace("\t#", "\t")
        code_section_done = code_section_done.replace("(#", "(")
        SCLConvertion.SCL_Code = code_section_done
        return code_section_done
    except Exception as err:
        raise ValueError("The code section could not be extracted from the SCL file.") from err


def find_project_name(full_text: str) -> str:
    """Find and store the project name from the SCL file."""
    linjer = full_text.split("\n")
    for i in range(len(linjer)):
        if "FUNCTION_BLOCK " in linjer[i]:
            start_index = linjer[i].find('"')
            stop_index = linjer[i].find('"', 16)
            SCLConvertion.project_name = linjer[i][start_index + 1 : stop_index]
    return SCLConvertion.project_name


def generate_dut_list(full_text: str) -> list[Tcdut]:
    """Generate the dut list from the SCL file."""
    stop_index = full_text.find("FUNCTION_BLOCK")
    dut_text: str = full_text[:stop_index].strip()
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
        lines[0] = lines[0].replace('"', "")

        for line in range(len(lines)):
            if "END_STRUCT" in lines[line]:
                lines[line] = lines[line].replace(";", "")

        dutcode = "\n".join(lines)
        SCLConvertion.dut_list.append(Tcdut(dut_name, dutcode))
    return SCLConvertion.dut_list


def generate_dut_files(folder_path: str, dut_list: list[Tcdut]) -> None:
    """Generate the dut files based on the provided file path."""
    for dut in dut_list:
        filsti = rf"{folder_path}/{dut.name}.TcDUT"
        with Path(filsti).open("w", encoding="utf-8-sig") as file:
            file.write(dut.header())
            file.write(dut.code)
            file.write(dut.footer)


def generate_tcpou_file(folder_path: str, project_name: str, header: str, variable_text: str, code: str) -> None:
    """Generate the TcPOU file based on the provided folder path."""
    filsti = rf"{folder_path}/{project_name}.TcPOU"
    with Path(filsti).open("w", encoding="UTF-8") as file:
        file.write(header)
        file.write(variable_text)
        file.write(code)
