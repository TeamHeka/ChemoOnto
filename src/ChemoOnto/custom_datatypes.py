from owlready2 import *
import isodate
# https://owlready2.readthedocs.io/en/latest/datatype.html

## s : string
## x : datatype

class GDay(object):
    def __init__(self, value):
        self.value = value

def gday_parser(s):
    return GDay(int(s))

def gday_unparser(x):
    return(str(x.value))

#declare_datatype(GDay, "http://www.w3.org/2001/XMLSchema#GDay", parser, unparser)
#define_datatype_in_ontology(GDay, "http://www.w3.org/2001/XMLSchema#GDay", onto)

class GMonth(object):
    def __init__(self, value):
        self.value = value

def gmonth_parser(s):
    return GMonth(int(s))

def gmonth_unparser(x):
    return(str(x.value))

#declare_datatype(GMonth, "http://www.w3.org/2001/XMLSchema#GMonth", parser, unparser)
#define_datatype_in_ontology(GMonth, "http://www.w3.org/2001/XMLSchema#GMonth", onto)

class GYear(object):
    def __init__(self, value):
        self.value = value

def gyear_parser(s):
    return GYear(int(s))

def gyear_unparser(x):
    return(str(x.value))

#declare_datatype(GYear, "http://www.w3.org/2001/XMLSchema#GYear", parser, unparser)
#define_datatype_in_ontology(GYear, "http://www.w3.org/2001/XMLSchema#GYear", onto)


# class Duration(object):
#     def __init__(self, value):
#         self.value = value
#
# def parser(s):
#     """
#     :param s: int > timedelta
#     :return: Duration
#     """
#     duration_xsd=isodate.duration_isoformat(s)
#     return Duration(duration_xsd)
#
# def unparser(x):
#     return(str(x.value))
#
# declare_datatype(GYear, "http://www.w3.org/2001/XMLSchema#GYear", parser, unparser)
# define_datatype_in_ontology(GYear, "http://www.w3.org/2001/XMLSchema#GYear", onto)


# >>> import isodate
# >>> isodate.parse_duration("P14D")
# datetime.timedelta(days=14)
# >>> totot=isodate.parse_duration("P14D")
# >>> type(totot)
# <class 'datetime.timedelta'>
# >>> int(totot)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# TypeError: int() argument must be a string, a bytes-like object or a number, not 'datetime.timedelta'
# >>> totot.days
# 14
# >>> isodate.duration_isoformat(totot.days)
# 'P%P'
# >>> isodate.duration_isoformat(totot)
# 'P14D'
# >>> totot
# datetime.timedelta(days=14)

## https://codesuche.com/python-examples/isodate.parse_duration/
# def serialize_duration(attr, **kwargs):
#     """Serialize TimeDelta object into ISO-8601 formatted string.
#
#     :param TimeDelta attr: Object to be serialized.
#     :rtype: str
#     """
#     ## Renvoie un str donc correspond à unparser
#     if isinstance(attr, str):
#         attr = isodate.parse_duration(attr)
#     return isodate.duration_isoformat(attr)
#
#
# def deserialize_duration(attr):
#     """Deserialize ISO-8601 formatted string into TimeDelta object.
#
#     :param str attr: response string to be deserialized.
#     :rtype: TimeDelta
#     :raises: DeserializationError if string format invalid.
#     """
#     ## Renvoie un timedelta donc correspond à un parser
#     try:
#         duration = isodate.parse_duration(attr)
#     except(ValueError, OverflowError, AttributeError) as err:
#         msg = "Cannot deserialize duration object."
#         #raise_with_traceback(DeserializationError, msg, err)
#     else:
#         return duration


# class Duration(datetime.timedelta):
#     def __init__(self, value):
#         self.value = value

# def duration_parser(s):
#     return Duration(isodate.parse_duration(s))

def duration_parser(s):
    return isodate.parse_duration(s)

def duration_unparser(x):
    return isodate.duration_isoformat(x)


#declare_datatype(datatype=datetime.timedelta, "http://www.w3.org/2001/XMLSchema#duration", parser=duration_parser, unparser=duration_unparser)

#declare_datatype(datatype=datetime.timedelta, "http://www.w3.org/2001/XMLSchema#GYear", parser=, unparser=)