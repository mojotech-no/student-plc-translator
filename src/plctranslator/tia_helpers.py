"""Contains the classes for the PLC translator."""

from pathlib import Path

from src.plctranslator.tc_helpers import Tcdut


class SCLConvertion:
    """Represents a conversion of SCL code."""

    SCL_Full_Text = ""
    SCL_Code = ""
    dut_list: list[Tcdut] = []
    ton_names: list[str] = []
    unconverted_ton_function: list[str] = []
    converted_ton_functions: list[str] = []
    variable_text1 = ""
    project_name = ""

    @staticmethod
    def header() -> str:
        """Generate the header for the SCL file."""
        return f"""<?xml version="1.0" encoding="utf-8"?>
<TcPlcObject Version="1.1.0.1" ProductVersion="3.1.4024.12">
<POU Name="{SCLConvertion.project_name}" Id="{{e0089193-a969-4f48-a38a-b0825baaeb17}}" SpecialFunc="None">
<Declaration><![CDATA[FUNCTION_BLOCK {SCLConvertion.project_name}
"""

    @staticmethod
    def variable_text() -> str:
        """Generate the variable text for the SCL file."""
        return "VAR_INPUT\n" + SCLConvertion.variable_text1

    @staticmethod
    def code() -> str:
        """Generate the code for the SCL file."""
        return f"""]]></Declaration>
    <Implementation>
      <ST><![CDATA[
 {SCLConvertion.SCL_Code}]]></ST>
    </Implementation>
  </POU>
</TcPlcObject>"""


def read_scl_file(scl_file_path: str) -> None:
    """Read the SCL file from the given file path and store the content in SCLConvertion.SCL_Full_Text."""
    try:
        with Path(scl_file_path).open(encoding="utf-8-sig") as fil:
            temp = fil.read()
            return temp
            SCLConvertion.SCL_Full_Text = fil.read()
    except Exception as e:
        return ""
        print(e.message)
