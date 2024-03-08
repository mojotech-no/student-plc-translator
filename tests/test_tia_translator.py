"""Test cases for the TIA Translator."""

from unittest import TestCase

from plctranslator import generate_code, generate_variable_text


class TestTiaTranslator(TestCase):
    """Test case for the TIA Translator."""

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

    def test_generate_variable_text(self):
        """Test case for the generate_variable_text method."""
        """This test verifies that the generate_variable_text method correctly extracts the variable
         text from a given input.
        The full_text variable contains a sample input with variables defined using the VAR_INPUT section.
        The expected_output variable contains the expected result after extracting the variable text.
        The result variable stores the actual result obtained from the generate_variable_text method.
        The self.assertEqual method is used to compare the actual result with the expected output.
        """

        expected_output = "input1 : INT;\ninput2 : BOOL;"
        result = generate_variable_text(TestTiaTranslator.full_text)
        print(f"results is {result}")
        self.assertEqual(result, expected_output)

    def test_generate_code(self):
        """Test case for the generate_code method."""
        expected_output = """
\t#InvertedX := #X XOR #Param.PinvX;

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



"""
        result = generate_code(TestTiaTranslator.full_text)
        self.assertEqual(result, expected_output)
