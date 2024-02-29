import re
import sys

from plctranslator.klasser_skisse import SCL_Convertion, TcDUT


def Read_SCL_Fil(SCL_File_Path):
    try:
        with open(SCL_File_Path, encoding="utf-8-sig") as fil:
            SCL_Convertion.SCL_Full_Text = fil.read()

    except FileNotFoundError:
        print(f"Filen {SCL_File_Path} ble ikke funnet.")
        sys.exit(1)

    except Exception as e:
        print(f"En uventet feil oppstod: {e}")


def Generate_Variable_Text():
    Start_Index = SCL_Convertion.SCL_Full_Text.find("VAR_INPUT")
    Stop_Index = SCL_Convertion.SCL_Full_Text.find("BEGIN")

    SCL_Convertion.variable_text = SCL_Convertion.SCL_Full_Text[Start_Index + len("VAR_INPUT") : Stop_Index].strip()


def Generate_Code():
    Start_Index = SCL_Convertion.SCL_Full_Text.find("BEGIN")
    Stop_Index = SCL_Convertion.SCL_Full_Text.find("END_FUNCTION_BLOCK")

    SCL_Convertion.SCL_Code = SCL_Convertion.SCL_Full_Text[Start_Index + len("VAR_INPUT") : Stop_Index].strip()
    SCL_Convertion.SCL_Code = SCL_Convertion.SCL_Code.replace("#", "")


def Find_Project_Name():
    linjer = SCL_Convertion.SCL_Full_Text.split("\n")
    for i in range(len(linjer)):  #
        if "FUNCTION_BLOCK " in linjer[i]:
            Start_Index = linjer[i].find('"')
            Stop_Index = linjer[i].find('"', 16)
            SCL_Convertion.project_Name = linjer[i][Start_Index + 1 : Stop_Index]


def Generate_DUT_List():
    Stopp_Index = SCL_Convertion.SCL_Full_Text.find("FUNCTION_BLOCK")
    DUT_Text = SCL_Convertion.SCL_Full_Text[:Stopp_Index].strip()
    DUT_List = re.split(r"END_TYPE", DUT_Text)

    for DUT in DUT_List[:-1]:
        DUT += "\nEND_TYPE"
        DUT = DUT.replace("VERSION : 0.1", "")
        DUT = DUT.replace("\n\n", "")
        Stopp_Index = DUT.find('"', 6)
        dut_name = DUT[6:Stopp_Index]
        DUT = DUT[: Stopp_Index + 1] + " :\n" + DUT[Stopp_Index + 1 :]  # Legger til en linje etter navnet

        lines = DUT.split("\n")
        lines[0] = lines[0].replace(";", "")

        for i in range(len(lines)):
            if "END_STRUCT" in lines[i]:
                lines[i] = lines[i].replace(";", "")

        DUT = "\n".join(lines)
        SCL_Convertion.DUT_List.append(TcDUT(dut_name, DUT))


def Generate_DUT_Files(File_Path):
    for DUT in SCL_Convertion.DUT_List:
        filsti = rf"{File_Path}\{DUT.name}.TcDUT"
        with open(filsti, "w", encoding="utf-8-sig") as file:
            file.write(DUT.Header())
            file.write(DUT.code)
            file.write(DUT.Footer)


def Generate_TcPOU_File(folder_path):
    filsti = rf"{folder_path}\{SCL_Convertion.project_Name}.TcPOU"
    with open(filsti, "w", encoding="UTF-8") as file:
        file.write(SCL_Convertion.Header())
        file.write(SCL_Convertion.Variable_Text())
        file.write(SCL_Convertion.Code())


def main():
    scl_file_path = r"C:\Users\47974\Desktop\Tia SCL FILER\MOJO_MB_V2.scl"
    scl_file_path = r"C:\Users\47974\Desktop\Tia SCL FILER\MOJO_MB_V2.scl"
    New_File_Path_TcPOU = r"C:\Users\47974\Documents\TcXaeShell\TwinCAT Project1\TwinCAT Project1\Untitled2\POUs"
    New_File_Path_TcDUT = r"C:\Users\47974\Documents\TcXaeShell\TwinCAT Project1\TwinCAT Project1\Untitled2\DUTs"

    Read_SCL_Fil(scl_file_path)
    Generate_Variable_Text()
    Generate_Code()
    Find_Project_Name()
    Generate_DUT_List()
    Generate_TcPOU_File(New_File_Path_TcPOU)
    Generate_DUT_Files(New_File_Path_TcDUT)


if __name__ == "__main__":
    main()
