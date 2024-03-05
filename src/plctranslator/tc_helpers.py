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