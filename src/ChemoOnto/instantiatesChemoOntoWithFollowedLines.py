import time
import pandas as pd
import zlib as zlib

from options_utils import boolOption, setConfigFileFollowed


# with warnings.catch_warnings():
#     warnings.filterwarnings("ignore",
#                             message="optimized Cython parser module 'owlready2_optimized' is not available, defaulting to slower Python implementation")
#     warnings.filterwarnings("ignore",
#                             message="DataProperty http://www.w3.org/2006/time#xsdDateTime belongs to more than one entity types: [owl.DeprecatedProperty, owl.DatatypeProperty]; I'm trying to fix it...")


import global_variables as gv
import med_dicts as md
#import chemonto_struct as cs
import chemonto_foll_PRC_inst as cfi
from utils import *


def usage(): print(
    """
    instantiatesChemoOntoWithFollowedLines.py :
        Instantiates a ChemoOnto graph with patient actual chemotherapy lines. 
        Creats 1 owl file in graph_outputs/ directory, prefixed with "followed_".
        The file contains a ChemoOnto graph instantiated with csv patient data in data/ChemoOnto_data/followed_lines/ directory.
        Recorded CHIMIO data of the patient must be in a csv file named with the patient number in CHIMIO_data/ subdirectory.
        
        If you want to change input and output directory options, please modify the config file.
        
          
    usage:    
        python3 instantiatesChemOntoWithFollowedLines.py -PLF <path/to/patients/data/file> -AC <on|off> -AA <on|off> -S <on|off> -R <on|off>
    
        
    Parameters :
        
        --patientsListFile / -PLF: path to a file containing a list of patients with their informations
        Default: ../../data/ChemoOnto_data/followed_lines/2023-09-07_5_patients_list.csv
        
        --anticancer / -AC: Followed by "on", ChemoOnto will be instantiated with information about anti-cancer drug administrations.
        Default: off 
        
        --antiade / -AA: Followed by "on", ChemoOnto will be instantiated with information about anti-adverse event drug administrations.
        Default: off
        
        --Solvant / -S: Followed by "on", ChemoOnto will be instantiated with information about solvant drug administrations.
        Default: off
        
        --romedi / -R: Followed by "on", every drugs will be linked to Romedi Ingredients. 
        
        
    """
    )

def main(argv=None):
    if "-h" in argv or "--help" in argv:
        usage()
        sys.exit()

    try:
        plf = argv[argv.index("--patientsListFile") + 1]
    except ValueError:
        try:
            plf = argv[argv.index("-PLF") + 1]
        except ValueError:
            plf = "../../data/ChemoOnto_data/followed_lines/2023-09-07_5_patients_list.csv"
            
    # try:
    #     pidf = argv[argv.index("--patientsIndividualDataFile") + 1]
    # except ValueError:
    #     try:
    #         pidf = argv[argv.index("-PIDF") + 1]
    #     except ValueError:
    #         pidf = 1

    try:
        pcf = argv[argv.index("--prefixConfFiles") + 1]
    except ValueError:
        try:
            pcf = argv[argv.index("-PCF") + 1]
        except ValueError:
            pcf = None
            
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
    gv.initConfigFile(romedi=romedi, pcf=pcf)

    patients_list_file = pd.read_csv(plf, sep=";")
    patients_list = patients_list_file['PATIENT_NUM'].tolist()
    
    # patients individual data
    dict_pat_data={}
    with open(plf, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        
        for row in reader:
            #print("row.keys() : ", row.keys())
            if str(row["PATIENT_NUM"]) not in dict_pat_data :
                dict_pat_data[str(row["PATIENT_NUM"])]={}
            dict_pat_data[str(row["PATIENT_NUM"])]["BIRTH_DATE"]=row["BIRTH_DATE"]
            dict_pat_data[str(row["PATIENT_NUM"])]["DEATH_DATE"]=row["DEATH_DATE"]
            dict_pat_data[str(row["PATIENT_NUM"])]["SEX"]=row["SEX_CD"]

    # patients chimio data
    
    # if os.path.exists(gv.cfg["log_files"]["no_chimio_data"]):
    #     no_chimiodata_patients_list_file = pd.read_csv(gv.cfg["log_files"]["no_chimio_data"])
    #     no_chimiodata_patients_list = no_chimiodata_patients_list_file['PATIENT_NUM'].tolist()
    # else :
    #     no_chimiodata_patients_list = []

    #print("len(no_chimiodata_patients_list)", len(no_chimiodata_patients_list))

    print("ChempOnto will be instantiated with :")
    prefix = ""
    if AC:
        print("-anti cancer")
        gv.initDictDCIFromJson(gv.cfg["drug_dicts_path"] + gv.cfg["dict_DCI"])
        prefix = prefix + "AC"
    if AA:
        print("-anti adverse event")
        gv.initDictAntiADEFromJson(gv.cfg["drug_dicts_path"] + gv.cfg["dict_anti_ade"])
        prefix = prefix + "AA"
    if S:
        print("-solvant")
        gv.initDictSolvantFromJson(gv.cfg["drug_dicts_path"] + gv.cfg["dict_solvant"])
        prefix = prefix + "S"
    print("drug administrations.\n\n")

    # Load empty ChemoOnto
    path_owl = gv.cfg["outputs"]
    name_empty_owl = gv.cfg["empty"]
    gv.initChemOntoWithPath(path_owl, name_empty_owl)

    # Load ChemOnto filled with theoretical PRC
    path_owl = gv.cfg["outputs"]
    name_theo_owl = gv.cfg["theoretical"]
    gv.initTheoChemOntoWithPath(path_owl, name_theo_owl)
    
    
    ## 2022-12-13
    # Load empty ChemOntoTox 
    gv.initChemOntoToxWithPath(path_empty_chemontotox = gv.cfg["onto"]["local"]["empty_chemontotox"])
    
    
    # Instantiates ChemOnto with empty an empty graph as starting point
    print(path_owl + name_empty_owl + " file will be used as starting ChemoOnto graph.\n")
    print("Instantiating ChemoOnto with followed lines \n")
    
    chemontotox_file = gv.cfg["onto"]["local"]["empty_chemontotox"]
    print("chemontotox_file", chemontotox_file)


    for patnum in patients_list :

        patnum = str(patnum)

        # Check process
        # path_to_info_process_yaml = gv.cfg["log_files"]["info_process_dict"]
        # print("path_to_info_process_yaml : ", path_to_info_process_yaml)
        # patnum_in_info_process_dict, parserError0, scannerError0 = checkPatNumInInfoProcessDict(path_to_info_process_yaml = path_to_info_process_yaml,
        #                              patnum = patnum,
        #                              AC = AC,
        #                              AA = AA,
        #                              S = S)
        #
        # if parserError0:
        #     addsPatNumToErrorFiles(path_to_log_file=gv.cfg['log_files']['yaml_errors'],
        #                            patnum=patnum,
        #                            function_name="checkPatNumInInfoProcessDict",
        #                            yaml_error_type="parserError")
        #
        # if scannerError0:
        #     addsPatNumToErrorFiles(path_to_log_file=gv.cfg['log_files']['yaml_errors'],
        #                            patnum=patnum,
        #                            function_name="checkPatNumInInfoProcessDict",
        #                            yaml_error_type="scannerError")

        # if patnum_in_info_process_dict or int(patnum) in no_chimiodata_patients_list:
        #
        #     if patnum_in_info_process_dict :
        #         print("A chemonto graph with these drug options has already been generated for patient ", patnum)
        #     else :
        #         print("No chimio data for patient ", patnum, "see ", gv.cfg["log_files"]["no_chimio_data"], " file." )
        #
        # else :
            
        pat_BD=dict_pat_data[patnum]["BIRTH_DATE"]
        pat_DD=dict_pat_data[patnum]["DEATH_DATE"]
        pat_SEX=dict_pat_data[patnum]["SEX"]
        patnum_an = str(zlib.crc32(patnum.encode('utf-8'))) #anonymize
        #gv.chemontotox_pat_ind = gv.patientInChemOntoToxGraph(patnum_an, chemontotox_file, pat_BD, pat_DD, pat_SEX)
        ## 2022-12-13
        chemontotox_pat_ind = cfi.patientInChemOntoToxGraph(patnum_an, pat_BD, pat_DD, pat_SEX,chemontotox_file)


        title_message = " ChemoOnto "
        centered_title_message = title_message.center(100, "*")

        chimiodata_pat = gv.cfg["tables_data"]["followed_lines_dir"] + gv.cfg["tables_data"]["chimiodata_dir"] + patnum + ".csv"

        print("\n\n\t" + centered_title_message + "\n\n")
        print("You are instantiating a ChemoOnto graph with followed chemotherapy lines in " + chimiodata_pat + " file. \n")



        # # Load pat_data
        # gv.initDictPatToChimioData(patnum=patnum,
        #                            path_to_CHIMIOData_dict=gv.cfg["query_results"]["dict_pat_to_chimio_data_path"])

        gv.initDictFollowedPRC()

        #md.followed_PRC_to_dict(gv.dict_patchimiodata)
        md.followed_PRC_to_dict(chimiodata_pat)


        cfi.instantiatesFollowedPRC(AC = AC,
                                    AA = AA,
                                    S = S,
                                    pat_num = patnum,
                                    patnum_an = patnum_an,
                                    chemontotox_pat_ind = chemontotox_pat_ind)
                                    #chemontotox_file = chemontotox_file)
                                    #chemontotox_file = gv.cfg["onto"]["local"]["chemontotox"])


        # cProfile.run("cfi.instantiatesFollowedPRC(AC = AC, AA = AA, S = S, pat_num = patnum,patnum_an = patnum_an,chemontotox_pat_ind = chemontotox_pat_ind)")
        # cProfile.run('cfi.instantiatesFollowedPRC(AC, AA, S, pat_num, patnum_an, chemontotox_pat_ind)')

        # Fill process_info_dict
        # parserError, scannerError = addPatNumToInfoProcessDict(pat_num = patnum,
        #                              AC = AC,
        #                              AA = AA,
        #                              S = S,
        #                              path_to_info_process_yaml=path_to_info_process_yaml)
        #
        # if parserError:
        #     addsPatNumToErrorFiles(path_to_log_file=gv.cfg['log_files']['yaml_errors'],
        #                              patnum=patnum,
        #                              function_name="addPatNumToInfoProcessDict",
        #                              yaml_error_type="parserError")
        #
        # if scannerError:
        #     addsPatNumToErrorFiles(path_to_log_file=gv.cfg['log_files']['yaml_errors'],
        #                              patnum=patnum,
        #                              function_name="addPatNumToInfoProcessDict",
        #                              yaml_error_type="scannerError")

    timestr = time.strftime("%Y%m%d%H%M%S")
    #name_owl = pcf + "_" + timestr + "_" + "ChemOnto.owl"

    name_owl = timestr + "_" + "ChemoOnto.owl"
    name_owl = "followed_" + prefix + "_" + name_owl
    gv.chemonto.save(path_owl + name_owl)
    # clean namespaces 2023-09
    replace_dieze(path_owl + name_owl)

    print("\n A ChemoOnto graph with followed lines is saved in " + path_owl + name_owl + ".\n\n" )

    ## 2022-12-13
    name_chemoontotox = timestr + "_" + "ChemoOntoTox.owl"
    gv.chemontotox.save(path_owl + name_chemoontotox)
    # clean namespaces 2023-09
    replace_dieze(path_owl + name_chemoontotox)

    print("\n Patients are in " + path_owl + name_chemoontotox + ".\n\n")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))