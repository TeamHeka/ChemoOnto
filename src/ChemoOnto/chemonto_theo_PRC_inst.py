from owlready2 import *

import global_variables as gv
from utils import *
from chemonto_TO import *
from chemonto_Romedi import *


"""
Procedures that instantiate ChemoOnto with theoretical protocols using the global theoretical dictionary (gv.dict_theoretical_PRC)
"""



def instantiateTheoreticalDrugAndDrugAdmInds(dict_DrugType_to_ABV, drugType, PRC_KEY, romedi,
                                           dict_day_ind, chemonto_cycle_ind, timeonto_curetime_ind):
    """
    Instantiates Drug and drug administration classes.

    @param dict_DrugType_to_ABV:
    @param drugType:
    @param PRC_KEY:
    @param romedi:
    @param dict_day_ind:
    @param chemonto_cycle_ind:
    @param timeonto_curetime_ind:
    @return:
    """

    # print("drugType", drugType)
    ABV = dict_DrugType_to_ABV[drugType][0]  # 'DCI' or 'PDT'
    name_ABV = dict_DrugType_to_ABV[drugType][1]  # NOMDCI or NOMPDT
    className = dict_DrugType_to_ABV[drugType][2]  # AntiCancer, AntiADE or Solvant
    dict_ABV = dict_DrugType_to_ABV[drugType][3]  # Dict Info
    prefix = dict_DrugType_to_ABV[drugType][4]
    if drugType in gv.dict_theoretical_PRC[PRC_KEY]:
        for TYPE_KEY in gv.dict_theoretical_PRC[PRC_KEY][drugType]:
            if ABV in gv.dict_theoretical_PRC[PRC_KEY][drugType][TYPE_KEY]:
                has_name_drug = dict_ABV[TYPE_KEY][name_ABV]
                #name_mol_drug_class = dict_ABV[TYPE_KEY][name_ABV]
                #name_mol_drug_class = removes_spe_char(name_mol_drug_class)
                label_drug = prefix + "_" + has_name_drug
                id_drug = prefix + "_" + TYPE_KEY
                label_adm_drug = prefix + "_THEO_" + PRC_KEY + "-" + has_name_drug
                id_adm_drug = prefix + PRC_KEY + "_" + TYPE_KEY

                # if name_mol_drug_class not in [c.name for c in gv.chemonto.classes()]:
                #     parent = gv.chemonto[className]
                #     drugClass = types.new_class(name_mol_drug_class, (parent,))
                #     drugClass.label.append(name_mol_drug_class)
                # else:
                #     drugClass = getattr(gv.chemonto, name_mol_drug_class)

                # Instatiating drug ind
                # if id_date_day_descr not in [c.name for c in gv.TIME_ONTO.DateTimeDescription.instances()]:
                #if id_drug not in [c.name for c in gv.chemonto.Drug.instances()]:
                parent = gv.chemonto[className]
                if id_drug not in [c.name for c in parent.instances()]:
                    chemonto_drug_ind = parent(id_drug,
                                                  hasDrugName=has_name_drug
                                                  # provisoire normalement = namedrugs et seuelement rempli pour les AC
                                                  #hasDrugMolecule=has_name_drug
                                                    )
                    chemonto_drug_ind.label.append(label_drug)
                    ### ROMEDI
                    if romedi and "ROMEDI_IND_NAME" in gv.dict_theoretical_PRC[PRC_KEY][drugType][TYPE_KEY][ABV]:
                        # print("ROMEDI theoretical PRC AC \n")
                        RomediType = gv.dict_theoretical_PRC[PRC_KEY][drugType][TYPE_KEY][ABV]["ROMEDI_TYPE"]
                        RomediIndName = gv.dict_theoretical_PRC[PRC_KEY][drugType][TYPE_KEY][ABV]["ROMEDI_IND_NAME"]
                        mappsToRomediInd(RomediType=RomediType, RomediIndName=RomediIndName,
                                         chemontoDrugInd=chemonto_drug_ind)
                else :
                    chemonto_drug_ind = getattr(gv.chemonto, id_drug)
            if 'DRUG_ADM' in gv.dict_theoretical_PRC[PRC_KEY][drugType][TYPE_KEY]:
                instantiatesTheoreticalDrugAdmInd(chemonto_drug_ind, chemonto_cycle_ind, label_adm_drug, id_adm_drug, PRC_KEY,
                                                drugType,TYPE_KEY, dict_day_ind, timeonto_curetime_ind)

    return None



def instantiatesTheoreticalDrugAdmInd(chemonto_drug_ind, chemonto_cycle_ind, label_drug, id_drug,
                                    PRC_KEY, drugType, TYPE_KEY, dict_day_ind, timeonto_curetime_ind):
    ## DRUG ADM
    if 'DRUG_ADM' in gv.dict_theoretical_PRC[PRC_KEY][drugType][TYPE_KEY]:
        adm_i = 0
        for dict_adm in gv.dict_theoretical_PRC[PRC_KEY][drugType][TYPE_KEY]['DRUG_ADM']:

            label_ac_adm = "ADM_" + "_" + str(adm_i) + "_" + label_drug
            id_drug_adm = "ADM_" + "_" + str(adm_i) + "_" + id_drug
            dose_drug_adm = dict_adm["DOSE"]
            dose_drug_adm = float(dose_drug_adm.replace(",", "."))
            unit_code = dict_adm["UNITE"]
            unit_drug_adm = returnsUnit(unit_code)

            # unit_drug_adm_label = returnsUnit(gv.dict_theoretical_PRC[PRC_KEY][drugType][TYPE_KEY]['DRUG_ADM']["UNITE"])
            code_voie_drug_adm = dict_adm["CODEVOIE"]
            duree_adm_drug_adm = dict_adm["DUREEADM"]
            ## 2022-12-13 5FU 
            if int(duree_adm_drug_adm) > 24 :
                #dose_drug_adm = dose_drug_adm * (int(duree_adm_drug_adm)//24)
                dose_drug_adm = dose_drug_adm * round(int(duree_adm_drug_adm)/24) # 46h -> 48h
                
            duree_adm_min_drug_adm = dict_adm["DUREEADMIN"]
            #comment_drug_adm = dict_adm["COMMENTADM"]
            jour_drug_adm = dict_adm["JOURADM"]
            heure_drug_adm = dict_adm["HEUREADM"]
            # BOLUS
            isBolus = isBolusTheoretical(duree_adm_drug_adm, duree_adm_min_drug_adm, code_voie_drug_adm)
            # Drug adm instantiation
            adm_i += 1
            chemonto_drug_adm_ind = gv.chemonto.TheoDrugAdministration(id_drug_adm,
                                                            hasDrug=chemonto_drug_ind,
                                                            isAdministratedIn=chemonto_cycle_ind,
                                                            hasDose=dose_drug_adm,
                                                            hasUnitSTR=unit_drug_adm,
                                                            hasUnitCode=int(unit_code),
                                                            hasDurationInHour=int(duree_adm_drug_adm),
                                                            hasDurationInMin=int(duree_adm_min_drug_adm),
                                                            isBolus=isBolus)
                                                            #hasCodeInjection=code_voie_drug_adm,
                                                            #hasDurationAdm=int(duree_adm_drug_adm),
                                                            #hasDurationAdmin=int(duree_adm_min_drug_adm),
                                                            #hasCommentDrugAdm=comment_drug_adm,
                                                            #hasDayDrugAdm=jour_drug_adm,
                                                            #hasHourDrugAdm=heure_drug_adm,
                                                            
            chemonto_drug_adm_ind.label.append(label_ac_adm)
            gv.chemonto.hasAdministration[chemonto_cycle_ind].append(chemonto_drug_adm_ind)
            chemonto_drug_ind.isDrugOf.append(chemonto_drug_adm_ind)
            # # Unit UO ? On met dans data property pour le moment car ça a l'air nul
            # Time Onto
            linksDrugAdmToDay(jour_drug_adm, dict_day_ind, chemonto_drug_adm_ind, timeonto_curetime_ind)
    return None



def instantiatesTheoreticalPRC(AC, AA, S, romedi):

    dict_DrugType_to_ABV = {}
    if AC:
        dict_DrugType_to_ABV['ANTI_CANCER'] = ['DCI', 'NOMDCI', 'AntiCancer', gv.dict_DCI, "AC"]
    if AA:
        dict_DrugType_to_ABV['ANTI_ADE_CODEPDT'] = ['PDT', 'NOMPDT', 'AntiADE', gv.dict_anti_ade, "AA"]
    if S:
        dict_DrugType_to_ABV['SOLVANT_CODEPDT'] = ['PDT', 'NOMPDT', 'Solvant', gv.dict_solvant, "S"]

    with gv.chemonto:
        for PRC_KEY in gv.dict_theoretical_PRC:

            # 1 - PRC, CYCLE, CURE
            ## info PRC, CYCLE, CURE

            label_prc = "PRC_THEO_" + PRC_KEY + "-" + gv.dict_theoretical_PRC[PRC_KEY]["NOMPROT"]
            has_name_prc = gv.dict_theoretical_PRC[PRC_KEY]["NOMPROT"]
            id_prc = "PRC_" + PRC_KEY
            label_cycle = "CYCLE_THEO_" + PRC_KEY
            id_cycle = "CYCLE_" + PRC_KEY
            label_cure = "CURE_THEO_" + PRC_KEY
            id_cure = "CURE_" + PRC_KEY

            #type_prc = gv.dict_theoretical_PRC[PRC_KEY]["TYPEPROT"]
            duration_cycle = gv.dict_theoretical_PRC[PRC_KEY]["DUREECYCLE"]
            xsd_duration_cycle = "P"+str(duration_cycle)+"D"
            #comment_prc = gv.dict_theoretical_PRC[PRC_KEY]["COMMENTPRO"]
            #supervison_prc = gv.dict_theoretical_PRC[PRC_KEY]["SURVEILLAN"]
            #other_comment_prc = gv.dict_theoretical_PRC[PRC_KEY]["REMARQUES"]
            #nb_cycle_def_prc = gv.dict_theoretical_PRC[PRC_KEY]["NBCYCLEDEF"]
            #utmajpr_prc = gv.dict_theoretical_PRC[PRC_KEY]["UTMAJPR"]
            #cost_prc = parsesstrtofloat(gv.dict_theoretical_PRC[PRC_KEY]["COUTPROT"])
            #max_cycle_prc = gv.dict_theoretical_PRC[PRC_KEY]["MAXCYCLE"]

            ## instantiates PRC, CYCLE, CURE
            chemonto_cycle_ind = gv.chemonto.TheoCycle(id_cycle,
                                       hasCycleDuration = int(duration_cycle),
                                       hasCyclePRCkey = int(PRC_KEY))
            chemonto_cycle_ind.label.append(label_cycle)
            chemonto_cure_ind = gv.chemonto.TheoCure(id_cure,
                                          cureOf = chemonto_cycle_ind)
            chemonto_cure_ind.label.append(label_cure)
            chemonto_prc_ind = gv.chemonto.Protocol(id_prc,
                                        hasCycle = chemonto_cycle_ind,
                                        hasName = has_name_prc
                                        #hasType = type_prc,
                                        #hasCommentProtocol = comment_prc,
                                        #hasOtherCommentProtocol = other_comment_prc,
                                        #hasSupervision = supervison_prc,
                                        #hasNbCycleDef = nb_cycle_def_prc,
                                        #hasUTMAJPR = utmajpr_prc,
                                        #hasCost = cost_prc,
                                        #hasMaxCycle = max_cycle_prc
                                        )
            chemonto_prc_ind.label.append(label_prc)
            #chemonto_prc_ind.comment.append(comment_prc)
            chemonto_cycle_ind.cycleOf = chemonto_prc_ind
            chemonto_cycle_ind.hasCure = chemonto_cure_ind


            ## Time Ontology

            id_cycle_time = "INT_CYCLE_" + PRC_KEY
            label_cycle_time = "INT_CYCLE_THEO_" + PRC_KEY
            id_cure_time = "INT_CURE_" + PRC_KEY
            label_cure_time = "INT_CURE_THEO_" + PRC_KEY

            timeonto_cycletime_ind, timeonto_curetime_ind = instantiatesTheoreticalCycleInt(id_cycle_time,
                                                                                          label_cycle_time,
                                                                                          id_cure_time,
                                                                                          label_cure_time,
                                                                                          xsd_duration_cycle,
                                                                                          chemonto_cycle_ind,
                                                                                          chemonto_cure_ind)
            dict_day_ind = intantiantesDaysofTheoreticalCycleInt(duration_cycle,
                                                               PRC_KEY,
                                                               timeonto_cycletime_ind)



            # 2 - DRUG, DRUG_ADMINISTRATION
            for drugType in dict_DrugType_to_ABV: # 'ANTI_CANCER', 'SOLVANT_CODEPT' et 'ANTI_ADE_CODEPDT':
                instantiateTheoreticalDrugAndDrugAdmInds(dict_DrugType_to_ABV,
                                                       drugType,
                                                       PRC_KEY,
                                                       romedi,
                                                       dict_day_ind,
                                                       chemonto_cycle_ind,
                                                       timeonto_curetime_ind)


    return None
