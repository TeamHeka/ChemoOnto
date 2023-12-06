from owlready2 import *
import datetime as datetime
import isodate
import custom_datatypes as cd
import global_variables as gv



"""
Definition of ChemoOnto structure (classes and properties)
"""

### ChemoOnto structure and instantiation

def creatsChemOntoStruct(path_owl, name_owl):
    with gv.chemonto:

        # 1 Classe definitions

        class Protocol(Thing): pass
        class Cycle(Thing): pass
        class TheoCycle(Thing): pass
        class Cure(Thing): pass
        class TheoCure(Thing): pass
        class DrugAdministration(Thing): pass
        class TheoDrugAdministration(Thing): pass
        class Drug(Thing): pass
        #class RxCUI(Thing): pass
        class AntiCancer(Drug): pass
        class Solvant(Drug): pass
        class AntiADE(Drug): pass
        # 2022-10-06 :
        #class Patient(Thing): pass
        class Line(Thing): pass
        #class CancerType(Thing): pass

        AllDisjoint([Protocol, Cycle, TheoCycle, Cure, TheoCure, DrugAdministration, TheoDrugAdministration, Drug, Line])


        # 2 Object Properties


        ## Protocol hasCycle TheoCycle -> could be removed
        ### Only theo
        class hasCycle(Protocol >> TheoCycle, FunctionalProperty): pass
        class cycleOf(TheoCycle >> Protocol, FunctionalProperty):
            inverse = hasCycle


        ## hasCure
        ### Followed
        class hasCure(Cycle >> Cure, FunctionalProperty): pass
        class cureOf(Cure >> Cycle, FunctionalProperty):
            inverse = hasCure
        ## Theo
        class hasCure(TheoCycle  >> TheoCure, FunctionalProperty): pass
        class cureOf(TheoCure >> TheoCycle, FunctionalProperty):
            inverse = hasCure

        ## hasAdministration
        ### Followed
        class hasAdministration(Cycle >> DrugAdministration): pass
        #class isAdministratedIn(DrugAdministration >> Cycle, FunctionalProperty):
            #inverse = hasAdministration
        class isAdministratedIn(DrugAdministration >> Cycle, FunctionalProperty): pass
        ### Theo
        class hasAdministration(TheoCycle >> TheoDrugAdministration): pass
        #class isAdministratedIn(DrugAdministration >> Cycle, FunctionalProperty):
            #inverse = hasAdministration
        class isAdministratedIn(TheoDrugAdministration >> TheoCycle, FunctionalProperty): pass


        ## hasDrug
        ### Followed
        class hasDrug(DrugAdministration >> Drug, FunctionalProperty): pass
        class isDrugOf(Drug >> DrugAdministration): pass
            #inverse = hasDrug
        class hasDrug(TheoDrugAdministration >> Drug, FunctionalProperty): pass
        class isDrugOf(Drug >> TheoDrugAdministration): pass
            #inverse = hasDrug

        ## realisationOf to link both parts
        class realisationOf(Cycle >> TheoCycle, FunctionalProperty): pass # Cycle >> TheoCycle (realised cycled is a realisation of theoretical cycle)
        #class isRealisedIn(Cycle >> Cycle): # TheoCycle >> Cycle
            #inverse = realisationOf
        class isRealisedIn(TheoCycle >> Cycle): pass # TheoCycle >> Cycle


        ##isComposedOfCycle
        ### Only followed
        class isComposedOfCycle(Line >> Cycle): pass
        #class cycleOfLine(Cycle >> Line, FunctionalProperty):
            #inverse = isComposedOfCycle
        class cycleOfLine(Cycle >> Line, FunctionalProperty): pass


        ##followedCycle
        ### Only followed
        class followedCycle(gv.chemontotox.Patient >> Cycle): pass
        #class cycleIsFollowedBy(Cycle >> Patient, FunctionalProperty):
            #inverse = followedCycle
        class cycleIsFollowedBy(Cycle >> gv.chemontotox.Patient, FunctionalProperty): pass


        ##followedLine
        ### Only followed
        class followedLine(gv.chemontotox.Patient >> Line): pass
        #class lineIsFollowedBy(Line >> Patient, FunctionalProperty):
            #inverse = followedLine
        class lineIsFollowedBy(Line >> gv.chemontotox.Patient, FunctionalProperty): pass




        #class isTreatedFor(Patient >> CancerType): pass
        #class concernsPatient(CancerType >> Patient, FunctionalProperty):
            #inverse = isTreatedFor

        # 3 Data Properties

        ## Protocol
        ### Only theo
        class hasName(Protocol >> str, FunctionalProperty): pass # TODO: USE EXISTING DATAPROPERTY
        #class hasCommentProtocol(Protocol >> str, FunctionalProperty): pass
        # class hasType(Protocol >> str, FunctionalProperty): pass
        #class hasSupervision(Protocol >> str, FunctionalProperty): pass
        #class hasOtherCommentProtocol(Protocol >> str, FunctionalProperty): pass
        #class hasNbCycleDef(Protocol >> str, FunctionalProperty): pass
        #class hasUTMAJPR(Protocol >> str, FunctionalProperty): pass
        #class hasCost(Protocol >> float, FunctionalProperty): pass
        #class hasMaxCycle(Protocol >> str, FunctionalProperty): pass

        ## Cycle
        ### Followed
        class hasCycleDuration(Cycle >> int, FunctionalProperty): pass
        class hasCycleNum(Cycle >> int, FunctionalProperty): pass
        class hasCyclePRCkey(Cycle >> int, FunctionalProperty): pass
        ### Theo
        class hasCycleDuration(TheoCycle>> int, FunctionalProperty): pass
        class hasCycleNum(TheoCycle>> int, FunctionalProperty): pass
        class hasCyclePRCkey(TheoCycle>> int, FunctionalProperty): pass

        ## Cure
        ### Followed
        class hasCureDuration(Cure >> str, FunctionalProperty): pass
        ### Theo
        class hasCureDuration(TheoCure >> str, FunctionalProperty): pass

        ## Line
        ### Only followed
        class hasProtocolName(Line >> str, FunctionalProperty) : pass
        class hasC1D1Date(Line >> str, FunctionalProperty) : pass
        class hasCNDNDate(Line >> str, FunctionalProperty): pass
        class hasLinePRCkey(Line >> int, FunctionalProperty): pass

        ## Drug
        class hasDrugName(Drug >> str, FunctionalProperty): pass
        #class hasDrugMolecule(Drug >> str, FunctionalProperty): pass


        ## DrugAdministration
        ### Followed
        class hasDose(DrugAdministration >> float, FunctionalProperty): pass  # both 2022-12-12
        class hasUnitSTR(DrugAdministration >> str, FunctionalProperty): pass  # both 2022-12-12
        # class hasUnitCode(DrugAdministration >> str, FunctionalProperty): pass  # theoretical
         # theoretical
        class hasDayDrugAdm(DrugAdministration >> int): pass  # both
        # class hasDayDrugAdm(DrugAdministration >> int, FunctionalProper): pass # both
        class isBolus(DrugAdministration >> bool, FunctionalProperty): pass  # both
        class hasDoseNorm(DrugAdministration >> float, FunctionalProperty): pass  # followed
        class hasCancerLocation(DrugAdministration >> str, FunctionalProperty): pass  # followed
        class hasReductionMotif(DrugAdministration >> str, FunctionalProperty): pass  # followed
        # 2022-12-12 :
        class hasPatBS(DrugAdministration >> float, FunctionalProperty): pass  # followed
        class hasPatWeight(DrugAdministration >> float, FunctionalProperty): pass  # followed
        # 2022-12-13
        class hasDurationInHour(DrugAdministration >> int, FunctionalProperty): pass  # both
        class hasDurationInMin(DrugAdministration >> int, FunctionalProperty): pass  # both
        # 2022-12-15
        class hasMissingValues(DrugAdministration >> str): pass  # followed

        ## Theo
        class hasDose(TheoDrugAdministration >> float, FunctionalProperty): pass
        class hasUnitSTR(TheoDrugAdministration >> str, FunctionalProperty): pass  # both 2022-12-12
        class hasUnitCode(TheoDrugAdministration >> int, FunctionalProperty): pass
        class hasDayDrugAdm(TheoDrugAdministration >> int): pass# both
        class hasDayDrugAdm(TheoDrugAdministration >> int): pass # both
        class isBolus(TheoDrugAdministration >> bool, FunctionalProperty): pass  # both
        class hasDurationInHour(TheoDrugAdministration >> int, FunctionalProperty): pass  # both
        class hasDurationInMin(TheoDrugAdministration >> int, FunctionalProperty): pass  # both

        ## DrugAdministration
        # class hasDose(DrugAdministration >> float, FunctionalProperty): pass
        # class hasDosePrescr(DrugAdministration >> float, FunctionalProperty): pass
        # class hasUnitSTR(DrugAdministration >> str, FunctionalProperty): pass
        # class hasCodeInjection(DrugAdministration >> str, FunctionalProperty): pass
        # class hasDurationAdm(DrugAdministration >> int, FunctionalProperty): pass
        # class hasDurationAdmin(DrugAdministration >> int, FunctionalProperty): pass
        # #class hasCommentDrugAdm(DrugAdministration >> str, FunctionalProperty): pass
        # class hasDayDrugAdm(DrugAdministration >> int): pass # Reste str pour le moment
        # class hasHourDrugAdm(DrugAdministration >> str, FunctionalProperty): pass
        # class hasReduction(DrugAdministration >> str, FunctionalProperty): pass
        # class hasReductionMotif(DrugAdministration >> str, FunctionalProperty): pass
        # class isBolus(DrugAdministration >> bool, FunctionalProperty): pass
        # class hasCancerLocalisation(DrugAdministration >> str, FunctionalProperty): pass
        # class hasPatWeight(DrugAdministration >> float, FunctionalProperty): pass
        # class hasPatHeight(DrugAdministration >> float, FunctionalProperty): pass
        # class hasBodySurf(DrugAdministration >> float, FunctionalProperty): pass
        # class hasBoydBodySurf(DrugAdministration >> float, FunctionalProperty): pass
        # class hasUnitCode(DrugAdministration >> int, FunctionalProperty): pass






        #set_datatype_iri(datatype=date.day, iri="https://www.w3.org/2001/XMLSchema#GDay")
        #set_datatype_iri(datatype=date., iri="https://www.w3.org/2001/XMLSchema#GDay")

    ## Time datatypes

    ### GDay
    declare_datatype(datatype=cd.GDay,
                     iri="http://www.w3.org/2001/XMLSchema#GDay",
                     parser=cd.gday_parser,
                     unparser=cd.gday_unparser)

    #define_datatype_in_ontology(GDay,"http://www.w3.org/2001/XMLSchema#GDay", gv.chemonto)

    ### GMonth
    declare_datatype(datatype=cd.GMonth,
                     iri="http://www.w3.org/2001/XMLSchema#GMonth",
                     parser= cd.gmonth_parser,
                     unparser= cd.gmonth_unparser)

    #define_datatype_in_ontology(GMonth, "http://www.w3.org/2001/XMLSchema#GMonth", gv.chemonto)

    ### GYear
    declare_datatype(datatype=cd.GYear,
                     iri="http://www.w3.org/2001/XMLSchema#GYear",
                     parser=cd.gyear_parser,
                     unparser=cd.gyear_unparser)

    #define_datatype_in_ontology(GYear,"http://www.w3.org/2001/XMLSchema#GYear",gv.chemonto)

    # ### date
    # set_datatype_iri(datetime.date, "http://www.w3.org/2001/XMLSchema#date")

    # ### duration
    declare_datatype(datatype=datetime.timedelta,
                     iri="http://www.w3.org/2001/XMLSchema#duration",
                     parser=cd.duration_parser,
                     unparser=cd.duration_unparser)
    # sqlite3.IntegrityError: UNIQUE constraint failed: resources.iri

    # set_datatype_iri(datatype=Duration,
    #                  iri="http://www.w3.org/2001/XMLSchema#duration")

    # define_datatype_in_ontology(datetime.timedelta, "http://www.w3.org/2001/XMLSchema#duration", gv.chemonto)

    gv.chemonto.save(path_owl + name_owl)

    return None


def importTO():
    gv.chemonto.imported_ontologies.append(gv.TIME_ONTO)
    return None



def addsChemOntoToRomediProperties(path_owl, name_owl):

    with gv.chemonto:

        #import Romedi #---> NON

        class isRelatedToRomIN(gv.chemonto.Drug >> gv.ROMEDI.IN, FunctionalProperty): pass
        #class isRelatedToChemDrugIN(gv.ROMEDI.IN >> gv.chemonto.Drug):
        #    inverse = isRelatedToRomIN

        class isRelatedToRomBNdosage(gv.chemonto.Drug >> gv.ROMEDI.BNdosage, FunctionalProperty): pass
        #class isRelatedToChemDrugBNdosage(gv.ROMEDI.BNdosage >> gv.chemonto.Drug):
        #    inverse = isRelatedToRomBNdosage

        class isRelatedToRomBN(gv.chemonto.Drug >> gv.ROMEDI.BN, FunctionalProperty): pass
        #class isRelatedToChemDrugBN(gv.ROMEDI.IN >> gv.chemonto.Drug):
        #    inverse = isRelatedToRomBN

        #class BNdosageHasIN(gv.ROMEDI.BNdosage >> gv.ROMEDI.IN): pass

        #class BNHasIN(gv.ROMEDI.BN >> gv.ROMEDI.IN): pass

    gv.chemonto.save(path_owl + name_owl)
    return None



### 2022-09-30 DRAFT

# ontotox=get_ontology("OntoTox_qst.owl").load()
# chemonto=get_ontology("chemonto2_equivalent_to.owl").load()

# pat_list_chem2 = list(chemonto.Patient.instances())
# pat_list_ontotox= list(ontotox.Patient.instances())
# pat_list_tox_names = [ind.name for ind in pat_list_ontotox]
# pat_list_chem_names = [ind.name for ind in pat_list_chem2]


# for pat_ind in pat_list_ontotox :
#     if pat_ind.name in pat_list_chem_names:
#         print("Yes")
#         pat_name = pat_ind.name
#         print(pat_name)
#         chemonto_ind = getattr(chemonto, pat_name)
#         print(chemonto_ind)
#         pat_ind.equivalent_to.append(chemonto_ind)


# for pat_ind in pat_list_ontotox :
#     if pat_ind.name in pat_list_chem_names:
#         print(pat_ind.equivalent_to)
        
# for pat_ind in pat_list_chem2 :
#     if pat_ind.name in pat_list_tox_names:
#         print("Yes")
#         pat_name = pat_ind.name
#         print(pat_name)
#         ontotox_ind = getattr(ontotox_qst, pat_name)
#         pat_ind.equivalent_to.append(ontotox_ind)
        
        
# for pat_ind in pat_list_chem2 :
#     if pat_ind.name in pat_list_tox_names:
#         print("Yes")
#         pat_name = pat_ind.name
#         print(pat_name)
#         ontotox_ind = getattr(ontotox_qst, pat_name)
#         pat_ind.equivalent_to.append(ontotox_ind)
        
        
