import sys, time, os.path

import global_variables as gv
import med_dicts as md
import chemonto_struct as cs
import chemonto_theo_PRC_inst as cti
from options_utils import boolOption, setConfigFileTheo, save_drug_dict

from utils import replace_dieze


def usage(): print(
    """
    
    instantiatesChemoOnto.py :
        Creats and instantiates a ChemoOnto graph with chemotherapy theoretical protocols. 
        Creats 2 owl files in graph_outputs/ directory :
            -Suffixed '_ChemoOnto' file contains ChemoOnto ontological structure (Classes, object and data properties)
            -Prefixed 'theo_' file contains ChemoOnto graph instantiated with chemotherapy theoretical protocols csv tables in data/ChemoOnto_data/theoretical_protocols_tables/ directory.
        
        If you want to change input and output directory options, please modify the config file.
    
    usage:    
        python3 instantiatesChemOntoWithTheoreticalPRC.py -AC <on|off> -AA <on|off> -S <on|off> -R <on|off>
        
    
    Parameters :
        --anticancer / -AC : Followed by "on", ChemoOnto will be instantiated with information about anti-cancer drug administrations.
        Default: off 
        
        --antiade / -AA : Followed by "on", ChemoOnto will be instantiated with information about anti-adverse event drug administrations.
        Default: off
        
        --Solvant / -S : Followed by "on", ChemoOnto will be instantiated with information about solvant drug administrations.
        Default: off
        
        --romedi / -R : Followed by "on", every drugs will be linked to Romedi Ingredients. 
        If there are existing json files in data/ChemoOnto_data/json_drug_dicts/ directory, these files will be used to creats Romedi links.
        If not, drugs will be detected with RomediApp. In this case, make sure RomediApp is installed (https://github.com/scossin/RomediApp) and that romedi options are correctly sett in the config file.
        Default: off
    
        
    """
    )

def main(argv=None):
    if "-h" in argv or "--help" in argv:
        usage()
        sys.exit()

    try:
        AC = argv[argv.index("--anticancer") + 1]
    except ValueError:
        try:
            AC = argv[argv.index("-AC") + 1]
        except ValueError:
            AC = None

    try:
        AA = argv[argv.index("--antiade") + 1]
    except ValueError:
        try:
            AA = argv[argv.index("-AA") + 1]
        except ValueError:
            AA = None

    try:
        S = argv[argv.index("--Solvant") + 1]
    except ValueError:
        try:
            S = argv[argv.index("-S") + 1]
        except ValueError:
            S = None

    try:
        S = argv[argv.index("--Solvant") + 1]
    except ValueError:
        try:
            S = argv[argv.index("-S") + 1]
        except ValueError:
            S = None

    try:
        romedi = argv[argv.index("--romedi") + 1]
    except ValueError:
        try:
            romedi = argv[argv.index("-R") + 1]
        except ValueError:
            romedi = None


    AC = boolOption(AC)
    AA = boolOption(AA)
    S = boolOption(S)
    romedi = boolOption(romedi)

    # Config File
    gv.initConfigFile(romedi=romedi, pcf=None)
    
    ## 2022-12-13
    # Load empty ChemOntoTox 
    gv.initChemOntoToxWithPath(path_empty_chemontotox = gv.cfg["onto"]["local"]["empty_chemontotox"])

    already_exists_AC = os.path.exists(gv.cfg["drug_dicts_path"] + gv.cfg["dict_DCI"])
    already_exists_AA = os.path.exists(gv.cfg["drug_dicts_path"] + gv.cfg["dict_anti_ade"])
    already_exists_S = os.path.exists(gv.cfg["drug_dicts_path"] + gv.cfg["dict_solvant"])

    title_message = " ChemoOnto "
    centered_title_message = title_message.center(100, "*")

    print("\n\n\t"+ centered_title_message +"\n\n")
    print(" You are instantiating a ChemoOnto graph with theoretical chemotherapy protocols in " + gv.cfg["tables_data"]["theoretical_PRC_dir"] + " dir. \n")

    if AC:
        print("\t Adding information about anti cancer drug administrations. \n")
        if already_exists_AC:
            print("\t Anti-cancer drugs have already been detected with RomediApp. Results are in " + gv.cfg["drug_dicts_path"] + gv.cfg["dict_DCI"])
            print("\t If you want Romedi links, please check if there are in the existing dict (keywords 'ROMEDI_IND_NAME', or 'ROMEDI_TYPE').\n"
                  "\t If there are not, you should delete the existing json file, and restart the the program, with activated romedi option.")
            gv.initDictDCIFromJson(gv.cfg["drug_dicts_path"] + gv.cfg["dict_DCI"])
        else:
            print("\t Detecting anti-cancer drugs with RomediApp. Saving results in " + gv.cfg["drug_dicts_path"] + gv.cfg["dict_DCI"])
            gv.initDictDCI()
            md.DCI_table_to_dict(table_csv=gv.cfg["tables_data"]["DCI"])

    if AA:
        print("\t Adding information about anti adverse event drug administrations. \n")
        if already_exists_AA:
            print("\t Anti adverse event drugs have already been detected with RomediApp. Results are in " + gv.cfg["drug_dicts_path"] +
                  gv.cfg["dict_anti_ade"])
            print(
                "\t If you want Romedi links, please check if there are in the existing dict (keywords 'ROMEDI_IND_NAME', or 'ROMEDI_TYPE').\n"
                "\t If there are not, you should delete the existing json file, and restart the the program, with romedi option.")
            gv.initDictAntiADEFromJson(gv.cfg["drug_dicts_path"] + gv.cfg["dict_anti_ade"])
        else :
            print("\t Detecting anti adverse event  drugs with RomediApp. Saving results in " + gv.cfg["drug_dicts_path"] + gv.cfg[
                "dict_anti_ade"])
            gv.initDictAntiADE()

    if S:
        print("\t Adding information about solvant administrations. \n")
        if already_exists_S:
            print("\t Solvants have already been detected with RomediApp. Results are in " + gv.cfg["dict_solvant"] +
                  gv.cfg["dict_solvant"])
            print(
                "\t If you want Romedi links, please check if there are in the existing dict (keywords 'ROMEDI_IND_NAME', or 'ROMEDI_TYPE').\n"
                "\t If there are not, you should delete the existing json file, and restart the the program, with romedi option.")
            gv.initDictSolvantFromJson(gv.cfg["drug_dicts_path"] + gv.cfg["dict_solvant"])
        else :
            print("\t Detecting anti-cancer drugs with RomediApp. Saving results in " + gv.cfg["drug_dicts_path"] + gv.cfg[
                "dict_solvant"])
            gv.initDictSolvant()

    if (AC and not already_exists_AC) or (AA and not already_exists_AA) or (S and not already_exists_S) :
        md.PDT_table_to_dict(table_csv=gv.cfg["tables_data"]["PRODUIT"], AC=AC, AA=AA, S=S)


    # Fill medications dictionaries depending on options

    prefix = ""

    if AC:
        if not already_exists_AC:
            if romedi:
                print("\n\n\t\t Adding Romedi links to anti cancer drugs. \n")
                md.addsRomediIndstoDCIdict()
            print("\t\t Saving anti cancer dict in a json file. (" + gv.cfg["drug_dicts_path"] + gv.cfg["dict_DCI"] + ")")
            save_drug_dict(gv.cfg["drug_dicts_path"], gv.cfg["dict_DCI"], gv.dict_DCI)
        prefix = prefix + "AC_"

    if AA:
        if not already_exists_AA:
            if romedi:
                print("\n\n\t\t Adding Romedi links to anti adverse event drugs. \n")
                md.addsRomediIndstoPDTdict(gv.dict_anti_ade)
            print("\t\t Saving anti adverse event dict in a json file.(" + gv.cfg["drug_dicts_path"] + gv.cfg["dict_anti_ade"] + ")")
            save_drug_dict(gv.cfg["drug_dicts_path"], gv.cfg["dict_anti_ade"], gv.dict_anti_ade)
        prefix = prefix + "AA_"

    if S:
        if not already_exists_S:
            if romedi:
                print("\n\n\t\t Adding Romedi links to anti solvants. \n")
                md.addsRomediIndstoPDTdict(gv.dict_solvant)
            print("\t\t Saving solvant dict in a json file.(" + gv.cfg["drug_dicts_path"] + gv.cfg["dict_solvant"] + ")")
            save_drug_dict(gv.cfg["drug_dicts_path"], gv.cfg["dict_solvant"], gv.dict_solvant)
        prefix = prefix + "S_"

    # Fill theroretical PRC dictionnary depending on options
    gv.initDictTheoreticalPRC()
    md.PRC_table_to_dict(gv.cfg["tables_data"]["PROTOCOLS"], AC = AC, AA = AA, S = S)


    # Define ChemOnto Structure
    print("\n\n\n Defining ChemoOnto Structure. \n")
    timestr = time.strftime("%Y%m%d%H%M%S")
    #name_space = "http://ChemOnto_" + timestr + ".owl#"
    #name_space = "http://ChemOnto.owl#"
    name_space = gv.cfg["namespaces"]["chemonto"]
    gv.initChemOntoWithNamespace(name_space)
    path_owl = gv.cfg["outputs"]
    empty_name_owl = timestr + "_ChemoOnto.owl"
    cs.creatsChemOntoStruct(path_owl=path_owl, name_owl=empty_name_owl)
    # import de la time ontology pour les règles SWRL :
    #cs.importTO()
    if romedi:
        cs.addsChemOntoToRomediProperties(path_owl=path_owl, name_owl=empty_name_owl)
    gv.chemonto.save(path_owl + empty_name_owl)

    # clean namespaces 2023-09
    replace_dieze(path_owl + empty_name_owl)

    print("\t An empty graph is saved in " + path_owl + empty_name_owl + "\n")

    # Instantiates ChemOnto with theroretical protocols
    print(" Instantiating ChemoOnto with theroretical protocols. \n")
    cti.instantiatesTheoreticalPRC(AC = AC, AA = AA, S = S, romedi = romedi)
    name_owl = "theo_" + prefix + empty_name_owl
    gv.chemonto.save(path_owl + name_owl)

    # clean namespaces 2023-09
    replace_dieze(path_owl + name_owl)

    print("\t ChemoOnto instantiated with theroretical protocols is saved in " + path_owl + name_owl + "\n")

    # set DB_config file with output
    setConfigFileTheo(name_owl, empty_name_owl)
    




if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

