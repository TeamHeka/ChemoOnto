#from owlready2 import *

import global_variables as gv
from utils import *
from chemonto_TO import *
import re
#import zlib as zlib
#from chemonto_Romedi import *


"""
Procedures that instantiate ChemoOnto with actual patient lines using the global actual lines dictionary (gv.dict_followed_PRC)
"""


def instantiatesFollowedCycle(chemonto_cycle_ind, chemonto_cure_ind, label_cycle, chemonto_pat_ind,
                              chemonto_line_ind, theo_CYCLE_ind, label_cure):
    ## ChemOnto
    chemonto_cycle_ind.label.append(label_cycle)
    gv.chemonto.followedCycle[chemonto_pat_ind].append(chemonto_cycle_ind)
    chemonto_cycle_ind.cycleIsFollowedBy = chemonto_pat_ind
    gv.chemonto.isComposedOfCycle[chemonto_line_ind].append(chemonto_cycle_ind)
    chemonto_cycle_ind.cycleOfLine = chemonto_line_ind
    if theo_CYCLE_ind is not None:
        chemonto_cycle_ind.realisationOf = theo_CYCLE_ind
        gv.chemonto.isRealisedIn[theo_CYCLE_ind].append(chemonto_cycle_ind)
    chemonto_cure_ind.label.append(label_cure)
    return None


def instantiatesFollowedLine(chemonto_line_ind, label_line, chemonto_pat_ind):
    chemonto_line_ind.label.append(label_line)
    # print("Instantiating Followed line")
    # print("chemonto_line_ind", chemonto_line_ind)
    # print("chemonto_pat_ind", chemonto_pat_ind)
    gv.chemonto.followedLine[chemonto_pat_ind].append(chemonto_line_ind)
    chemonto_line_ind.lineIsFollowedBy = chemonto_pat_ind
    return None


def instantiatesFollowedPRCDrug(pat_num, patnum_an , first_START_DATE_PRCKEY, PRC_KEY, adm_key, AC, AA, S, date_str, cycle_num):
    dictDrugType = None
    if AA or S:
        if gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["CONCEPT_CD"][7] == "P":
            MED_KEY = gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["CONCEPT_CD"].split("|")[-1]
            if AA :
                if MED_KEY in gv.dict_anti_ade:
                    dictDrugType = gv.dict_anti_ade
                    prefix = "AA"
                    second_KEY = "NOMPDT"
            if S:
                if MED_KEY in gv.dict_solvant:
                    dictDrugType = gv.dict_solvant
                    prefix = "S"
                    second_KEY = "NOMPDT"
    if AC:
        if gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["CONCEPT_CD"][7] == "D":
            MED_KEY = gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["CONCEPT_CD"].split("|")[-1]
            if MED_KEY in gv.dict_DCI:
                dictDrugType = gv.dict_DCI
                prefix = "AC"
                second_KEY = "NOMDCI"
    if dictDrugType is not None :

        # has_name_drug = dict_ABV[TYPE_KEY][name_ABV]
        # # name_mol_drug_class = dict_ABV[TYPE_KEY][name_ABV]
        # # name_mol_drug_class = removes_spe_char(name_mol_drug_class)
        # label_drug = prefix + "_" + has_name_drug
        # id_drug = prefix + "_" + TYPE_KEY


        # hasdrugname = dictDrugType[MED_KEY][second_KEY]
        # name_drug_class = dictDrugType[MED_KEY][second_KEY]
        # name_drug_class = removes_spe_char(name_drug_class)
        # id_drug = prefix + "_" + pat_num + "_" + date_str + "_" + cycle_num + "_" + MED_KEY + "_" + adm_key
        # label_drug = prefix + "_" + PRC_KEY + "_" + adm_key + "-" + hasdrugname

        hasdrugname = dictDrugType[MED_KEY][second_KEY]
        id_adm_drug = prefix + "_" + patnum_an + "_" + date_str + "_" + cycle_num + "_" + MED_KEY + "_" + adm_key
        label_adm_drug = prefix + "_" + PRC_KEY + "_" + adm_key + "-" + hasdrugname
        id_drug =  prefix + "_" + MED_KEY # retrouver le nom d'individu pour l'instancier

        chemonto_drug_ind = getattr(gv.theo_chemonto, id_drug)


        # ## Drug instantiation
        # chemonto_drug_class = getattr(gv.chemonto, name_drug_class)
        # chemonto_drug_ind = chemonto_drug_class(id_drug, hasDrugName=hasdrugname)
        # chemonto_drug_ind.label.append(label_drug)

        # if romedi:
        #     romedi = checkRomediInDict(dictDrugType[MED_KEY])
        #     if romedi:
        #         RomediType, RomediIndName = returnsRomediTypeAndIndName(dictDrugType[MED_KEY])
        #         mappsToRomediInd(RomediType=RomediType, RomediIndName=RomediIndName,
        #                          chemontoDrugInd=chemonto_drug_ind)

        return chemonto_drug_ind, id_adm_drug, label_adm_drug
    else:
        # print("\n\n")
        # print("dictDrugType is None")
        # print("\n\n")
        return None

    
def instantiatesStopInst(timeonto_int_ind, id_stop, label_stop, date_str):

    timeonto_stop_ind = gv.TIME_ONTO.Instant(id_stop)
    xsd_date = date.fromisoformat(date_str)
    timeonto_stop_ind.inXSDDate.append(xsd_date)
    timeonto_stop_ind.label.append(label_stop)
    gv.TIME_ONTO.hasEnd[timeonto_int_ind].append(timeonto_stop_ind)
    return None
    



def instantiatesFollowedPRC(AC, AA, S, pat_num, patnum_an, chemontotox_pat_ind):
    
    # patnum_an = str(zlib.crc32(pat_num.encode('utf-8'))) #anonymize
    # chemontotox_pat_ind = gv.patientInChemOntoToxGraph(patnum_an, chemontotox_file)
    
    #print("[pat_num for pat_num.name in gv.chemontotox.Patient.instances()]", [pat_num.name for pat_num in gv.chemontotox.Patient.instances()])
    
    with gv.chemonto:
        #chemonto_pat_ind = gv.chemontotox.Patient(pat_num)
        # LINE, (and CANCERTEYPE ?)
        for first_START_DATE_PRCKEY in gv.dict_followed_PRC[pat_num]:
            for PRC_KEY in gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY]:
                FLAG = False # note the first cycle for stop instants
                first_key_adm = list(gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY].keys())[0] # wont change of PRCNAME
                PRC_NAME = gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][first_key_adm]["PROTO"]

                ## Line Instantiation
                id_line = "LINE_" + patnum_an + "_" + first_START_DATE_PRCKEY
                label_line = "LINE_" + first_START_DATE_PRCKEY + "-" + PRC_NAME
                FIRST_DATE = re.sub(r'_[0-9]{1,5}', "", first_START_DATE_PRCKEY)
                FIRST_DATE = FIRST_DATE.replace("_None", "")

                hasLinePCKEY = parseHasLinePRCKEY(PRC_KEY)

                if id_line not in [c.name for c in gv.chemonto.Line.instances()]:
                    chemonto_line_ind = gv.chemonto.Line(id_line,
                                                  hasProtocolName=PRC_NAME,
                                                  hasC1D1Date=FIRST_DATE,
                                                  hasLinePRCkey = hasLinePCKEY)
                    instantiatesFollowedLine(chemonto_line_ind, label_line, chemontotox_pat_ind)


                    ## Time Ontology
                    id_line_int = "INT_LINE_" + patnum_an + "_" + FIRST_DATE + "_" + PRC_KEY
                    label_line_int = "INT_LINE_" + PRC_KEY

                    id_line_start = "START_LINE_" + patnum_an + "_" + FIRST_DATE + "_" + PRC_KEY
                    label_line_start = "START_LINE_" + "_" + PRC_KEY + "-" + FIRST_DATE
                    instantiatesStartInstAndInt(chemonto_ind=chemonto_line_ind,  id_start=id_line_start,
                                                    label_start=label_line_start, id_int=id_line_int,
                                                    label_int=label_line_int, date_str=FIRST_DATE)
                    timeonto_line_int_ind = getattr(gv.chemonto, id_line_int)
                else :
                    chemonto_line_ind = getattr(gv.chemonto, id_line)

                # CYCLE, DRUG, DRUG ADMINISTRATION
                for adm_key in gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY]:
                    #admkey = adm_key.lower().replace("_","")
                    # end inst of last CURE
                    if FLAG and gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["CYCLE"] != cycle_num: # that means the last admission was for the last cycle, and we can note the end of cure and cycle
                        ## Time Ontology
                        ### CYCLE and CURE STOP inst
                        #### CURE
                        cycle_start_date = id_cycle_start.split("_")[-2] 
                        id_cure_stop = "STOP_CURE_" + PRC_KEY + "_" + patnum_an + "_" + date_str + "_" + cycle_num
                        label_cure_stop = "STOP_CURE_" + PRC_KEY + "_" + cycle_num + "-" + date_str
                        instantiatesStopInst(timeonto_cure_int_ind, id_cure_stop, label_cure_stop, date_str)
                        #### CYCLE
                        date_str = gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["START_DATE"] # day just before the actual cycle
                        day_date_before = returns_day_date_before_date(date_str = date_str,
                                                                       cycle_start_date = cycle_start_date,
                                                                       patnum = pat_num,
                                                                       adm_key = adm_key,
                                                                       path_d2_before_d1 = gv.cfg["log_files"]["d2_before_d1"])
                        # returns_day_date_before_date(date_str,cycle_start_date,patnum, path_d2_before_d1)
                        id_cycle_stop = "STOP_CYCLE_" + PRC_KEY + "_" + patnum_an + "_" + day_date_before + "_" + cycle_num
                        label_cycle_stop = "STOP_CYCLE_" + PRC_KEY + "_" + cycle_num + "-" + day_date_before
                        instantiatesStopInst(timeonto_cycle_int_ind, id_cycle_stop, label_cycle_stop, day_date_before)

                    ## ADM and CYCLE infos :
                    FLAG = True
                    cycle_num = gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["CYCLE"]
                    date_str = gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["START_DATE"]
                    dose_prescr = parsesstrtofloat(gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["NVAL_NUM"])
                    day_str = gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["JOUR"]
                    reduction_str = gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["REDUCTION"]
                    motif_str = gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["MOTIF"]
                    localisation = gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["LOCALISATION"]
                    day_drugadm_num = gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["JOUR"]
                    
                    pat_BD = gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["BIRTH_DATE"]
                    pat_sex = gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["SEX_CD"]
                    pat_weight = parsesstrtofloat(gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["POIDS"])
                    pat_height = parsesstrtofloat(gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["TAILLE"])
                    pat_creat = parsesstrtofloat(gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["CREAT"])
                    voie = gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["NOMVOIE"]
                    #bodysurf = parsesstrtofloat(gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["SCPATPRE"])
                    bodysurf = returnBodySurf(SCPATPRE=gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["SCPATPRE"], SCPATBOYD=gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["SCPATBOYD"])
                    #bodysurfBoyd = parsesstrtofloat(gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["SCPATBOYD"])
                    unit_code = int(gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["UNITE"])
                    unit_str = returnsUnit(unit_code)
                    dureeadm , dureeadmin = parsesadminduration(gv.dict_followed_PRC[pat_num][first_START_DATE_PRCKEY][PRC_KEY][adm_key]["DUREEADM"])

                    isBolus = isBolusFollowed(dureeadm, dureeadmin, voie)
                    
                    ## NVAL_NUM, UNITE SEX AND START_DATE, BIRTH DATE are never NULL. 
                    ## Possible value on pat_weight, bodysurface, creat. Algo to retrieve it depending on unit.
                    
                    missing_values_for_data = []
                    
                    
                    if unit_code in [1, 4, 5, 15]: # dose_unit/kg -> POIDS
                        if pat_weight == -1:
                            pat_weight, way = findClosestMissingValue(dict_followed_PRC_of_pat_num = gv.dict_followed_PRC[pat_num], 
                                                                   first_START_DATE_PRCKEY = first_START_DATE_PRCKEY,
                                                                   PRC_KEY = PRC_KEY,
                                                                   current_adm_key = adm_key, 
                                                                   missing_value = "POIDS")
                            if "POIDS" + "_" + way not in missing_values_for_data : 
                                missing_values_for_data.append("POIDS" + "_" + way)
                            
                        dose_norm = calculatesNormDose_weight(dose_prescr, pat_weight)
                        # if dose_norm < 0 :
                        #     print("1-POIDS-dose_norm <0 :")
                        #     print("pat_weight", pat_weight)
                        #     print("dose_prescr", dose_prescr)
                        #     print("adm_key", adm_key)
                            
                    elif unit_code in [7,8]: # AUC carbo -> POIDS and CREAT
                        if dose_prescr != 0 : # sometimes CREAT = 0 but in these cases NVAL_NUM always = 0
                            if pat_weight == -1:
                                pat_weight, way = findClosestMissingValue(dict_followed_PRC_of_pat_num = gv.dict_followed_PRC[pat_num], 
                                                                       first_START_DATE_PRCKEY = first_START_DATE_PRCKEY,
                                                                       PRC_KEY = PRC_KEY,
                                                                       current_adm_key = adm_key, 
                                                                       missing_value = "POIDS")
                                if "POIDS" + "_" + way not in missing_values_for_data : 
                                    missing_values_for_data.append("POIDS" + "_" + way)
                            if pat_creat == -1 :
                                pat_creat, way = findClosestMissingValue(dict_followed_PRC_of_pat_num = gv.dict_followed_PRC[pat_num], 
                                                                       first_START_DATE_PRCKEY = first_START_DATE_PRCKEY,
                                                                       PRC_KEY = PRC_KEY,
                                                                       current_adm_key = adm_key, 
                                                                       missing_value = "CREAT")
                                if "CREAT"+ "_" + way not in missing_values_for_data : 
                                    missing_values_for_data.append("CREAT" + "_" + way)

                            dose_norm = calculatesNormDose_carbo(dose_prescr, pat_weight, pat_BD, pat_creat, pat_sex, date_str)
                        else:
                            dose_norm = 0
                        # if dose_norm < 0 :
                        #     print("2-CARBO-dose_norm <0 :")
                        #     print("pat_weight", pat_weight)
                        #     print("pat_creat", pat_creat)
                        #     print("pat_BD", pat_BD)
                        #     print("pat_sex", pat_sex)
                        #     print("date_str", date_str)
                        #     print("dose_prescr", dose_prescr)
                        #     print("adm_key", adm_key)
                            
                    elif unit_code == 2: # BODYSURF
                        if bodysurf == -1:
                            bodysurf, way = findClosestMissingValue(dict_followed_PRC_of_pat_num = gv.dict_followed_PRC[pat_num], 
                                                                   first_START_DATE_PRCKEY = first_START_DATE_PRCKEY,
                                                                   PRC_KEY = PRC_KEY,
                                                                   current_adm_key = adm_key, 
                                                                   missing_value = "SCPATBOYD")
                            if "SCPATBOYD"+ "_" + way not in missing_values_for_data : 
                                missing_values_for_data.append("SCPATBOYD" + "_" + way)
                            
                        dose_norm = calculatesNormDose_bodysurf(dose_prescr, bodysurf)
                        # if dose_norm < 0 :
                        #     print("3-SCPATBOYD-dose_norm <0 :")
                        #     print("bodysurf",bodysurf)
                        #     print("dose_prescr", dose_prescr)
                        #     print("adm_key", adm_key)
                    
                    else : # Fixed dose
                        dose_norm = dose_prescr
                        # if dose_norm < 0 :
                        #     print("4-DOSEFIXE-dose_norm <0 :")
                        #     print("dose_prescr", dose_prescr)
                        #     print("unite", unit_code)
                        #     print("adm_key", adm_key)
                        
                        
                    if dose_norm < 0 :
                        one_data_is_always_None(path_to_log_file = gv.cfg["log_files"]["data_always_None"], 
                                                patnum = pat_num,
                                                missing_values_list = missing_values_for_data,
                                                adm_key = adm_key)

                    ## Time Ontology
                    ### DAY
                    
                    ### 2022-10-04 :
                    id_day_inst = "DAY_" + "_" + PRC_KEY + "_" + patnum_an + "_" + cycle_num + "_" + day_str + "_" + date_str
                    label_day_inst = "DAY_" + "_" + PRC_KEY + "_" + cycle_num + "_" + day_str + "-" + date_str
                    if id_day_inst not in [c.name for c in gv.TIME_ONTO.Instant.instances()]:
                        timeonto_day_inst = instantiatesDayInst(id_day=id_day_inst,
                                                                label_day=label_day_inst,
                                                                date_str=date_str)
                    else:
                        timeonto_day_inst = getattr(gv.chemonto, id_day_inst, label_day_inst)
                    
                    
                    ### 2022-10-03 :
                    # Finally option Date-Time interval, with "inXDSDateTime" data property and without "has Date-Time description"
                    # object property because of datatype problems.
                    
                    # id_day_int = "DAY_" + "_" + PRC_KEY + "_" + pat_num + "_" + cycle_num + "_" + day_str + "_" + date_str
                    # label_day_int = "DAY_" + "_" + PRC_KEY + "_" + cycle_num + "_" + day_str + "-" + date_str
                    # if id_day_int not in [c.name for c in gv.TIME_ONTO.DateTimeInterval.instances()]:
                    #     timeonto_day_int = gv.TIME_ONTO.DateTimeInterval(id_day_int)
                    #     instantiatesDateTimeIntAndDesc2(timeonto_day_int, label_day_int, date_str)
                    # else :
                    #     timeonto_day_int = getattr(gv.chemonto, id_day_int, label_day_int)
                    
                    

                    ### 2022-09-14 :
                    # either timeonto_day is an Instant, and you use the data poperty inXSDDate to define absolute date
                    # or it's a Date-Time interval; subclass of Interval, and you use object property "has Date-Time description"
                    # Here we choose the first option, so timeonto_day_int become timeonto_day_inst
                    
                    # TOMORROW to comment
                    # id_day_inst = "DAY_" + "_" + PRC_KEY + "_" + pat_num + "_" + cycle_num + "_" + day_str + "_" + date_str
                    # label_day_inst = "DAY_" + "_" + PRC_KEY + "_" + cycle_num + "_" + day_str + "-" + date_str
                    # if id_day_inst not in [c.name for c in gv.TIME_ONTO.Instant.instances()]:
                    #     timeonto_day_inst = instantiatesDayInst(id_day=id_day_inst,
                    #                                             label_day=label_day_inst,
                    #                                             date_str=date_str)
                    # else:
                    #     timeonto_day_inst = getattr(gv.chemonto, id_day_inst, label_day_inst)

                    ### Before 2022-09-14:

                    # id_day_int = "DAY_" + "_" + PRC_KEY + "_" + pat_num + "_" + cycle_num + "_" + day_str + "_" + date_str
                    # label_day_int = "DAY_" + "_" + PRC_KEY + "_" + cycle_num + "_" + day_str + "-" + date_str
                    # if id_day_int not in [c.name for c in gv.TIME_ONTO.DateTimeInterval.instances()]:
                    #     timeonto_day_int = gv.TIME_ONTO.DateTimeInterval(id_day_int)
                    #     instantiatesDateTimeIntAndDesc(timeonto_day_int, label_day_int, date_str)
                    # else :
                    #     timeonto_day_int = getattr(gv.chemonto, id_day_int, label_day_int)
                    
                    
                    ###


                    # Drug instantiation
                    #pat_num, first_START_DATE_PRCKEY, PRC_KEY, adm_key, AC, AA, S, romedi, date_str, cycle_num
                    #chemonto_drug_ind, id_drug, label_drug
                    infos_drug_ind = instantiatesFollowedPRCDrug(pat_num=pat_num,
                                                                 patnum_an=patnum_an,
                                                                first_START_DATE_PRCKEY=first_START_DATE_PRCKEY,
                                                                PRC_KEY=PRC_KEY,
                                                                adm_key=adm_key,
                                                                AC=AC,
                                                                AA=AA,
                                                                S=S,
                                                                date_str=date_str,
                                                                cycle_num=cycle_num)


                    # Cycle instantiation
                    id_cycle = "CYCLE_" + PRC_KEY + "_" + patnum_an + "_" + FIRST_DATE + "_" + cycle_num
                    label_cycle = "CYCLE_" + PRC_KEY + "_" + FIRST_DATE + "_" + cycle_num
                    id_cure = "CURE_" + PRC_KEY + "_" + patnum_an + "_" + FIRST_DATE + "_" + cycle_num
                    label_cure = "CURE_" + PRC_KEY + "_" + FIRST_DATE + "_" + cycle_num
                    if id_cycle not in [c.name for c in gv.chemonto.Cycle.instances()]:

                        if PRC_KEY != "None":
                            theo_CYCLE_id = "CYCLE_" + PRC_KEY
                            #theo_CYCLE_ind = getattr(gv.chemonto, theo_CYCLE_id)
                            theo_CYCLE_ind = getattr(gv.theo_chemonto, theo_CYCLE_id)
                        else :
                            theo_CYCLE_ind = None

                        chemonto_cycle_ind = gv.chemonto.Cycle(id_cycle,
                                                        hasCycleNum=int(cycle_num))

                        chemonto_cure_ind = gv.chemonto.Cure(id_cure)

                        id_cycle_int = "INT_CYCLE_" + PRC_KEY + "_" + patnum_an + "_" + date_str + "_" + cycle_num
                        label_cycle_int = "INT_CYCLE_" + PRC_KEY + "_" + cycle_num + "-" + date_str

                        id_cycle_start = "START_CYCLE_" + PRC_KEY + "_" + patnum_an + "_" + date_str + "_" + cycle_num
                        label_cycle_start = "START_CYCLE_" + PRC_KEY + "_" + cycle_num + "-" + date_str

                        id_cure_int = "INT_CURE_" + PRC_KEY + "_" + patnum_an + "_" + date_str + "_" + cycle_num
                        label_cure_int = "INT_CURE_" + PRC_KEY + "_" + cycle_num + "-" + date_str

                        id_cure_start = "START_CURE_" + PRC_KEY + "_" + patnum_an + "_" + date_str + "_" + cycle_num
                        label_cure_start = "START_CURE_" + PRC_KEY + "_" + cycle_num + "-" + date_str


                        instantiatesFollowedCycle(chemonto_cycle_ind, chemonto_cure_ind, label_cycle,
                                                  chemontotox_pat_ind, chemonto_line_ind, theo_CYCLE_ind, label_cure)

                        instantiatesStartInstAndInt(chemonto_ind=chemonto_cycle_ind, id_start=id_cycle_start,
                                                    label_start=label_cycle_start, id_int=id_cycle_int,
                                                    label_int=label_cycle_int, date_str=date_str)

                        instantiatesStartInstAndInt(chemonto_ind=chemonto_cure_ind, id_start=id_cure_start,
                                                    label_start=label_cure_start, id_int=id_cure_int,
                                                    label_int=label_cure_int, date_str=date_str)

                        timeonto_cycle_int_ind = getattr(gv.chemonto, id_cycle_int)

                        timeonto_cycle_start_ind = getattr(gv.chemonto, id_cycle_start)

                        timeonto_cure_int_ind = getattr(gv.chemonto, id_cure_int)

                        timeonto_cure_start_ind = getattr(gv.chemonto, id_cure_start)

                    else:
                        chemonto_cycle_ind = getattr(gv.chemonto, id_cycle)
                        #chemonto_cycle_ind.label.append(label_cycle)


                    # Drug adm instantiation
                    if infos_drug_ind is not None :
                        chemonto_drug_ind, id_adm_drug, label_adm_drug = infos_drug_ind
                        id_drug_adm = "ADM_" + id_adm_drug
                        label_drug_adm = "ADM_" + label_adm_drug
                        chemonto_drug_adm_ind = gv.chemonto.DrugAdministration(id_drug_adm,
                                                                        hasDrug=chemonto_drug_ind,
                                                                        isAdministratedIn=chemonto_cycle_ind,
                                                                        hasDoseNorm = dose_norm,
                                                                        hasReductionMotif=motif_str,
                                                                        isBolus=isBolus,
                                                                        hasCancerLocation=localisation,
                                                                        hasDose = dose_prescr,
                                                                        hasUnitSTR = unit_str,
                                                                        hasPatBS = bodysurf,
                                                                        hasPatWeight = pat_weight,
                                                                        hasDurationInHour=int(dureeadm),
                                                                        hasDurationInMin=int(dureeadmin))
                        chemonto_drug_adm_ind.label.append(label_drug_adm)
                        gv.chemonto.hasAdministration[chemonto_cycle_ind].append(chemonto_drug_adm_ind)
                        
                        if len(missing_values_for_data) > 0 :
                            for data in missing_values_for_data :
                                gv.chemonto.hasMissingValues[chemonto_drug_adm_ind].append(data)
                        #gv.chemonto.hasDrug[chemonto_drug_adm_ind].append(chemonto_drug_ind) 2022-10-25 
                        try :
                            gv.chemonto.hasDrug[chemonto_drug_adm_ind].append(chemonto_drug_ind)
                        except AttributeError:
                             addPatNumToAttributeErrorFile(path_to_log_file = gv.cfg["log_files"]["attribute_error"],
                                                          patnum = pat_num,
                                                          prop = "hasDrug",
                                                          chemonto_drug_ind = str(chemonto_drug_ind),
                                                          chemonto_drug_adm_ind_label = label_drug_adm)
                        try :
                            chemonto_drug_ind.isDrugOf.append(chemonto_drug_adm_ind)
                        except AttributeError:
                            addPatNumToAttributeErrorFile(path_to_log_file = gv.cfg["log_files"]["attribute_error"],
                                                          patnum = pat_num,
                                                          prop = "isDrugOf",
                                                          chemonto_drug_ind = str(chemonto_drug_ind),
                                                          chemonto_drug_adm_ind_label = label_drug_adm)
                        try :
                            gv.chemonto.hasDayDrugAdm[chemonto_drug_adm_ind].append(int(day_drugadm_num))
                        except AttributeError:
                            addPatNumToAttributeErrorFile(path_to_log_file = gv.cfg["log_files"]["attribute_error"],
                                                          patnum = pat_num,
                                                          prop = "hasDayDrugAdm",
                                                          chemonto_drug_ind = str(chemonto_drug_ind),
                                                          chemonto_drug_adm_ind_label = label_drug_adm)
                        try :
                            gv.TIME_ONTO.hasTime[chemonto_drug_adm_ind].append(timeonto_day_inst)
                        except AttributeError:
                            addPatNumToAttributeErrorFile(path_to_log_file = gv.cfg["log_files"]["attribute_error"],
                                                          patnum = pat_num,
                                                          prop = "hasTime",
                                                          chemonto_drug_ind = str(chemonto_drug_ind),
                                                          chemonto_drug_adm_ind_label = label_drug_adm)
                        
                        #gv.chemonto.hasDayDrugAdm[chemonto_drug_adm_ind].append(int(day_drugadm_num)) # 2022-10-25
                        #gv.TIME_ONTO.hasTime[chemonto_drug_adm_ind].append(timeonto_day_inst) # 2022-10-25
                        
                        #gv.TIME_ONTO.hasTime[chemonto_drug_adm_ind].append(timeonto_day_int)
            CNDN=date_str
            gv.chemonto.hasCNDNDate[chemonto_line_ind].append(CNDN)
            # Time Ontology
            ## CYCLE an CURE stop inst

            id_cure_stop = "STOP_CURE_" + PRC_KEY + "_" + patnum_an + "_" + CNDN + cycle_num
            label_cure_stop = "STOP_CURE_" + PRC_KEY + "_" + cycle_num + "-" + CNDN

            instantiatesStopInst(timeonto_cure_int_ind, id_cure_stop, label_cure_stop, CNDN)

            id_cycle_stop = "STOP_CYCLE_" + PRC_KEY + "_" + patnum_an + "_" + CNDN + cycle_num
            label_cycle_stop = "STOP_CYCLE_" + PRC_KEY + "_" + cycle_num + "-" + CNDN

            instantiatesStopInst(timeonto_cycle_int_ind, id_cycle_stop, label_cycle_stop, CNDN)

            ## LINE stop inst
            id_line_stop = "STOP_LINE_" + PRC_KEY + "_" + patnum_an + "_" + CNDN
            label_line_stop = "STOP_LINE_" + PRC_KEY + "-" + CNDN

            instantiatesStopInst(timeonto_line_int_ind, id_line_stop, label_line_stop, CNDN)




    return None



## 2022-12-13

def patientInChemOntoToxGraph(patnum, pat_BD, pat_DD, pat_SEX, chemontotox_file):
    #patnum = str(zlib.crc32(patnum.encode('utf-8'))) #anonymize
    #print("in patientInChemOntoToxGraph, chemontotox_file : ", chemontotox_file)
    with gv.chemontotox :
        if patnum not in [c.name for c in gv.chemontotox.Patient.instances()]:
            chemontotox_pat_ind = gv.chemontotox.Patient(patnum,
                                                     hasBirthDate = pat_BD,
                                                     hasDeathDate = pat_DD,
                                                     hasGender = pat_SEX)
            gv.chemontotox.save(chemontotox_file)
            #print("\n Patient added to " + chemontotox_file + ".\n\n" )
        else :
            chemontotox_pat_ind = getattr(gv.chemontotox, patnum)
    return chemontotox_pat_ind