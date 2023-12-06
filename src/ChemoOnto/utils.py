import csv, sys, yaml
from datetime import date, datetime, timedelta
from os.path import exists
import shutil


#import global_variables as gv


### other functions


def read_config_file(yml_file="config.yml"):
    with open(yml_file, "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    return cfg

def removes_spe_char(name_class):
    list_of_special_char = ["/", ":", ";", "-", "'", "<", ">", "&", "%", ",", ".", "²", " ", "(", ")", "+", "=", "µ"]
    for el in list_of_special_char:
        if el in name_class:
            if el == "²":
                name_class = name_class.replace(el, "2")
            if el == "&" or el == "+":
                name_class = name_class.replace(el, "and")
            if el == "/":
                name_class = name_class.replace(el, "per")
            if el == "%":
                name_class = name_class.replace(el, "percent")
            if el == "=":
                name_class = name_class.replace(el, "equal")
            if el == "µ":
                name_class = name_class.replace(el, "micro")
            else:
                name_class = name_class.replace(el, "_")
    return name_class

def returns_jouradm(letter, world):
    return [pos+1 for pos, char in enumerate(world) if char == letter]


def returns_day_date_before_date(date_str, cycle_start_date,patnum, adm_key ,path_d2_before_d1):
    day_before = date.fromisoformat(date_str) - timedelta(days=1)
    date_cycle_start=date.fromisoformat(cycle_start_date)
    # day_before should be > to cycle_start_date
    if day_before < date.fromisoformat(cycle_start_date) and abs((day_before - date_cycle_start).days) == 1: # cycles of 1 day
        return date_cycle_start.isoformat()
    elif day_before < date.fromisoformat(cycle_start_date) and abs((day_before - date_cycle_start).days) > 1:
        d2_before_d1(path_to_log_file =path_d2_before_d1,
                     d1 = date_cycle_start, 
                     d2 = day_before,
                     adm_key = adm_key,
                     patnum = patnum)
    return day_before.isoformat()


def returnsUnit(number_unit):
    dict_number_to_unit = {1: "mg/kg",
                           2: "mg/m²",
                           3: "mg",
                           7: "mg",
                           8: "mg",
                           13: "mg",
                           4: "UI/kg",
                           5: "UI/kg",
                           15: "µg/kg",
                           16: "MUI/ml",
                           6: "UI/ml",
                           19: "MUI",
                           14: "MUI/ml",
                           30: "MUI/ml",
                           }
    if int(number_unit) in dict_number_to_unit:
        return dict_number_to_unit[int(number_unit)]
    else:
        return "-1"


def toUnitClasses(unit_str):
    dict_unit_to_uo_class = {
        "mg/kg" : "UO_0000308",
        "mg/m²": "UO_0000309"
        }
    return dict_unit_to_uo_class[unit_str]


def returnBodySurf(SCPATPRE, SCPATBOYD):
    # print("SCPATPRE",SCPATPRE)
    # print("type(SCPATPRE)", type(SCPATPRE))
    if SCPATPRE != "None":
        return parsesstrtofloat(SCPATPRE)
    else :
        return parsesstrtofloat(SCPATBOYD)


def parsesstrtofloat(str_data):
    if str_data == "" or str_data == 'None':
        return -1
    else :
        return float(str_data.replace(",", "."))

def parsesadminduration(data_dureeadm):
    dureeadm = data_dureeadm.split(":")[0]
    dureeadmin = data_dureeadm.split(":")[1]
    return dureeadm, dureeadmin

def isBolusFollowed(dureeadm, dureeadmin, voie):

    if (int(dureeadm) == 0 and int(dureeadmin) <= 30) or voie == "Voie Sous Cutanée":
        return True
    else:
        return False


def isBolusTheoretical(duree_adm_drug_adm, duree_adm_min_drug_adm, code_voie_drug_adm):
    if (int(duree_adm_drug_adm) == 0 and int(duree_adm_min_drug_adm) <= 30) or code_voie_drug_adm == "SC":
        return True
    else:
        return False


    
def calculatesNormDose_weight(dose_prescr, pat_weight):
    if pat_weight != -1 :
        return dose_prescr/pat_weight
    else :
        return -1
    
def calculatesNormDose_carbo(dose_prescr, pat_weight, pat_BD, pat_creat, pat_sex, date_str):
    if pat_weight != -1 and pat_creat != -1 :
        pat_age = calc_age_of_pat(pat_BD, date_str)
        predicted_CL_carbo = compute_chatelut(dose_prescr, pat_weight ,pat_age, pat_creat, pat_sex)
        AUC=dose_prescr/predicted_CL_carbo
        dose_norm = AUC
        return dose_norm
    else :
        return -1
    
def calculatesNormDose_bodysurf(dose_prescr, bodysurf):
    if bodysurf != -1:
        return dose_prescr/bodysurf
    else:
        return -1
    


        # {1: "mg/kg",
        #  2: "mg/m²",
        #  3: "mg",
        #  7: "mg" CARBO -> CHATELUT,
        #  8: "mg" CARBO -> CHATELUT,
        #  13: "mg",
        #  4: "UI/kg",
        #  5: "UI/kg",
        #  15: "µg/kg",
        #  16: "MUI/ml",
        #  6: "UI/ml"}




            

def findClosestMissingValue(dict_followed_PRC_of_pat_num, 
                          first_START_DATE_PRCKEY,
                          PRC_KEY,
                          current_adm_key, 
                          missing_value):
    
    #print("\n\n\n !!!!! IN findClosestWeightOrBS !!!!!!!!! \n\n\n")
    
    #print("dict_followed_PRC_of_pat_num[first_START_DATE_PRCKEY][PRC_KEY].keys()",dict_followed_PRC_of_pat_num[first_START_DATE_PRCKEY][PRC_KEY].keys())
    
    MV = dict_followed_PRC_of_pat_num[first_START_DATE_PRCKEY][PRC_KEY][current_adm_key][missing_value]
    
    #print("\n\n MV (must be 'None') :", MV)
    
    list_int_adm_desc_order = [int(adm_key_i.split("_")[-2]) for adm_key_i in dict_followed_PRC_of_pat_num[first_START_DATE_PRCKEY][PRC_KEY].keys()]
    list_int_adm_desc_order.sort(reverse = True)
    
    dict_int_adm_order_to_str_key = {}
    
    #dict_int_adm_order_to_str_key : int number of administration of pat to adm_id (adm_id = "numadm_rownum")
    for adm_key_i in dict_followed_PRC_of_pat_num[first_START_DATE_PRCKEY][PRC_KEY].keys():
        dict_int_adm_order_to_str_key[int(adm_key_i.split("_")[-2])] = adm_key_i
    
    # from the current administration to the first administration :
    int_adm_current_adm_key = int(current_adm_key.split("_")[-2])
    past_list_int_adm_desc_order = list_int_adm_desc_order[list_int_adm_desc_order.index(int_adm_current_adm_key):-1]
    ind_list = 0
    # Backward loop :
    while ind_list <= len(past_list_int_adm_desc_order)-1 and MV == 'None' : # equivalent
    #while past_list_int_adm_desc_order[ind_list] >= past_list_int_adm_desc_order[-1] and MV == 'None' :
        adm_key_i = dict_int_adm_order_to_str_key[past_list_int_adm_desc_order[ind_list]]
        MV = dict_followed_PRC_of_pat_num[first_START_DATE_PRCKEY][PRC_KEY][adm_key_i][missing_value]
        ind_list += 1
        #print("1- while past_list_int_adm_desc_order[ind_list] >= past_list_int_adm_desc_order[-1] and MV == 'None'  :")
        #print("1- adm_key_i : ", adm_key_i)
    if MV != 'None':
        #print("\n\n 1- return  parsesstrtofloat(MV) :", parsesstrtofloat(MV))
        return parsesstrtofloat(MV), "LATEST"
    else :
        
        MV = dict_followed_PRC_of_pat_num[first_START_DATE_PRCKEY][PRC_KEY][current_adm_key][missing_value]
        
        list_int_adm_asc_order = [int(adm_key_i.split("_")[-2]) for adm_key_i in dict_followed_PRC_of_pat_num[first_START_DATE_PRCKEY][PRC_KEY].keys()]
        list_int_adm_asc_order.sort()
        
        # from the current administration to the last administration :
        foward_list_int_adm_asc_order = list_int_adm_asc_order[list_int_adm_asc_order.index(int_adm_current_adm_key):-1]
        ind_list = 0
        # Foward loop :
        while ind_list <= len(foward_list_int_adm_asc_order)-1 and MV == 'None' : # equivalent
        #while foward_list_int_adm_asc_order[ind_list] <= foward_list_int_adm_asc_order[-1] and MV == 'None' :
            adm_key_i = dict_int_adm_order_to_str_key[foward_list_int_adm_asc_order[ind_list]]
            MV = dict_followed_PRC_of_pat_num[first_START_DATE_PRCKEY][PRC_KEY][adm_key_i][missing_value]
            ind_list += 1
            #print("2- while foward_list_int_adm_asc_order[ind_list] <= foward_list_int_adm_asc_order[-1] and MV == 'None' :")
            #print("2- adm_key_i : ", adm_key_i)
        if MV != 'None':
            #print("\n\n 2- return parsesstrtofloat(MV) :", parsesstrtofloat(MV))
            return parsesstrtofloat(MV),"NEXT"
        else :
            #print("\n\n 2- return  -1")
            return -1, 'NEVER'        
        
        
def compute_chatelut(dose_prescr, pat_weight , pat_age, pat_creat, pat_sex):
    if pat_sex == "DEM|SEX:M" :
        sex = 0
    elif pat_sex == "DEM|SEX:F":
        sex = 1
    else :
        return -1
    return 0.134*pat_weight + (218*pat_weight*(1-0.00457*pat_age)*(1-0.314*sex)/pat_creat)


def calc_age_of_pat(pat_BD, date_str):
    st= datetime.strptime(date_str, "%Y-%m-%d") 
    db=datetime.strptime(pat_BD, "%Y-%m-%d")
    return st.year-db.year-((st.month, st.day) < (db.month, db.day))
        
def cleanOwlFile(filename):
    """
    remove NamedIndividual type from owl file
    """

    with open(filename, 'r') as fp:
        # read an store all lines into list
        lines = fp.readlines()

    with open(filename, 'w') as fp:
        for line in lines :
            if '<rdf:type rdf:resource="http://www.w3.org/2002/07/owl#NamedIndividual"/>' not in line:
                fp.write(line)

    return None


def updateConfigFileWithQueryResFilename(key_filename, filename, yml_file):
    """
    key_filename :
        - cohort
    """
    with open(yml_file) as f:
        doc = yaml.safe_load(f)

    doc['query_results'][key_filename] = filename

    with open(yml_file, 'w') as f:
        yaml.safe_dump(doc, f, default_flow_style=False)
    cfg = read_config_file(yml_file)
    return cfg


def parseHasLinePRCKEY(PRCKEY):
    # print("PRCKEY", PRCKEY)
    # print("type(PRCKEY)", type(PRCKEY))
    if PRCKEY != "None":
        return int(PRCKEY)
    else:
        return -1


def addPatNumToYamlFile(yml_key, yml_value, yml_file):
    """
    Check if patnum is in path_to_chimiodata_dict
    If it is, instantitatesChemOntoFollowedLines isnt lanched
    If it is not, path_to_chimiodata_dict is modified and instantitatesChemOntoFollowedLines is launched
    + exceptions:
    sometimes, the file path_to_chimiodata_dict is read in the same time it is edited (because of manual parallelisation)
    {'2006325693': '../data/query_results/CHIMIOPatData/2006325693.csv}
    yml_file = pat_to_chimiodata_path_file
    yml_value = path_tochimiodata
    yml_key =patnum
    """
    patnum_in_yaml = False
    parserError = False
    scannerError = False
    try :
        with open(yml_file, 'r') as yamlfile:
            dict_yaml = yaml.safe_load(yamlfile) or {}
    except yaml.reader.ReaderError:
        print("\n\n\n STOOOOOOOOOP \n\n\n")
        sys.exit()
    except yaml.parser.ParserError:
        parserError = True
    except yaml.scanner.ScannerError:
        scannerError = True
    else:
        if yml_key not in dict_yaml:
            dict_yaml[yml_key] = yml_value
        else :
            patnum_in_yaml = True
        if not patnum_in_yaml:
            with open(yml_file, 'w') as yamlfile:
                yaml.safe_dump(dict_yaml, yamlfile)
    return patnum_in_yaml, parserError, scannerError

    # patnum_in_yaml = u.addPatNumToYamlFile(yml_key = pat_num,
    #                   yml_value = path_to_results_file,
    #                   yml_file = pat_to_chimio_path_dict)


def addPatNumToInfoProcessDict(pat_num, AC, AA, S, path_to_info_process_yaml):
    """
    {'2006325693': 'AC':'true' , 'AA':'false', 'S':'false' }
    """
    parserError = False
    scannerError = False
    try:
        with open(path_to_info_process_yaml, 'r') as yamlfile:
            dict_yaml = yaml.safe_load(yamlfile) or {}
    except yaml.reader.ReaderError:
        print("\n\n\n ReaderError : STOP  PROCESSING \n\n\n")
        sys.exit()
    except yaml.parser.ParserError:
        parserError = True
    except yaml.scanner.ScannerError:
        scannerError = True
    else:
        if pat_num not in dict_yaml:
            dict_yaml[pat_num] = {}
            dict_yaml[pat_num]["AC"] = AC
            dict_yaml[pat_num]["AA"] = AA
            dict_yaml[pat_num]["S"] = S
        else:
            modifyDrugOptionsInfoProcessDict(dict_info_process_patnum=dict_yaml[pat_num],
                                             option_str="AC",
                                             option_bool_value = AC)
            modifyDrugOptionsInfoProcessDict(dict_info_process_patnum=dict_yaml[pat_num],
                                             option_str="AA",
                                             option_bool_value=AA)
            modifyDrugOptionsInfoProcessDict(dict_info_process_patnum=dict_yaml[pat_num],
                                             option_str="S",
                                             option_bool_value=S)
        with open(path_to_info_process_yaml, 'w') as yamlfile:
            yaml.safe_dump(dict_yaml, yamlfile)

    return parserError, scannerError


def modifyDrugOptionsInfoProcessDict(dict_info_process_patnum, option_str, option_bool_value):
    """
    modify yaml file only if a drug options has become True
    """
    if not dict_info_process_patnum[option_str] and option_bool_value:
        dict_info_process_patnum[option_str] = True
    return None


def check_info_process_dict_options(dict_info_process_patnum, AC, AA, S):
    if AC != dict_info_process_patnum["AC"] or AA != dict_info_process_patnum["AA"] or dict_info_process_patnum["S"] != S:
        return False
    else :
        return True


def checkPatNumInInfoProcessDict(path_to_info_process_yaml, patnum, AC, AA, S):
    parserError = False
    scannerError = False
    patnumInYaml = False
    try:
        with open(path_to_info_process_yaml, 'r') as yamlfile:
            dict_yaml = yaml.safe_load(yamlfile) or {}
    except yaml.reader.ReaderError:
        print("\n\n\n ReaderError : STOP  PROCESSING \n\n\n")
        sys.exit()
    except yaml.parser.ParserError:
        parserError = True
    except yaml.scanner.ScannerError:
        scannerError = True
    else:
        with open(path_to_info_process_yaml, 'r') as yamlfile:
            dict_yaml = yaml.safe_load(yamlfile) or {}
        if (patnum not in dict_yaml) or (not check_info_process_dict_options(dict_yaml[patnum], AC, AA, S)):
            patnumInYaml = False
        else:
            patnumInYaml = True
    return patnumInYaml, parserError, scannerError


def addsPatNumToErrorFiles(path_to_log_file, patnum, function_name, yaml_error_type):
    file_exists = exists(path_to_log_file)
    if not file_exists:
        with open(path_to_log_file, 'w', newline="") as csvfile:
            fieldnames = ['PATNUM', 'function_name', 'yaml_error_type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'PATNUM': patnum,
                             'function_name': function_name,
                             'yaml_error_type': yaml_error_type})
    else :
        with open(path_to_log_file, 'a', newline="") as csvfile:
            fieldnames = ['PATNUM', 'function_name', 'yaml_error_type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'PATNUM': patnum,
                             'function_name': function_name,
                             'yaml_error_type': yaml_error_type})
    return None


def modifyConfigFileWithPrefix(first_keyfield, prefix, path_to_config):
    with open(path_to_config) as f:
        dict_yaml = yaml.safe_load(f)
    for key_path in dict_yaml[first_keyfield]:
        path = dict_yaml[first_keyfield][key_path]
        new_path = path.replace(first_keyfield, first_keyfield + "/" + prefix)
        dict_yaml[first_keyfield][key_path] = new_path
    with open(path_to_config, 'w') as f:
        yaml.safe_dump(dict_yaml, f, default_flow_style=False)
    return None

def modifyConfigFileWithSuffix(first_keyfield, second_keyfield, third_keyfield, suffix, path_to_config):
    with open(path_to_config) as f:
        dict_yaml = yaml.safe_load(f)
    path = dict_yaml[first_keyfield][second_keyfield][third_keyfield]
    new_path = path.replace(".owl", "_" + suffix + ".owl")
    dict_yaml[first_keyfield][second_keyfield][third_keyfield] = new_path
    ## 2022-12-13
    if third_keyfield != "chemontotox":
        shutil.copyfile(path,new_path)
    with open(path_to_config, 'w') as f:
        yaml.safe_dump(dict_yaml, f, default_flow_style=False)
    return None


def addPatNumToAttributeErrorFile(path_to_log_file, patnum, prop, chemonto_drug_ind, chemonto_drug_adm_ind_label):
    file_exists = exists(path_to_log_file)
    if not file_exists:
        with open(path_to_log_file, 'w', newline="") as csvfile:
            fieldnames = ['PATNUM', 'prop' , 'chemonto_drug_ind', 'chemonto_drug_adm_ind_label']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'PATNUM': patnum,
                             'prop': prop,
                             'chemonto_drug_ind': chemonto_drug_ind,
                             'chemonto_drug_adm_ind_label': chemonto_drug_adm_ind_label})
    else :
        with open(path_to_log_file, 'a', newline="") as csvfile:
            fieldnames = ['PATNUM', 'prop', 'chemonto_drug_ind', 'chemonto_drug_adm_ind_label']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'PATNUM': patnum,
                             'prop': prop,
                             'chemonto_drug_ind': chemonto_drug_ind,
                             'chemonto_drug_adm_ind_label': chemonto_drug_adm_ind_label})
    return None


def addsPatNumToNoChimioData(path_to_log_file, patnum):
    file_exists = exists(path_to_log_file)
    if not file_exists:
        with open(path_to_log_file, 'w', newline="") as csvfile:
            fieldnames = ['PATIENT_NUM']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'PATIENT_NUM': patnum})
    else :
        with open(path_to_log_file, 'a', newline="") as csvfile:
            fieldnames = ['PATIENT_NUM']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'PATIENT_NUM': patnum})
    return None



def patientInChemOntoToxGraph(patnum, pat_BD, pat_DD, pat_SEX):
    #patnum = str(zlib.crc32(patnum.encode('utf-8'))) #anonymize
    #print("in patientInChemOntoToxGraph, chemontotox_file : ", chemontotox_file)
    with chemontotox :
        if patnum not in [c.name for c in chemontotox.Patient.instances()]:
            chemontotox_pat_ind = chemontotox.Patient(patnum,
                                                     hasBirthDate = pat_BD,
                                                     hasDeathDate = pat_DD,
                                                     hasGender = pat_SEX)
        else :
            chemontotox_pat_ind = getattr(chemontotox, patnum)
    return chemontotox_pat_ind



def d2_before_d1(path_to_log_file, d1, d2, adm_key , patnum):
    
    file_exists = exists(path_to_log_file)
    if not file_exists:
        with open(path_to_log_file, 'w', newline="") as csvfile:
            fieldnames = ['PATNUM', 'adm_key', 'd1', 'd2']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'PATNUM': patnum,
                             'adm_key': adm_key,
                             'd1': d1,
                             'd2': d2})
    else :
        with open(path_to_log_file, 'a', newline="") as csvfile:
            fieldnames = ['PATNUM', 'adm_key' ,'d1', 'd2']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'PATNUM': patnum,
                             'adm_key': adm_key,
                             'd1': d1,
                             'd2': d2})
    return None


def one_data_is_always_None(path_to_log_file, patnum, missing_values_list, adm_key):
    
    #print("one_data_is_always_None , adm_key : ", adm_key)
    
    file_exists = exists(path_to_log_file)
    if not file_exists:
        with open(path_to_log_file, 'w', newline="") as csvfile:
            fieldnames = ['PATNUM','adm_key','always missing values for these data']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'PATNUM': patnum,
                             'adm_key': adm_key,
                             'always missing values for these data': missing_values_list})
    else :
        with open(path_to_log_file, 'a', newline="") as csvfile:
            fieldnames = ['PATNUM', 'adm_key','always missing values for these data']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'PATNUM': patnum,
                             'adm_key': adm_key,
                             'always missing values for these data': missing_values_list})

    return None


def replace_dieze(owl_file):
    with open(owl_file, 'r') as file:
        filedata = file.read()

    filedata = filedata.replace('http://chemontotox.owl#', 'http://chemontotox.owl/#')
    filedata = filedata.replace('http://chemonto.owl#INT_CYCLE', 'http://chemonto.owl/#INT_CYCLE')
    filedata = filedata.replace('http://ontotox.owl#DAY', 'http://ontotox.owl/#DAY')

    with open(owl_file, 'w') as file:
        file.write(filedata)
    return None





# def findClosestWeightOrBS(dict_followed_PRC_of_pat_num, 
#                           first_START_DATE_PRCKEY,
#                           PRC_KEY,
#                           adm_key, 
#                           missing_value):
    
#     print("\n\n\n !!!!! IN findClosestWeightOrBS !!!!!!!!! \n\n\n")
    
#     print("dict_followed_PRC_of_pat_num[first_START_DATE_PRCKEY][PRC_KEY].keys()",dict_followed_PRC_of_pat_num[first_START_DATE_PRCKEY][PRC_KEY].keys())
    
#     MV = dict_followed_PRC_of_pat_num[first_START_DATE_PRCKEY][PRC_KEY][adm_key][missing_value]
#     first_adm_key=adm_key
#     order_adm_key=int(adm_key.split("_")[-2])
#     row_num=int(adm_key.split("_")[-1])
#     min_order_adm_key=min([int(adm_key_i.split("_")[-2]) for adm_key_i in dict_followed_PRC_of_pat_num[first_START_DATE_PRCKEY][PRC_KEY].keys()])
    
#     # Backward loop
#     #while order_adm_key >= 1 and not MV :
#     while order_adm_key >= min_order_adm_key and MV == 'None' :
#         order_adm_key -= 1 
#         row_num -= 1
#         adm_key = str(order_adm_key) + "_" + str(row_num)
#         print("1- while order_adm_key >= min_order_adm_key and MV == 'None' :")
#         print("1- adm_key : ", adm_key)
#         while adm_key not in dict_followed_PRC_of_pat_num[first_START_DATE_PRCKEY][PRC_KEY] :
#             order_adm_key -= 1
#             row_num -= 1
#             adm_key = str(order_adm_key) + "_" + str(row_num)
#             print("2- while adm_key not in dict_followed_PRC_of_pat_num loop ")
#             print("2- adm_key : ", adm_key)
#         MV = dict_followed_PRC_of_pat_num[first_START_DATE_PRCKEY][PRC_KEY][adm_key][missing_value]
#     if MV != 'None':
#         return parsesstrtofloat(MV)
#     else :
#         adm_key = first_adm_key
#         order_adm_key=int(adm_key.split("_")[-2])
#         row_num=int(adm_key.split("_")[-1])
#         max_order_adm_key=max([int(adm_key_i.split("_")[-2]) for adm_key_i in dict_followed_PRC_of_pat_num[first_START_DATE_PRCKEY][PRC_KEY].keys()])
#         # Foward loop
#         while order_adm_key <= max_order_adm_key and MV == 'None':
#             order_adm_key += 1 
#             row_num += 1
#             adm_key = str(order_adm_key) + "_" + str(row_num)
#             print("3- while adm_key not in dict_followed_PRC_of_pat_num[first_START_DATE_PRCKEY][PRC_KEY]")
#             print("3- adm_key : ", adm_key)
#             while adm_key not in dict_followed_PRC_of_pat_num[first_START_DATE_PRCKEY][PRC_KEY] :
#                 order_adm_key += 1 
#                 row_num += 1
#                 adm_key = str(order_adm_key) + "_" + str(row_num)
#                 print("4-while adm_key not in dict_followed_PRC_of_pat_num[first_START_DATE_PRCKEY][PRC_KEY]")
#                 print("4- adm_key : ", adm_key)
#             MV = dict_followed_PRC_of_pat_num[first_START_DATE_PRCKEY][PRC_KEY][adm_key][missing_value]
#         if MV != 'None':
#             return parsesstrtofloat(MV)
#         else :
#             return -1




# def calculatesNormDose(dose_prescr, unit_code, pat_weight, bodysurf, pat_BD, pat_creat, pat_sex, date_str):
#     if unit_code in [1, 4, 5, 15]:
#         if dose_prescr != 'None' and pat_weight != 'None':
#             dose_norm = dose_prescr/pat_weight
#         else :
#             dose_norm = -1
#     ## 2022-12-01
#     elif unit_code in [7,8]:
#         if pat_BD != 'None' and date_str != 'None' and dose_prescr != 'None' and pat_sex != 'None' :
#             pat_age = calc_age_of_pat(pat_BD, date_str)
#             predicted_CL_carbo = compute_chatelut(dose_prescr, pat_weight ,pat_age, pat_creat, pat_sex)
#             AUC=dose_prescr/predicted_CL_carbo
#             dose_norm = AUC
#         else :
#             dose_norm = -1
#     elif unit_code == 2:
#         if dose_prescr != 'None' and bodysurf != 'None':
#             dose_norm = dose_prescr/bodysurf
#         else:
#             dose_norm = -1
#     else : # dose fixe
#         if dose_prescr != 'None':
#             dose_norm = dose_prescr
#         else :
#             dose_norm = -1
#     return dose_norm