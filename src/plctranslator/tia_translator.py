"""This module contains functions for converting SCL files."""

import io  # Importerer io for å kunne bruke StringIO
import logging  # Importerer logging for å kunne logge
import re  # Importerer re for å kunne bruke split
from logging import StreamHandler  # Importerer StreamHandler for å kunne bruke log_stream
from pathlib import Path

from .tc_helpers import Tcdut  # Importerer Tcdut fra tc_helpers
from .tia_helpers import SCLConvertion, read_scl_file  # Importerer SCLConvertion fra tia_helpers

log_stream = io.StringIO()  # Lager en log_stream for å kunne lagre logg til en variabel
stream_handler = StreamHandler(log_stream)  # Lager en stream_handler for å kunne skrive logg til en variabel
_LOGGER = logging.getLogger(__name__)  # Lager en logger for å kunne logge
_LOGGER.addHandler(stream_handler)  # Legger til stream_handler for å kunne skrive logg til en variabel
formatter = logging.Formatter("%(levelname)s - %(message)s")  # Lager en formatter for å kunne formatere logg
stream_handler.setFormatter(formatter)
logging_text = ""


def create_object(full_text: str) -> SCLConvertion:
    """Create an SCLConvertion object from the given full text."""
    scl_full_text = full_text
    _LOGGER.info("Generating Code...")
    try:
        scl_code = generate_code(full_text)
    except Exception as err:
        _LOGGER.critical(f"Error in generating code. {err}")
    _LOGGER.debug("Generating DUT List...")
    try:
        dut_list = generate_dut_list(full_text)
        _LOGGER.debug(f"Generating DUT List.. dut's found: {len(dut_list)}...")
    except Exception as err:
        _LOGGER.critical(f"Error in generating DUT list. {err}")
    _LOGGER.debug("Generating Variable Text...")
    try:
        scl_variable_text = convert_timers_and_counters_in_variabletext(generate_variable_text(full_text))
    except Exception as err:
        _LOGGER.critical(f"Error in generating variable text. {err}")
    _LOGGER.debug("Finding Project Name...")
    try:
        project_name = find_project_name(full_text)
    except Exception as err:
        _LOGGER.critical(f"Error in finding project name. {err}")

    converting_object = SCLConvertion(scl_full_text, scl_code, scl_variable_text, project_name)
    converting_object.dut_list = dut_list

    return converting_object


def generate_variable_text(full_text: str) -> str:
    """Generate the variable text from the SCL file."""
    start_index = full_text.find("VAR_INPUT")
    stop_index = full_text.find("BEGIN")
    converted_variable_text = full_text[start_index + len("VAR_INPUT") : stop_index].strip()
    return converted_variable_text


def find_full_info(converting_object: SCLConvertion) -> str:
    """Find the full information from the converting object."""
    potential_converted_tcpou: str = converting_object.header() + converting_object.variable_text() + converting_object.code()
    potential_converted_dut: str = ""
    for i in range(len(converting_object.dut_list)):
        potential_converted_dut += converting_object.dut_list[i].code
    return potential_converted_dut + potential_converted_tcpou


def check(full_text: str) -> bool:  # Check funksjonen tar inn en streng og returnerer en bool
    """Check the full text."""
    converting_object = create_object(full_text)  # Lager et converting_object med data fra full_text
    result = True
    potential_converted_full_info = find_full_info(converting_object)

    must_have_keywords = ["END_FUNCTION_BLOCK", "BEGIN"]
    error_list = ["TON_TIME", "TOF_TIME", "TP_TIME", "CTU_INT"]
    found_errors = [keyword for keyword in error_list if keyword in potential_converted_full_info]
    not_found_keywords = [keyword for keyword in must_have_keywords if keyword not in full_text]

    if found_errors:
        result = False
        for error in found_errors:
            _LOGGER.error(f"Check Complete: Error found - {error}")
        log_stream.truncate()  # Tømmer log_stream for å unngå at den blir fylt opp med gamle verdier
        log_stream.seek(0)  # Setter log_stream til starten for å unngå at den blir fylt opp med gamle verdier
    elif not_found_keywords:
        result = False
        for error in not_found_keywords:
            _LOGGER.error(f"Check Complete: Error, did not find - {error}")
        log_stream.truncate()  # Tømmer log_stream for å unngå at den blir fylt opp med gamle verdier
        log_stream.seek(0)

    else:
        _LOGGER.info("Check Complete: No Errors found")
        log_stream.truncate()  # Tømmer log_stream for å unngå at den blir fylt opp med gamle verdier
        log_stream.seek(0)

    converting_object.dut_list = []
    return result


def translate(filepath: str, new_file_path_tc: str) -> None:
    """Translate the SCL file and generate the TCPou and DUT files."""
    full_text = read_scl_file(filepath)
    code = generate_code(full_text)
    dut_list = generate_dut_list(full_text)
    variable_text = convert_timers_and_counters_in_variabletext(generate_variable_text(full_text))
    project_name = find_project_name(full_text)
    scl_full_text = full_text
    convertion_object = SCLConvertion(scl_full_text, code, variable_text, project_name)
    convertion_object.dut_list = dut_list
    log_stream.truncate()
    log_stream.seek(0)

    _LOGGER.debug("Generating TcPOU files...")
    try:
        generate_tcpou_file(new_file_path_tc, convertion_object)
        _LOGGER.info(f"POU file generated successfully in \n{new_file_path_tc}")
    except Exception as err:
        _LOGGER.critical(f"Error in generating TCPou file. {err}")

    _LOGGER.debug("Generating DUT files...")
    try:
        generate_dut_files(new_file_path_tc, convertion_object)
        _LOGGER.info(f"DUT files generated successfully in \n{new_file_path_tc}")
        convertion_object.dut_list = []
    except Exception as err:
        _LOGGER.critical(f"Error in generating DUT files. {err}")


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

    return variable_text


def generate_code(full_text: str) -> str:
    """Generate the code from the SCL file."""
    try:
        start_index = full_text.find("BEGIN") + len("BEGIN")
        end_index = full_text.find("END_FUNCTION_BLOCK")
        code_section = full_text[start_index:end_index]
        code_section_done = code_section.replace(" #", " ")
        code_section_done = code_section_done.replace("\t#", "\t")
        code_section_done = code_section_done.replace("(#", "(")
        return code_section_done
    except Exception as err:
        raise ValueError("The code section could not be extracted from the SCL file.") from err


def find_project_name(full_text: str) -> str:
    """Find and store the project name from the SCL file."""
    lines = full_text.split("\n")
    for i in range(len(lines)):
        if "FUNCTION_BLOCK " in lines[i]:
            start_index = lines[i].find('"')
            stop_index = lines[i].find('"', 16)
            project_name = lines[i][start_index + 1 : stop_index]
    return project_name


def generate_dut_list(full_text: str) -> list[Tcdut]:
    """Generate the dut list from the SCL file."""
    stop_index = full_text.find("FUNCTION_BLOCK")
    dut_text: str = full_text[:stop_index].strip()
    dut_lines = dut_text.split("\n")
    for i in range(len(dut_lines)):
        if "VERSION" in dut_lines[i]:
            dut_lines[i] = dut_lines[i].replace(dut_lines[i], "//" + dut_lines[i])
    dut_text = "\n".join(dut_lines)
    dut_list: list[str] = re.split(r"END_TYPE", dut_text)
    dut_list_done: list[Tcdut] = []

    for dut in dut_list[:-1]:
        dutcode = dut
        dutcode += "\nEND_TYPE"
        dutcode = dutcode.replace("\n\n", "")
        start_index = dutcode.find('"')
        stopp_index = dutcode.find('"', start_index + 1)
        dut_name = dutcode[6:stopp_index]
        dutcode = dutcode[: stopp_index + 1] + " :\n" + dutcode[stopp_index + 1 :]  # Legger til en linje etter navnet

        lines = dutcode.split("\n")
        lines[0] = lines[0].replace(";", "")
        lines[0] = lines[0].replace('"', "")

        for line in range(len(lines)):
            if "END_STRUCT" in lines[line]:
                lines[line] = lines[line].replace(";", "")

        dutcode = "\n".join(lines)
        dut_list_done.append(Tcdut(dut_name, dutcode))
    return dut_list_done


def generate_dut_files(folder_path: str, converting_object: SCLConvertion) -> None:
    """Generate the dut files based on the provided file path."""
    for dut in converting_object.dut_list:
        filsti = rf"{folder_path}/{dut.name}.TcDUT"
        with Path(filsti).open("w", encoding="utf-8-sig") as file:
            file.write(dut.header())
            file.write(dut.code)
            file.write(dut.footer)


def generate_tcpou_file(folder_path: str, converting_object: SCLConvertion) -> None:
    """Generate the TcPOU file based on the provided folder path."""
    filsti = rf"{folder_path}/{converting_object.project_name}.TcPOU"
    with Path(filsti).open("w", encoding="UTF-8") as file:
        file.write(converting_object.header())
        file.write(converting_object.variable_text())
        file.write(converting_object.code())
