"""Contains the classes for the PLC translator."""


class Tcdut:
    """Represents a DUT."""

    def __init__(self, name, code):
        """Initialize the DUT object with a name and code."""
        self.name = name
        self.code = code

    def header(self):
        """Generate the header for the DUT."""
        return f"""<?xml version="1.0" encoding="utf-8"?>
<TcPlcObject Version="1.1.0.1" ProductVersion="3.1.4024.12">
  <DUT Name= "{self.name}" Id="{{572155cd-1cb7-4296-b8e0-698682541d76}}">
    <Declaration><![CDATA["""

    footer = """
]]></Declaration>
  </DUT>
</TcPlcObject>"""


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
