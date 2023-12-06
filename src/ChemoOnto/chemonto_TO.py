#from owlready2 import *

import isodate
import global_variables as gv
from utils import *
import custom_datatypes as cd
#from datetime import date
from datetime import *


"""
Procedures that instantiate Time ontology (TO) classes to represent time for both chemotherapy theoretical protocols and actual lines.
"""

### Theoretical PRC :

def instantiatesTheoreticalCycleInt(id_cycle_time, label_cycle_time, id_cure_time, label_cure_time, xsd_duration_cycle,
                                  chemonto_cycle_ind, chemonto_cure_ind):
    ## Time Ontology
    timeonto_cycletime_ind = gv.TIME_ONTO.ProperInterval(id_cycle_time)
    timeonto_cycletime_ind.label.append(label_cycle_time)
    xsd_duration_cycle = isodate.parse_duration(xsd_duration_cycle) # seulement pour que xsd_duration soit de type timedelta et que xsd:duration soit du bon type
    gv.TIME_ONTO.hasXSDDuration[timeonto_cycletime_ind].append(xsd_duration_cycle)
    timeonto_curetime_ind = gv.TIME_ONTO.ProperInterval(id_cure_time)
    timeonto_curetime_ind.label.append(label_cure_time)
    gv.TIME_ONTO.intervalDuring[timeonto_curetime_ind].append(timeonto_cycletime_ind)
    gv.TIME_ONTO.hasTime[chemonto_cycle_ind].append(timeonto_cycletime_ind)
    gv.TIME_ONTO.hasTime[chemonto_cure_ind].append(timeonto_curetime_ind)
    return timeonto_cycletime_ind, timeonto_curetime_ind


def intantiantesDaysofTheoreticalCycleInt(duration_cycle, PRC_KEY, timeonto_cycletime_ind):
    duration_cycle_int = int(duration_cycle) + 1
    dict_day_ind = {}
    for duration_cycle_counter in range(1, duration_cycle_int):
        id_day = "DAY_" + PRC_KEY + "_" + str(duration_cycle_counter)
        # 2022-10-05 : Instant (to agree more with followed lines)
        timeonto_day_cycle_ind = gv.TIME_ONTO.Instant(id_day)
        gv.TIME_ONTO.inside[timeonto_cycletime_ind].append(timeonto_day_cycle_ind)
        dict_day_ind[duration_cycle_counter] = timeonto_day_cycle_ind
        # before 2022-10-05:
        #timeonto_day_cycle_ind = gv.TIME_ONTO.ProperInterval(id_day) 
        #gv.TIME_ONTO.intervalDuring[timeonto_day_cycle_ind].append(timeonto_cycletime_ind)
        #dict_day_ind[duration_cycle_counter] = timeonto_day_cycle_ind
        #if duration_cycle_counter > 1:
        #    gv.TIME_ONTO.intervalMeets[dict_day_ind[duration_cycle_counter - 1]].append(timeonto_day_cycle_ind)
    return dict_day_ind


def linksDrugAdmToDay(jour_drug_adm, dict_day_ind,chemonto_drug_adm_ind, timeonto_curetime_ind):
    list_day_indices = returns_jouradm("O", jour_drug_adm)
    for indice in list_day_indices:
        day_ind = dict_day_ind[indice]
        gv.chemonto.hasDayDrugAdm[chemonto_drug_adm_ind].append(indice)
        gv.TIME_ONTO.hasTime[chemonto_drug_adm_ind].append(day_ind)
        # 2022-10-05:
        gv.TIME_ONTO.inside[timeonto_curetime_ind].append(day_ind)
        #gv.TIME_ONTO.intervalDuring[day_ind].append(timeonto_curetime_ind)
    return None


### Followed PRC :

## 2022-9-07 date datatype



def instantiatesStartInstAndInt(chemonto_ind, id_start, label_start, id_int, label_int, date_str):
    ## Time Ontology
    ### LINE int and inst
    #### int
    timeonto_int_ind = gv.TIME_ONTO.ProperInterval(id_int)
    timeonto_int_ind.label.append(label_int)
    chemonto_ind.hasTime.append(timeonto_int_ind)
    #### inst
    timeonto_start_ind = gv.TIME_ONTO.Instant(id_start)
    xsd_date = date.fromisoformat(date_str)
    timeonto_start_ind.inXSDDate.append(xsd_date) # pour avoir le bon type
    timeonto_start_ind.label.append(label_start)
    gv.TIME_ONTO.hasBeginning[timeonto_int_ind].append(timeonto_start_ind)
    return None




def instantiatesStopInst(timeonto_int_ind, id_stop, label_stop, date_str):

    timeonto_stop_ind = gv.TIME_ONTO.Instant(id_stop)
    xsd_date = date.fromisoformat(date_str)
    timeonto_stop_ind.inXSDDate.append(xsd_date)
    timeonto_stop_ind.label.append(label_stop)
    gv.TIME_ONTO.hasEnd[timeonto_int_ind].append(timeonto_stop_ind)
    return None




### 2022-10-05:


def instantiatesDayInst(id_day, label_day, date_str):

    timeonto_day_inst = gv.TIME_ONTO.Instant(id_day)
    xsd_date = date.fromisoformat(date_str)
    timeonto_day_inst.inXSDDate.append(xsd_date)
    timeonto_day_inst.label.append(label_day)
    return timeonto_day_inst



### 2022-10-03 :

def instantiatesDateTimeIntAndDesc2(timeonto_day_int, label_day_int, date_str):
    timeonto_day_int.label.append(label_day_int)
    xsd_dateTime = datetime.fromisoformat(date_str+"T00:00:00")
    timeonto_day_int.xsdDateTime.append(xsd_dateTime)
    return None
    
    #timeonto_day_int.inXSDDateTime.append(xsd_date)
    
    #gyear = date_str.split("-")[0]
    #gmonth = date_str.split("-")[1]
    #gday = date_str.split("-")[2]
    #id_date_day_descr = date_str.replace("-", "")
    #label_date_day_descr = date_str
    #if id_date_day_descr not in [c.name for c in gv.TIME_ONTO.DateTimeDescription.instances()]:
        #timeonto_date_desc = gv.TIME_ONTO.DateTimeDescription(id_date_day_descr)
        #instantiatesDateTimeDesc(timeonto_date_desc, gday, gmonth, gyear, label_date_day_descr)
    #else:
        #timeonto_date_desc = getattr(gv.chemonto, id_date_day_descr)
    #gv.TIME_ONTO.hasDateTimeDescription[timeonto_day_int].append(timeonto_date_desc)
    #return None


### Unused (before 2022-10-03):
### 2022-09-14 :
# either timeonto_day is an Instant, and you use the data poperty inXSDDate to define absolute date
# or it's a Date-Time interval; subclass of Interval, and you use oject property "has Date-Time description


# def instantiatesDayInst(id_day, label_day, date_str):

#     timeonto_day_inst = gv.TIME_ONTO.Instant(id_day)
#     xsd_date = date.fromisoformat(date_str)
#     timeonto_day_inst.inXSDDate.append(xsd_date)
#     timeonto_day_inst.label.append(label_day)
#     return timeonto_day_inst



### Unused (before 2022-09-14):

def instantiatesDateTimeIntAndDesc(timeonto_day_int, label_day_int, date_str):
    timeonto_day_int.label.append(label_day_int)
    xsd_date = date.fromisoformat(date_str)
    timeonto_day_int.inXSDDate.append(xsd_date)
    gyear = date_str.split("-")[0]
    gmonth = date_str.split("-")[1]
    gday = date_str.split("-")[2]
    id_date_day_descr = date_str.replace("-", "")
    label_date_day_descr = date_str
    if id_date_day_descr not in [c.name for c in gv.TIME_ONTO.DateTimeDescription.instances()]:
        timeonto_date_desc = gv.TIME_ONTO.DateTimeDescription(id_date_day_descr)
        instantiatesDateTimeDesc(timeonto_date_desc, gday, gmonth, gyear, label_date_day_descr)
    else:
        timeonto_date_desc = getattr(gv.chemonto, id_date_day_descr)
    gv.TIME_ONTO.hasDateTimeDescription[timeonto_day_int].append(timeonto_date_desc)
    return None


def instantiatesDateTimeDesc(timeonto_date_desc, gday, gmonth, gyear, label_date_day_descr):
    #gday=cd.GDay(gday)
    #gmonth=cd.GMonth(gmonth)
    #gyear=cd.GYear(gyear)  # ValueError: Cannot store literal '<custom_datatypes.GDay object at 0x7f3cc1c89a10>' of type '<class 'custom_datatypes.GDay'>'
    timeonto_date_desc.label.append(label_date_day_descr)
    timeonto_date_desc.day.append(gday)
    timeonto_date_desc.month.append(gmonth)
    timeonto_date_desc.year.append(gyear)
    return None


