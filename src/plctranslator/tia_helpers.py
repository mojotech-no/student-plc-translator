"""Contains the classes for the PLC translator."""

import logging
import sys
from pathlib import Path

from .tc_helpers import Tcdut

_LOGGER = logging.getLogger(__name__)


class SCLConvertion:
    """Represents a conversion of SCL code."""

    SCL_full_Text = ""
    scl_code = ""
    scl_variable_text = ""
    project_name = ""
    dut_list: list[Tcdut] = []

    def __init__(self, scl_full_text, scl_code="", scl_variable_text="", project_name=""):
        """Initialize the SCLConvertion object."""
        self.SCL_full_Text = scl_full_text
        self.scl_code = scl_code
        self.scl_variable_text = scl_variable_text
        self.project_name = project_name
        self.dut_list = []

    potential_converted_full_info = ""

    def header(self) -> str:
        """Generate the header for the SCL file."""
        return f"""<?xml version="1.0" encoding="utf-8"?>
<TcPlcObject Version="1.1.0.1" ProductVersion="3.1.4024.12">
<POU Name="{self.project_name}" Id="{{e0089193-a969-4f48-a38a-b0825baaeb17}}" SpecialFunc="None">
<Declaration><![CDATA[FUNCTION_BLOCK {self.project_name}
"""
    
    

    def variable_text(self) -> str:
        """Generate the variable text for the SCL file."""
        return "VAR_INPUT\n" + self.scl_variable_text.replace('"', "")




    def code(self) -> str:
        """Generate the code for the SCL file."""
        return f"""]]></Declaration>
    <Implementation>
      <ST><![CDATA[
 {self.scl_code }]]></ST>
    </Implementation>
  </POU>
</TcPlcObject>"""


def read_scl_file(scl_file_path: str) -> str:
    """Read the SCL file from the given file path and store the content in SCLConvertion.SCL_Full_Text."""
    _LOGGER.debug(f"Reading SCL file from {scl_file_path}")
    try:
        with Path(scl_file_path).open(encoding="utf-8-sig") as fil:
            return fil.read()
    except FileNotFoundError:
        _LOGGER.critical(f"Filen {scl_file_path} ble ikke funnet.")
        sys.exit(1)
    except Exception as e:
        _LOGGER.critical(f"En uventet feil oppstod: {e}")
        return ""



