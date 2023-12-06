import csv, os

from IAMsystemRomediAPI import *

import global_variables as gv


"""
Procedures that parse csv data in global variables dictionaries.
These dictionaries are used to instantiate ChemoOnto.
"""


### Dictionaries


################################## THEORETICAL

def DCI_table_to_dict(table_csv):
    """
    Creats or adds additional anti-cancer molecule informations to a a global dictionary (gv.dict_DCI) from a csv table containing CHIMIO data on anti-cancer molecule.
    The csv must contain a column "DCCLEUNIK" with the DCI key of the anti-cancer molecule.
    (in french "DCI" "Dénomination Commune Internationale", in english "INN" International Nonproprietary Names)
    In this repository, an example of csv table is available in data/ChemoOnto_data/theoretical_protocols_tables/CHIMIO_DCI.csv
    From this table, the content of the output dictionary is available in the json file : data/ChemoOnto_data/json_drugs_dict/dict_DCI.csv
    @param table_csv: csv table that contains CHIMIO anti-cancer molecules information
    @return: None
    """
    with open(table_csv, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter='|')
        for row in csvreader:
            if row["DCCLEUNIK"] != "-1":
                if row["DCCLEUNIK"] not in gv.dict_DCI:
                    gv.dict_DCI[row["DCCLEUNIK"]] = {}
                    for col_key in row:
                        gv.dict_DCI[row["DCCLEUNIK"]][col_key] = row[col_key]
                else:
                    print("this is possible")
    return None


def PDT_table_to_dict(table_csv, AC, AA, S):
    """
    Creats or adds additional anti-cancer molecule informations to a a global dictionaries (gv.dict_DCI, gv.dict_anti_ade ,gv.dict_solvant) from a csv table containing CHIMIO data on commercial drugs.
    The csv must contain a column "CODEPDT" the code of the commercial drug name.
    In this repository, an example of csv table is available in data/ChemoOnto_data/theoretical_protocols_tables/CHIMIO_PRODUIT.csv
    Depending on the options, informations about commercial drugs will be added to global anti-cancer drug dictionary, global anti adverse event dictionary or global solvant dictionary.
    From this table, the content of the output dictionary is available in the directory : data/ChemoOnto_data/json_drugs_dict/
    @param table_csv: csv table that contains CHIMIO drugs information
    @param AC: if TRUE, add information about anti-cancer drugs
    @param AA: if TRUE, add information about anti-adverse event drugs
    @param S: if TRUE, add information about solvant
    @return: None
    """
    with open(table_csv, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter='|')
        for row in csvreader:
            if row["DCCLEUNIK"] == "-1": # solvant or anti-ADE
                if "poche" in row["NOMPDT"].lower(): # solvant
                    if S :
                        if row["CODEPDT"] not in gv.dict_solvant:
                            gv.dict_solvant[row["CODEPDT"]] = {}
                            for col_key in row:
                                gv.dict_solvant[row["CODEPDT"]][col_key] = row[col_key]
                        else:
                            print("this is possible solvant")
                else: # anti-ADE
                    if AA :
                        if row["CODEPDT"] not in gv.dict_anti_ade:
                            gv.dict_anti_ade[row["CODEPDT"]] = {}
                            for col_key in row :
                                gv.dict_anti_ade[row["CODEPDT"]][col_key] = row[col_key]
                        else:
                            print("this is possible ADE")
            elif row["DCCLEUNIK"] != "": #DCI
                if AC :
                    str_dccleunik = str(row["DCCLEUNIK"])
                    if "CODEPDT" not in gv.dict_DCI[str_dccleunik]:
                        gv.dict_DCI[str_dccleunik]["CODEPDT"] = {}
                        if row["CODEPDT"] not in gv.dict_DCI[str_dccleunik]["CODEPDT"]:
                            gv.dict_DCI[str_dccleunik]["CODEPDT"][row["CODEPDT"]] = {}
                        for col_key in row :
                            gv.dict_DCI[str_dccleunik]["CODEPDT"][row["CODEPDT"]][col_key] = row[col_key]
                    elif row["CODEPDT"] not in gv.dict_DCI[str_dccleunik]["CODEPDT"]:
                        gv.dict_DCI[str_dccleunik]["CODEPDT"][row["CODEPDT"]] = {}
                        for col_key in row:
                            gv.dict_DCI[str_dccleunik]["CODEPDT"][row["CODEPDT"]][col_key] = row[col_key]
                    else:
                        print("this is possible DCI for ", str_dccleunik)
            #else :
                #print("row with no DCCLEUNIK", row)
    return None


#### Romedi


def addsRomediIndstoDCIdict():
    """
    Detect anti-cancer molecule names and adds Romedi ingredients to global anti-cancer dictionary (gv.dict_DCI)
    @return: None
    """
    #list_name_dci = [dict_DCI[dci_id]['NOMDCI'] for dci_id in dict_DCI.keys()]
    ## local installation
    url_detection = gv.cfg["romediapp"]["url_detection"]
    url_detection_by_type = gv.cfg["romediapp"]["url_detection_by_type"]
    iam_system = IAMsystemRomediAPI(url_detection, url_detection_by_type)
    if os.path.exists(gv.cfg["romediapp"]["no_found_dci"]):
        os.remove(gv.cfg["romediapp"]["no_found_dci"])
    for dci_key in gv.dict_DCI.keys():
        nom_dci = gv.dict_DCI[dci_key]['NOMDCI'].replace('EC', ' ')
        res = iam_system.detect_drug(nom_dci.encode(encoding='UTF-8'))
        if res != {}:
            gv.dict_DCI[dci_key]["ROMEDI_IND_NAME"] = res['0']["code"].split("/")[-1]
            gv.dict_DCI[dci_key]["ROMEDI_TYPE"] = res['0']['type']
        else:
            with open(gv.cfg["romediapp"]["no_found_dci"], "a") as f:
                f.write(gv.dict_DCI[dci_key]['NOMDCI'] + "\n")
    return None


def addsRomediIndstoPDTdict(dict_PDT):
    """
    Detect CHIMIO drugs commercial name and adds Romedi ingredients to global dictionaries (gv.dict_DCI, gv.anti_ade, gv.dict_solvant)
    @param dict_PDT:
    @return:
    """

    url_detection = gv.cfg["romediapp"]["url_detection"]
    url_detection_by_type = gv.cfg["romediapp"]["url_detection_by_type"]
    iam_system = IAMsystemRomediAPI(url_detection, url_detection_by_type)
    if os.path.exists(gv.cfg["romediapp"]["no_found_pdt"]):
        os.remove(gv.cfg["romediapp"]["no_found_pdt"])
    for pdt_key in dict_PDT.keys():
        res = iam_system.detect_drug(dict_PDT[pdt_key]['NOMPDT'].encode(encoding='UTF-8'))
        if res != {}:
            dict_PDT[pdt_key]["ROMEDI_IND_NAME"] = res['0']["code"].split("/")[-1]
            dict_PDT[pdt_key]["ROMEDI_TYPE"] = res['0']['type']
        else :
            with open(gv.cfg["romediapp"]["no_found_pdt"], "a") as f:
                f.write(dict_PDT[pdt_key]['NOMPDT'] + "\n")
    return None





### Protocols

def PRC_table_to_dict(table_csv, AC, AA, S):
    """
    Creats a global protocol dictionary from csv CHIMIO theoretical protocols csv table.
    The csv must contain a "PRCLEUNIK" column, the key of the protocols.
    The final dicionary will contains the entire description of the drug administrations (day, dose, unit) of each protocols.
    In this repository, an example of csv table is available in data/ChemoOnto_data/theoretical_protocols_tables/WDN_LIGNEPROTOCOLS.csv
    @param table_csv: CHIMIO table with protocols
    @param AC: if TRUE, information about anti-cancer drug administrations will be added to the global protocol dictionary (gv.dict_theoretical_PRC).
    @param AA: if TRUE, information about anti adverse event drug administrations will be added to the global protocol dictionary (gv.dict_theoretical_PRC).
    @param S: if TRUE, information about solvant administrations will be added to the global protocol dictionary (gv.dict_theoretical_PRC).
    @return: None
    """
    name_col_prt_list = ["TYPEPROT","NOMPROT","DUREECYCLE","DUREETRT","BIBLIOPROT","COMMENTPRO","SURVEILLAN","REMARQUES","NBCYCLEDEF","UTMAJPR","COUTPROT","MAXCYCLE"]
    with open(table_csv, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter='|')
        for row in csvreader:
            if row["PRCLEUNIK"] not in gv.dict_theoretical_PRC:
                gv.dict_theoretical_PRC[row["PRCLEUNIK"]] = {}
            for col_key in row:
                if col_key in name_col_prt_list:
                    gv.dict_theoretical_PRC[row["PRCLEUNIK"]][col_key] = row[col_key]
            if AC :
                if row["DCCLEUNIK"] in gv.dict_DCI:
                    if "ANTI_CANCER" not in gv.dict_theoretical_PRC[row["PRCLEUNIK"]]:
                        gv.dict_theoretical_PRC[row["PRCLEUNIK"]]["ANTI_CANCER"] = {}
                    # Première fois qu'on rencontre la molécule pour le PRC x
                    if row["DCCLEUNIK"] not in gv.dict_theoretical_PRC[row["PRCLEUNIK"]]["ANTI_CANCER"] :
                        gv.dict_theoretical_PRC[row["PRCLEUNIK"]]["ANTI_CANCER"][row["DCCLEUNIK"]] = {}
                        gv.dict_theoretical_PRC[row["PRCLEUNIK"]]["ANTI_CANCER"][row["DCCLEUNIK"]]["DCI"] = gv.dict_DCI[row["DCCLEUNIK"]]
                        gv.dict_theoretical_PRC[row["PRCLEUNIK"]]["ANTI_CANCER"][row["DCCLEUNIK"]]["DRUG_ADM"] = {}
                        dict_adm = {}
                        for col_key in row:
                            if col_key not in name_col_prt_list:
                               dict_adm[col_key] = row[col_key]
                        gv.dict_theoretical_PRC[row["PRCLEUNIK"]]["ANTI_CANCER"][row["DCCLEUNIK"]]["DRUG_ADM"] = [dict_adm]
                    # cas où le PRC x a deux fois la même mol : ex molécules 6 dans PRC 944 ou molécule 25 dans PRC 433
                    else:
                        dict_adm = {}
                        for col_key in row:
                            if col_key not in name_col_prt_list:
                                dict_adm[col_key] = row[col_key]
                        gv.dict_theoretical_PRC[row["PRCLEUNIK"]]["ANTI_CANCER"][row["DCCLEUNIK"]]["DRUG_ADM"].append(dict_adm)
            if S:
                if row["CODEPDT"] in gv.dict_solvant:
                    if "SOLVANT_CODEPDT" not in gv.dict_theoretical_PRC[row["PRCLEUNIK"]]:
                        gv.dict_theoretical_PRC[row["PRCLEUNIK"]]["SOLVANT_CODEPDT"] = {}
                    if row["CODEPDT"] not in gv.dict_theoretical_PRC[row["PRCLEUNIK"]]["SOLVANT_CODEPDT"] :
                        gv.dict_theoretical_PRC[row["PRCLEUNIK"]]["SOLVANT_CODEPDT"][row["CODEPDT"]] = {}
                        gv.dict_theoretical_PRC[row["PRCLEUNIK"]]["SOLVANT_CODEPDT"][row["CODEPDT"]]["PDT"] = gv.dict_solvant[row["CODEPDT"]]
                        gv.dict_theoretical_PRC[row["PRCLEUNIK"]]["SOLVANT_CODEPDT"][row["CODEPDT"]]["DRUG_ADM"] = {}
                        dict_adm = {}
                        for col_key in row:
                            if col_key not in name_col_prt_list:
                                dict_adm[col_key] = row[col_key]
                        gv.dict_theoretical_PRC[row["PRCLEUNIK"]]["SOLVANT_CODEPDT"][row["CODEPDT"]]["DRUG_ADM"] = [dict_adm]
                    else :
                        dict_adm = {}
                        for col_key in row:
                            if col_key not in name_col_prt_list:
                                dict_adm[col_key] = row[col_key]
                        gv.dict_theoretical_PRC[row["PRCLEUNIK"]]["SOLVANT_CODEPDT"][row["CODEPDT"]]["DRUG_ADM"].append(dict_adm)
            if AA:
                if row["CODEPDT"] in gv.dict_anti_ade:
                    if "ANTI_ADE_CODEPDT" not in gv.dict_theoretical_PRC[row["PRCLEUNIK"]]:
                        gv.dict_theoretical_PRC[row["PRCLEUNIK"]]["ANTI_ADE_CODEPDT"] = {}
                    if row["CODEPDT"] not in gv.dict_theoretical_PRC[row["PRCLEUNIK"]]["ANTI_ADE_CODEPDT"]:
                        gv.dict_theoretical_PRC[row["PRCLEUNIK"]]["ANTI_ADE_CODEPDT"][row["CODEPDT"]] = {}
                        gv.dict_theoretical_PRC[row["PRCLEUNIK"]]["ANTI_ADE_CODEPDT"][row["CODEPDT"]]["PDT"] = gv.dict_anti_ade[row["CODEPDT"]]
                        gv.dict_theoretical_PRC[row["PRCLEUNIK"]]["ANTI_ADE_CODEPDT"][row["CODEPDT"]]["DRUG_ADM"] = {}
                        dict_adm = {}
                        for col_key in row:
                            if col_key not in name_col_prt_list:
                                dict_adm[col_key] = row[col_key]
                        gv.dict_theoretical_PRC[row["PRCLEUNIK"]]["ANTI_ADE_CODEPDT"][row["CODEPDT"]]["DRUG_ADM"] = [dict_adm]
                    else:
                        dict_adm = {}
                        for col_key in row:
                            if col_key not in name_col_prt_list:
                                dict_adm[col_key] = row[col_key]
                        gv.dict_theoretical_PRC[row["PRCLEUNIK"]]["ANTI_ADE_CODEPDT"][row["CODEPDT"]]["DRUG_ADM"].append(dict_adm)
    return None



################################## FOLLOWED



def followed_PRC_to_dict(ranked_table_csv):
    """
    Creats a global actual lines dictionary, from CHIMIO clinical data (1 row by administration)
    In this repository, an example of csv table, with false patient data, is available in data/ChemoOnto_data/followed_lines/CHIMIO_data.
    @param ranked_table_csv: a table with CHIMIO clinical data, ordered by PRCKEY, start_date
    @return:None
    """
    gv.dict_followed_PRC = {}
    with open(ranked_table_csv, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';')
        PRC_KEY = -1
        CYCLE_NUM = -1
        for row in csvreader:
            if row["PATIENT_NUM"] not in gv.dict_followed_PRC:
                i = 1 # to identify changement of pat for None weigth 2022-12-12 
                gv.dict_followed_PRC[row["PATIENT_NUM"]] = {}
                PRC_KEY = row["PRCKEY"]
                CYCLE_NUM = row["CYCLE"]
                KEY_ADM = str(i) + "_" + row["ROW_NUM"]
                first_START_DATE_PRCKEY = row["START_DATE"] + "_" + PRC_KEY
                gv.dict_followed_PRC[row["PATIENT_NUM"]][first_START_DATE_PRCKEY] = {}
                gv.dict_followed_PRC[row["PATIENT_NUM"]][first_START_DATE_PRCKEY][PRC_KEY] = {}
                gv.dict_followed_PRC[row["PATIENT_NUM"]][first_START_DATE_PRCKEY][PRC_KEY][KEY_ADM] = {}
                for col_key in row:
                    gv.dict_followed_PRC[row["PATIENT_NUM"]][first_START_DATE_PRCKEY][PRC_KEY][KEY_ADM][col_key] = row[col_key]
            if row["PRCKEY"] != PRC_KEY or (row["PRCKEY"] == PRC_KEY and int(row["CYCLE"]) < int(CYCLE_NUM)):
                i += 1
                PRC_KEY = row["PRCKEY"]
                CYCLE_NUM = row["CYCLE"]
                ## 2022-12-01 :
                KEY_ADM = str(i) + "_" + row["ROW_NUM"]
                first_START_DATE_PRCKEY = row["START_DATE"] + "_" + PRC_KEY
                gv.dict_followed_PRC[row["PATIENT_NUM"]][first_START_DATE_PRCKEY] = {}
                gv.dict_followed_PRC[row["PATIENT_NUM"]][first_START_DATE_PRCKEY][PRC_KEY] = {}
                gv.dict_followed_PRC[row["PATIENT_NUM"]][first_START_DATE_PRCKEY][PRC_KEY][KEY_ADM] = {}
                for col_key in row:
                    gv.dict_followed_PRC[row["PATIENT_NUM"]][first_START_DATE_PRCKEY][PRC_KEY][KEY_ADM][col_key] = row[col_key]
            else:
                i += 1
                ## 2022-12-01 :
                KEY_ADM = str(i) + "_" + row["ROW_NUM"]
                CYCLE_NUM = row["CYCLE"]
                gv.dict_followed_PRC[row["PATIENT_NUM"]][first_START_DATE_PRCKEY][PRC_KEY][KEY_ADM] = {}
                for col_key in row:
                    gv.dict_followed_PRC[row["PATIENT_NUM"]][first_START_DATE_PRCKEY][PRC_KEY][KEY_ADM][col_key] = row[col_key]
    return None