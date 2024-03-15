"""Test cases for the TIA Translator."""

from pathlib import Path
from unittest import TestCase

from src.plctranslator.tc_helpers import Tcdut
from src.plctranslator.tia_translator import (
    convert_timers_and_counters_in_variabletext,
    find_project_name,
    generate_code,
    generate_dut_files,
    generate_dut_list,
    generate_tcpou_file,
    generate_variable_text,
    check,
)


class TestTiaTranslator(TestCase):
    """Test case for the TIA Translator."""

    dut_list: list[Tcdut] = []
    dut_list.append(Tcdut("Param_MB_V1", "HEIHEI"))
    dut_list.append(Tcdut("OsSta_MB_V1", "HEIHEIHEHIE"))
    full_text = """TYPE "Param_MB_V1"
VERSION : 0.1
   STRUCT
      Ptag : String[16] := 'TagName';   // Tag name.Tag name for di...
      PinvX : Bool := FALSE;   // Invert input. If the parameter is ...
      PlatchY : Bool := FALSE;   // Latched output.If the parameter ...
      PalarmDelay : Time := T#0MS;   // Time delay alarm.Delay before ...
      Ppriority : Int := 99;   // Alarm priority.Integer describing ...
   END_STRUCT;

END_TYPE

TYPE "OsSta_MB_V1"
VERSION : 0.1
   STRUCT
      BX : Bool;
      Y : Bool;
      Alarm : Bool;
      Warning : Bool;
      Fault : Bool;
      Latched : Bool;
      Blocked : Bool;
      Suppressed : Bool;
      ForcedBlocked : Bool;
      ForcedSuppressed : Bool;
   END_STRUCT;

END_TYPE

FUNCTION_BLOCK "FB_my_fb"
{ S7_Optimized_Access := 'TRUE' }
VERSION : 0.1
   VAR_INPUT
      X : Bool;
      Safetysensor : Bool;
      MyInput : Bool;
      MyReset : Bool;
      MyPV : Int;
   END_VAR

   VAR_OUTPUT
      Y : Bool;
      Alarm : Bool;
      EmergencyStop : Bool;
      Qatt : Bool;
      MyCounter : Int;
   END_VAR

   VAR
      TimerTON {InstructionName := 'TON_TIME'; LibVersion := '1.0'; S7_SetPoint := 'False'} : TON_TIME;
      TimerTOF {InstructionName := 'TOF_TIME'; LibVersion := '1.0'} : TOF_TIME;
      TimerTP {InstructionName := 'TP_TIME'; LibVersion := '1.0'} : TP_TIME;
      InvertedX { S7_SetPoint := 'True'} : Bool;
      AlarmTimer {InstructionName := 'TON_TIME'; LibVersion := '1.0'; S7_SetPoint := 'False'} : TON_TIME;
      Param : "Param_MB_V1";
      OsSta : "OsSta_MB_V1";
      CTU {InstructionName := 'CTU_INT'; LibVersion := '1.0'} : CTU_INT;
   END_VAR


BEGIN
	#InvertedX := #X XOR #Param.PinvX;

	// Eksempel på bruk av TON
	IF #InvertedX THEN
    #TimerTON(IN := #InvertedX,
	PT := T#5S); // Juster PT-verdien etter behov
	#Y := #TimerTON.Q;
	ELSE
	#TimerTOF(IN := NOT #InvertedX,
	PT := T#5S); // Juster PT-verdien etter behov
	#Y := #TimerTOF.Q;
	END_IF;


	// Eksempel på bruk av TP
	#TimerTP(IN := #InvertedX,
	PT := T#2S); // Pulstid
	IF #TimerTP.Q THEN
    IF NOT #Safetysensor THEN
	#EmergencyStop := TRUE; // Utfør nødstopp hvis sikkerhetssensoren er deaktivert
	END_IF;
	END_IF;

	// Håndtering av alarmforsinkelse
	#AlarmTimer(IN := #InvertedX AND NOT #AlarmTimer.Q,
	PT := #Param.PalarmDelay);
	IF #AlarmTimer.Q THEN
	#Alarm := TRUE;

	END_IF;

	// Eksempel på å låse Y-utgangen
	IF #Param.PlatchY THEN
	#Y := #Y OR (#Y AND NOT #InvertedX); // Låser Y til sann til X går til falsk
	END_IF;



END_FUNCTION_BLOCK"""

    variable_text = """X : Bool;
      Safetysensor : Bool;
      MyInput : Bool;
      MyReset : Bool;
      MyPV : Int;
   END_VAR

   VAR_OUTPUT
      Y : Bool;
      Alarm : Bool;
      EmergencyStop : Bool;
      Qatt : Bool;
      MyCounter : Int;
   END_VAR

   VAR
      TimerTON {InstructionName := 'TON_TIME'; LibVersion := '1.0'; S7_SetPoint := 'False'} : TON_TIME;
      TimerTOF {InstructionName := 'TOF_TIME'; LibVersion := '1.0'} : TOF_TIME;
      TimerTP {InstructionName := 'TP_TIME'; LibVersion := '1.0'} : TP_TIME;
      InvertedX { S7_SetPoint := 'True'} : Bool;
      AlarmTimer {InstructionName := 'TON_TIME'; LibVersion := '1.0'; S7_SetPoint := 'False'} : TON_TIME;
      Param : "Param_MB_V1";
      OsSta : "OsSta_MB_V1";
      CTU {InstructionName := 'CTU_INT'; LibVersion := '1.0'} : CTU_INT;
   END_VAR"""

    def test_generate_variable_text(self):
        """Test case for the generate_variable_text method."""
        """This test verifies that the generate_variable_text method correctly extracts the variable
         text from a given input.
        The full_text variable contains a sample input with variables defined using the VAR_INPUT section.
        The expected_output variable contains the expected result after extracting the variable text.
        The result variable stores the actual result obtained from the generate_variable_text method.
        The self.assertEqual method is used to compare the actual result with the expected output.
        """
        expected_output = """X : Bool;
      Safetysensor : Bool;
      MyInput : Bool;
      MyReset : Bool;
      MyPV : Int;
   END_VAR

   VAR_OUTPUT
      Y : Bool;
      Alarm : Bool;
      EmergencyStop : Bool;
      Qatt : Bool;
      MyCounter : Int;
   END_VAR

   VAR
      TimerTON {InstructionName := 'TON_TIME'; LibVersion := '1.0'; S7_SetPoint := 'False'} : TON_TIME;
      TimerTOF {InstructionName := 'TOF_TIME'; LibVersion := '1.0'} : TOF_TIME;
      TimerTP {InstructionName := 'TP_TIME'; LibVersion := '1.0'} : TP_TIME;
      InvertedX { S7_SetPoint := 'True'} : Bool;
      AlarmTimer {InstructionName := 'TON_TIME'; LibVersion := '1.0'; S7_SetPoint := 'False'} : TON_TIME;
      Param : "Param_MB_V1";
      OsSta : "OsSta_MB_V1";
      CTU {InstructionName := 'CTU_INT'; LibVersion := '1.0'} : CTU_INT;
   END_VAR"""
        result = generate_variable_text(TestTiaTranslator.full_text)
        self.assertEqual(result, expected_output)

    def test_generate_code(self):
        """Test case for the generate_code method."""
        expected_output = """
\tInvertedX := X XOR Param.PinvX;

	// Eksempel på bruk av TON
	IF InvertedX THEN
    TimerTON(IN := InvertedX,
\tPT := T#5S); // Juster PT-verdien etter behov
\tY := TimerTON.Q;
	ELSE
\tTimerTOF(IN := NOT InvertedX,
\tPT := T#5S); // Juster PT-verdien etter behov
\tY := TimerTOF.Q;
	END_IF;


	// Eksempel på bruk av TP
	TimerTP(IN := InvertedX,
\tPT := T#2S); // Pulstid
	IF TimerTP.Q THEN
    IF NOT Safetysensor THEN
\tEmergencyStop := TRUE; // Utfør nødstopp hvis sikkerhetssensoren er deaktivert
\tEND_IF;
	END_IF;

	// Håndtering av alarmforsinkelse
	AlarmTimer(IN := InvertedX AND NOT AlarmTimer.Q,
\tPT := Param.PalarmDelay);
	IF AlarmTimer.Q THEN
\tAlarm := TRUE;

	END_IF;

	// Eksempel på å låse Y-utgangen
	IF Param.PlatchY THEN
\tY := Y OR (Y AND NOT InvertedX); // Låser Y til sann til X går til falsk
	END_IF;



"""

        result = generate_code(TestTiaTranslator.full_text)
        self.assertEqual(result, expected_output)

    def test_convert_timers_and_counters_in_variabletext(self):
        """Test case for the convert_timers_and_counters_in_variabletext method."""
        expected_output = """X : Bool;
      Safetysensor : Bool;
      MyInput : Bool;
      MyReset : Bool;
      MyPV : Int;
   END_VAR

   VAR_OUTPUT
      Y : Bool;
      Alarm : Bool;
      EmergencyStop : Bool;
      Qatt : Bool;
      MyCounter : Int;
   END_VAR

   VAR
\tTimerTON: TON;
\tTimerTOF: TOF;
\tTimerTP: TP;
      InvertedX { S7_SetPoint := 'True'} : Bool;
\tAlarmTimer: TON;
      Param : "Param_MB_V1";
      OsSta : "OsSta_MB_V1";
\tCTU: CTU;
   END_VAR"""
        result = convert_timers_and_counters_in_variabletext(TestTiaTranslator.variable_text)
        self.assertEqual(result, expected_output)

    def test_find_project_name(self):
        """Test case for the find_project_name method."""
        expected_output = "FB_my_fb"
        result = find_project_name(TestTiaTranslator.full_text)
        self.assertEqual(result, expected_output)

    def test_generate_dut_list(self):
        """Test case for the find_project_name method."""
        dut_list = generate_dut_list(TestTiaTranslator.full_text)
        expected_output = ["Param_MB_V1", "OsSta_MB_V1"]
        for i in range(len(dut_list)):
            result = dut_list[i].name
            self.assertIn(result, expected_output[i])

    def test_generate_dut_files(self):
        """Test case for the generate_dut_files method."""
        folderpath = Path("./tests/data/testConvertion")  # Konverter strengen til et Path-objekt
        generate_dut_files(folderpath, TestTiaTranslator.dut_list)
        for dut in TestTiaTranslator.dut_list:
            file_path = folderpath / f"{dut.name}.TcDUT"  # Bruk Path-objekt for å bygge filstien
            self.assertTrue(file_path.exists())  # Sjekk at filen eksisterer

    def test_generate_tcpou_file(self):
        """Test case for the generate_tcpou_file method."""
        folderpath = Path("./tests/data/testConvertion")
        project_name = "FB_my_fb"
        header = f"""<?xml version="1.0" encoding="utf-8"?>
   <TcPlcObject Version="1.1.0.1" ProductVersion="3.1.4024.12">
   <POU Name="{project_name}" Id="{{e0089193-a969-4f48-a38a-b0825baaeb17}}" SpecialFunc="None">
   <Declaration><![CDATA[FUNCTION_BLOCK {project_name}
   """
        variable_text = "VAR_INPUT\n" + TestTiaTranslator.variable_text.replace('"', "")
        code = generate_code(TestTiaTranslator.full_text)
        code_wrapped = f"""]]></Declaration>
   <Implementation>
   <ST><![CDATA[
   {code}]]></ST>
   </Implementation>
   </POU>
   </TcPlcObject>"""

        generate_tcpou_file(folderpath, project_name, header, variable_text, code_wrapped)

        # Rettet bruk av Path for å sjekke eksistens og slette fil
        file_path = folderpath / f"{project_name}.TcPOU"
        print(file_path)
        self.assertTrue(file_path.exists())

      
    def test_check(self):
      """Test case for the check method."""
      result = check(TestTiaTranslator.full_text)
      self.assertEqual(len(TestTiaTranslator.dut_list), 2)
      self.assertTrue(result)
