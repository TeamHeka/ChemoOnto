import yaml, json
from owlready2 import *

"""
Global variables with dictionaries and external ontologies
"""

### Dictionaries

def initDictDCI():
    """
    initialize/reinitialize an empty global anti-cancer molecule dictionary (gv.dict_DCI)
    @return: None
    """
    global dict_DCI
    dict_DCI = {}
    return None

def initDictDCIFromJson(path_dict_DCI):
    """
    Loads a global anti-cancer molecule dictionary (gv.dict_DCI) from a json file.
    @param path_dict_DCI:
    @return:
    """
    global dict_DCI
    with open(path_dict_DCI, encoding='utf-8') as fh:
        dict_DCI = json.load(fh)
    return None


def initDictAntiADE():
    """
    initialize/reinitialize an empty global anti adverse event drug dictionary (gv.dict_anti_ade)
    @return: None
    """
    global dict_anti_ade
    dict_anti_ade = {}
    return None

def initDictAntiADEFromJson(path_dict_anti_ade):
    """
    Loads a global anti-adverse event drug dictionary (gv.dict_anti_ade) from a json file.
    @param path_dict_anti_ade:
    @return:
    """
    global dict_anti_ade
    with open(path_dict_anti_ade, encoding='utf-8') as fh:
        dict_anti_ade = json.load(fh)
    return None


def initDictSolvant():
    """
    initialize/reinitialize an empty global solvant dictionary (gv.dict_solvant)
    @return: None
    """
    global dict_solvant
    dict_solvant = {}
    return None

def initDictSolvantFromJson(path_dict_solvant):
    """
    Loads a global solvant event drug dictionary (gv.dict_solvant) from a json file.
    @param path_dict_solvant:
    @return:
    """
    global dict_solvant
    with open(path_dict_solvant, encoding='utf-8') as fh:
        dict_solvant = json.load(fh)
    return None

def initDictTheoreticalPRC():
    """
    initialize/reinitialize an empty global theoretical protocols dictionary (gv.dict_theoretical_PRC)
    @return: None
    """
    global dict_theoretical_PRC
    dict_theoretical_PRC = {}
    return None

def initDictFollowedPRC():
    """
    initialize/reinitialize an empty global followed lines dictionary (gv.dict_followed_PRC)
    @return:
    """
    global dict_followed_PRC
    dict_followed_PRC = {}
    return None


def initDictPatToChimioData(patnum, path_to_CHIMIOData_dict):
    global dict_patchimiodata
    with open(path_to_CHIMIOData_dict, "r") as ymlfile:
        dict_pat_to_chimiodata = yaml.safe_load(ymlfile)
    dict_patchimiodata = dict_pat_to_chimiodata[patnum]
    return None


### ChemOnto

#### Theoretical #non
def initChemOntoWithNamespace(name_space):
    global chemonto
    chemonto = get_ontology(name_space)
    return None

#### Followed #non
def initChemOntoWithPath(path_owl, name_owl):
    global chemonto
    chemonto = get_ontology(path_owl + name_owl).load()
    return None


# def reInitChemOntoWithPath(path_owl, name_owl):
#     global chemonto
#     chemonto = get_ontology(path_owl + name_owl).load(only_local=True)


def initTheoChemOntoWithPath(path_owl, name_owl):
    global theo_chemonto
    theo_chemonto = get_ontology(path_owl + name_owl).load()
    return None


def initChemOntoToxWithPath(path_empty_chemontotox):
    global chemontotox
    chemontotox = get_ontology(path_empty_chemontotox).load()
    return None


### Config File

def initConfigFile(romedi, pcf):
    global cfg
    if pcf:
        config_file = "config" + "_" + str(pcf) + ".yml"
    else:
        config_file = "config.yml"
    with open(config_file, "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    # Load External ontologies
    global TIME_ONTO

    # TIME_ONTO=get_ontology(cfg["onto"]["local"]["time"]).load()
    # TIME_ONTO=get_ontology(cfg["onto"]["local"]["time"]).load()
    TIME_ONTO = get_ontology(cfg["onto"]["url"]["time"]).load()

    if romedi:
        global ROMEDI
        ROMEDI = get_ontology(cfg["onto"]["local"]["romedi"]).load()
    return None
