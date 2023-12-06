from owlready2 import *

import global_variables as gv
from utils import *

"""
Procedures that instantiate Romedi classes to represent and standarize chemotherapy drugs. https://github.com/scossin/RomediApp
"""


## Theoretical

def mappsToRomediInd(RomediType, RomediIndName, chemontoDrugInd):
    RomediInd = getattr(gv.ROMEDI, RomediIndName)
    #print("RomediInd.is_a")
    #print(RomediInd.is_a)
    #print("RomediInd.equivalent_to")
    #print(RomediInd.equivalent_to)
    if RomediType == "IN":
        gv.chemonto.isRelatedToRomIN[chemontoDrugInd].append(RomediInd)
        #gv.chemonto.isRelatedToChemDrugIN[RomediInd].append(chemontoDrugInd)
    elif RomediType == "BNdosage":
        gv.chemonto.isRelatedToRomBNdosage[chemontoDrugInd].append(RomediInd)
        # gv.chemonto.isRelatedToChemDrugBNdosage[RomediInd].append(chemontoDrugInd)
        # Search for inverse properties to get the IN
        list_inv_properties = list(RomediInd.get_inverse_properties())
        RomediINind = getsRomediINInd(list_inv_properties)
        # Enlevé :
        #gv.chemonto.BNdosageHasIN[RomediInd].append(RomediINind)
        # Ajouté :
        gv.chemonto.isRelatedToRomIN[chemontoDrugInd].append(RomediINind)
    elif RomediType == "BN":
        gv.chemonto.isRelatedToRomBN[chemontoDrugInd].append(RomediInd)
        #gv.chemonto.isRelatedToChemDrugBN[RomediInd].append(chemontoDrugInd)
        # Search for inverse properties to get the IN
        list_inv_properties = list(RomediInd.get_inverse_properties())
        RomediINind = getsRomediINInd(list_inv_properties)
        # Enlevé :
        #gv.chemonto.BNHasIN[RomediInd].append(RomediINind)
        # Ajouté :
        gv.chemonto.isRelatedToRomIN[chemontoDrugInd].append(RomediINind)
    else :
        # other Romedi type
        with open(cfg["romediapp"]["other_type"], "a") as f:
            f.write(RomediType + ":" + RomediIndName + "\n")
    return None



def getsRomediINInd(res):
    if type(res[0][0]) == gv.ROMEDI.CIS:
        RomediCISInd = res[0][0]
        RomediPINdosageInd = getattr(RomediCISInd, "CIShasPINdosage")[0]
        RomediINdosageInd = getattr(RomediPINdosageInd, "PINdosagehasINdosage")[0]
        #print(type(getattr(RomediINdosageInd, "INdosagehasIN")))
        # if (len(getattr(RomediINdosageInd, "INdosagehasIN"))) > 1:
        #     print('getattr(RomediINdosageInd, "INdosagehasIN")', getattr(RomediINdosageInd, "INdosagehasIN"))
        #     print()
        #     print('getattr(RomediINdosageInd, "INdosagehasIN")[0]', getattr(RomediINdosageInd, "INdosagehasIN")[0])
        RomediINInd = getattr(RomediINdosageInd, "INdosagehasIN")[0]
        return RomediINInd
    else :
        RomediInd = res[0][0]
        res = list(RomediInd.get_inverse_properties())
        return getsRomediINInd(res)


# def RxCUItoATCDict():
#     dict_cui_to_atc = {}
#     with open(cfg["rxnorm"]["rxcui_atc"], 'r') as f:
#         lines = f.readlines()
#     for line in lines:
#         ATC, RxCUI = line.split("|")
#         dict_cui_to_atc[ATC] = RxCUI
#     return dict_cui_to_atc


def getsRxCUIandATC7(res):
    if type(res[0][0]) == gv.ROMEDI.CIS:
        RomediCISInd = res[0][0]
        ATCInd=  getattr(RomediCISInd, "CIShasATC7")[0]
        RomediPINdosageInd = getattr(RomediCISInd, "CIShasPINdosage")[0]
        RomediINdosageInd = getattr(RomediPINdosageInd, "PINdosagehasINdosage")[0]
        #print(type(getattr(RomediINdosageInd, "INdosagehasIN")))
        # if (len(getattr(RomediINdosageInd, "INdosagehasIN"))) > 1:
        #     print('getattr(RomediINdosageInd, "INdosagehasIN")', getattr(RomediINdosageInd, "INdosagehasIN"))
        #     print()
        #     print('getattr(RomediINdosageInd, "INdosagehasIN")[0]', getattr(RomediINdosageInd, "INdosagehasIN")[0])
        RomediINInd = getattr(RomediINdosageInd, "INdosagehasIN")[0]
        return RomediINInd
    else :
        RomediInd = res[0][0]
        res = list(RomediInd.get_inverse_properties())
        return getsRxCUIandATC7(res)


def ATCtoRxCUIDict():
    dict_atc_to_cui = {}
    with open(cfg["rxnorm"]["rxcui_atc"], 'r') as f:
        lines = f.readlines()
    for line in lines:
        ATC, RxCUI = line.split("|")
        dict_atc_to_cui_to_atc[ATC] = RxCUI
    return dict_atc_to_cui


## Followed

def checkRomediInDict(dict_drug_type_MED_KEY):
    if "ROMEDI_IND_NAME" not in dict_drug_type_MED_KEY:
        return False
    else:
        return True


def returnsRomediTypeAndIndName(dict_drug_type_MED_KEY):
    RomediType = dict_drug_type_MED_KEY["ROMEDI_TYPE"]
    RomediIndName = dict_drug_type_MED_KEY["ROMEDI_IND_NAME"]
    return RomediType, RomediIndName


# def mappsToRomediInd(RomediType, RomediIndName, chemontoDrugInd):
#     RomediInd = getattr(gv.ROMEDI, RomediIndName)
#     #print("RomediInd.is_a")
#     #print(RomediInd.is_a)
#     #print("RomediInd.equivalent_to")
#     #print(RomediInd.equivalent_to)
#     if RomediType == "IN":
#         #gv.chemonto.isRelatedToRomIN[chemontoDrugInd].append(RomediInd)
#         #gv.chemonto.isRelatedToChemDrugIN[RomediInd].append(chemontoDrugInd)
#         chemontoDrugInd.equivalent_to.append(RomediInd)
#     elif RomediType == "BNdosage":
#         #gv.chemonto.isRelatedToRomBNdosage[chemontoDrugInd].append(RomediInd)
#         #gv.chemonto.isRelatedToChemDrugBNdosage[RomediInd].append(chemontoDrugInd)
#         # Search for inverse properties to get the IN
#         list_inv_properties = list(RomediInd.get_inverse_properties())
#         RomediINind = getsRomediINInd(list_inv_properties)
#         # Enlevé :
#         #gv.chemonto.BNdosageHasIN[RomediInd].append(RomediINind)
#         # Ajouté :
#         #gv.chemonto.isRelatedToRomIN[chemontoDrugInd].append(RomediINind)
#         chemontoDrugInd.equivalent_to.append(RomediINind)
#     elif RomediType == "BN":
#         #gv.chemonto.isRelatedToRomBN[chemontoDrugInd].append(RomediInd)
#         #gv.chemonto.isRelatedToChemDrugBN[RomediInd].append(chemontoDrugInd)
#         # Search for inverse properties to get the IN
#         list_inv_properties = list(RomediInd.get_inverse_properties())
#         RomediINind = getsRomediINInd(list_inv_properties)
#         # Enlevé :
#         #gv.chemonto.BNHasIN[RomediInd].append(RomediINind)
#         # Ajouté :
#         #gv.chemonto.isRelatedToRomIN[chemontoDrugInd].append(RomediINind)
#         chemontoDrugInd.equivalent_to.append(RomediINind)
#     else :
#         # other Romedi type
#         with open(cfg["romediapp"]["other_type"], "a") as f:
#             f.write(RomediType + ":" + RomediIndName + "\n")
#     return None