class TcDUT:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        

    def Header(self):
        return f"""<?xml version="1.0" encoding="utf-8"?>
<TcPlcObject Version="1.1.0.1" ProductVersion="3.1.4024.12">
  <DUT Name= "{self.name}" Id="{{572155cd-1cb7-4296-b8e0-698682541d76}}">
    <Declaration><![CDATA["""

    Footer = """
]]></Declaration>
  </DUT>
</TcPlcObject>"""


class SCL_Convertion:
      SCL_Full_Text = ""
      SCL_Code = ""
      DUT_List = []
      variable_text = ""
      def Header():
           return f"""<?xml version="1.0" encoding="utf-8"?>
<TcPlcObject Version="1.1.0.1" ProductVersion="3.1.4024.12">
<POU Name="{SCL_Convertion.project_Name}" Id="{{e0089193-a969-4f48-a38a-b0825baaeb17}}" SpecialFunc="None">
<Declaration><![CDATA[FUNCTION_BLOCK {SCL_Convertion.project_Name}
            """
      
      def Variable_Text():
           return "VAR_INPUT\n" + SCL_Convertion.variable_text
      
      def Code():
        return f"""]]></Declaration>
    <Implementation>
      <ST><![CDATA[
 {SCL_Convertion.SCL_Code}]]></ST>
    </Implementation>
  </POU>
</TcPlcObject>""" 