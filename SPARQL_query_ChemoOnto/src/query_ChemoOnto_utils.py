import requests
import yaml
import urllib.parse
import re
import json
import sys
import time as t
from os.path import exists


def read_config_file(yml_file="config.yml"):
    with open(yml_file, "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    return cfg

def updateConfigFileWithQueryResFilename(key_filename, filename, yml_file):
    """
    key_filename : 
        - theo_filename 
        - foll_pats_filename
        - foll_lines_filename
        - foll_cycles_filename
        - foll_adms_filename
    """
    with open(yml_file) as f:
        doc = yaml.safe_load(f)

    doc['query_results'][key_filename] = filename

    with open(yml_file, 'w') as f:
        yaml.safe_dump(doc, f, default_flow_style=False)
    cfg = read_config_file(yml_file)
    return cfg


def percent_encode_query(query_file, encoded_query_file):
    with open(query_file, "r") as f:
        query = f.read()
    encoded_query=urllib.parse.quote(query)
    encoded_query="query="+encoded_query # DON'T FORGET "query="
    with open(encoded_query_file, "w") as f :
        f.write(encoded_query)
    return None


def query_chemonto(url, proxies, headers, input_enc_query_file, output_path, filename):
    with open(input_enc_query_file, 'rb') as f:
        data = f.read()
    res = requests.post(url=url,
                    data=data,
                    headers=headers,
                    proxies=proxies)
    if headers["Accept"] == "application/sparql-results+json" :
        file_ext = ".json"
    elif headers["Accept"] == "text/csv; charset=utf-8":
        file_ext = ".csv"
    else :
        file_ext = ".txt"
    output_file = output_path + filename + file_ext
    if res.status_code == 200 :
        with open(output_file, "w") as f:
            f.write(res.text)
    else :
        print("PBBB")
        print("res.status_code : ", res.status_code)
        with open(output_file, "w") as f:
            f.write(str(res.status_code))
    return None




def write_all_info_by_pat(query_file, PAT="http://chemontotox.owl/#1111111111"):
    with open(query_file, 'r') as f :
        query=f.read()
    new_query = re.sub(r'PAT=<(http://chemontotox.owl/#[0-9]{0,20})', "PAT=<"+PAT, query)
    with open(query_file, 'w+') as f :
        f.write(new_query)
    return None


def write_theo_query(PRCKEY, query_file):
    with open(query_file, 'r') as f :
        query=f.read()
    new_query = re.sub(r'PRCKEY=(-{0,1}[0-9]+)', "PRCKEY="+str(PRCKEY), query)
    with open(query_file, 'w+') as f :
        f.write(new_query)
    return None

def write_lines_of_pat_query(query_file, PAT="http://chemontotox.owl/#1111111111"):
    with open(query_file, 'r') as f :
        query=f.read()
    new_query = re.sub(r'PAT=<(http://chemontotox.owl/#[0-9]{0,20})', "PAT=<"+PAT, query)
    with open(query_file, 'w+') as f :
        f.write(new_query)
    return None

def write_cycles_of_line_query(query_file, LINE="http://chemonto.owl/#LINE_1111111111_2012-12-17_944"):
    with open(query_file, 'r') as f :
        query=f.read()
    new_query = re.sub(r'line=<(http://chemonto.owl/#LINE_[0-9]{1,20}_[0-9]{4}-[0-9]{2}-[0-9]{2}_([0-9]{1,5}|None))', "line=<"+LINE, query)
    with open(query_file, 'w+') as f :
        f.write(new_query)
    return None


def write_adms_of_cycle_query(query_file, CYCLE="http://chemonto.owl/#CYCLE_944_1111111111_2012-12-17_2"):
    with open(query_file, 'r') as f :
        query=f.read()
    new_query = re.sub(r'cycle=<(http://chemonto.owl/#CYCLE_([0-9]{1,5}|None)_[0-9]{0,20}_[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]+)', "cycle=<"+CYCLE, query)
    with open(query_file, 'w+') as f :
        f.write(new_query)
    return None


def write_toxs_in_cycle_query(query_file, CYCLE="http://chemonto.owl/#CYCLE_944_1111111111_2012-12-17_2"):
    #print("CYCLE", CYCLE)
    with open(query_file, 'r') as f :
        query=f.read()
    new_query = re.sub(r'cycle_id=<(http://chemonto.owl/#CYCLE_([0-9]{1,5}|None)_[0-9]{0,20}_[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]+)', "cycle_id=<"+CYCLE, query)
    #print("new_query: ", new_query)
    with open(query_file, 'w+') as f :
        f.write(new_query)
    return None

def write_meddra_cui_of_tox_query(query_file, tox_id = "http://ontotox.owl/#417_QSTQN43609__04.50_(43609)_Rash_cutané"):
    #print("\n\n tox_id :", tox_id )
    with open(query_file, 'r') as f :
        query=f.read()
    new_query = re.sub(r'tox_id=<(http://ontotox.owl/#.+)\>', "tox_id=<"+tox_id+">", query)
    #print("\n\n query : ", query)
    #print("\n\n new_query", new_query)
    with open(query_file, 'w+') as f :
        f.write(new_query)
    return None

    


def json_file_to_dict(json_name):
    f = open (json_name, "r")
    dict_res = json.loads(f.read())
    return dict_res



def from_query_to_dict_res_procedure(query_type, filter_variable, yml_file, results_file_format) :
    """
    query_type :
    - "pat"
    - "theo"
    - "lines"
    - "cycles"
    - "adms"
    - "tox_in_cycle"
    - "meddra_cui_of_tox"
    - "all_infos_by_pat"
    """
    
    message =  """
        Please choose between query_type :
            - "pat"
            - "theo"
            - "lines"
            - "cycles"
            - "adms"
            - "tox_in_cycle"
            - "meddra_cui_of_tox"
        """
    
    cfg = read_config_file(yml_file)
    
    
    if results_file_format == "json" :
        headers = cfg["request_params"]["headers_json"]
        output_path = cfg["query_results"]["json_foll"]
    else :
        headers = cfg["request_params"]["headers_csv"]
        output_path = cfg["query_results"]["csv_foll"]
        
    
    url = cfg["request_params"]["url"]
    proxies = cfg["request_params"]["proxies"]    
    input_enc_query_file = cfg["sparql"]["p_enc_adms_of_cycle_query"]
    
    ## Write a query depending on the query_type
    if query_type == "theo":
        output_path = cfg["query_results"]["json_theo"]
        query_file = cfg["sparql"]["theo_query"]
        encoded_query_file = cfg["sparql"]["p_encoded_theo_query"]
        write_theo_query(query_file = query_file, PRCKEY = filter_variable)
        filename = "theo_" + str(filter_variable.replace("http://chemonto.owl/#", ""))
        key_filename ="theo_filename"
    elif query_type == "pat":
        query_file = cfg["sparql"]["pats_of_chemonto_query"]
        encoded_query_file = cfg["sparql"]["p_enc_pats_of_chemonto_query"]
        #write_theo_query(query_file = query_file, PRCKEY = filter_ cvariable)
        filename = t.strftime("%Y%m%d%H%M%S") + "_pats_of_chemonto"
        key_filename ="foll_pats_filename"
    elif query_type == "lines":
        query_file = cfg["sparql"]["lines_of_pat_query"]
        encoded_query_file = cfg["sparql"]["p_enc_lines_of_pat_query"]
        write_lines_of_pat_query(query_file = query_file, PAT = filter_variable)
        filename = "lines_of_pat_" + str(filter_variable.replace("http://chemontotox.owl/#", ""))
        key_filename = "foll_lines_filename"
    elif query_type == "cycles":
        query_file = cfg["sparql"]["cycles_of_line_query"]
        encoded_query_file = cfg["sparql"]["p_enc_cycles_of_line_query"]
        write_cycles_of_line_query(query_file = query_file, LINE = filter_variable)
        filename = "cycles_of_line" + "_" + str(filter_variable.replace("http://chemonto.owl/#", ""))
        key_filename = "foll_cycles_filename"
    elif query_type == "adms":
        query_file = cfg["sparql"]["adms_of_cycle_query"]
        encoded_query_file = cfg["sparql"]["p_enc_adms_of_cycle_query"]
        write_adms_of_cycle_query(query_file = query_file, CYCLE = filter_variable)
        filename = "adms_of_cycle" + "_" + str(filter_variable.replace("http://chemonto.owl/#", ""))
        key_filename = "foll_adms_filename"
    elif query_type == "tox_in_cycle":
        query_file = cfg["sparql"]["tox_in_cycle_query"]
        encoded_query_file = cfg["sparql"]["p_encoded_tox_in_cycle_query"]
        write_toxs_in_cycle_query(query_file = query_file, CYCLE = filter_variable)
        filename = "tox_in_cycle" + "_" + str(filter_variable.replace("http://chemonto.owl/#", ""))
        key_filename = "tox_filename"
    elif query_type == "meddra_cui_of_tox":
        query_file = cfg["sparql"]["meddra_cui_of_tox_query"]
        encoded_query_file = cfg["sparql"]["p_encoded_meddra_cui_of_tox_query"]
        write_meddra_cui_of_tox_query(query_file = query_file, tox_id = filter_variable)
        filename = "meddra_cui_of_tox" + "_" + str(filter_variable.replace("http://ontotox.owl/#", "").split("_")[1])
        key_filename = "meddra_cui_filename"        
    
    
    ## VAL
    
    elif query_type == "all_infos_by_pat":
        query_file = cfg["sparql"]["all_infos_by_pat"]
        encoded_query_file = cfg["sparql"]["p_encoded_all_infos_by_pat"]
        write_lines_of_pat_query(query_file = query_file, PAT = filter_variable)
        filename = "all_infos_by_pat" + str(filter_variable.replace("http://chemontotox.owl/#", ""))
        key_filename = "all_infos_by_pat_filename"
    elif query_type == "all_infos":
        query_file = cfg["sparql"]["all_infos"]
        encoded_query_file = cfg["sparql"]["p_encoded_all_infos"]
        filename = "all_infos_by_pat"
        key_filename = "all_infos_by_pat_filename"
    
    else :
        print(message)
        sys.exit()
        
    ## Update config file
    cfg = updateConfigFileWithQueryResFilename(key_filename = key_filename, 
                                               filename = filename, 
                                               yml_file=yml_file)
    
    if query_type == "theo":
        filename = cfg["query_results"]["theo_filename"]
    elif query_type == "pat":
        filename = cfg["query_results"]["foll_pats_filename"]
    elif query_type == "lines":
        filename = cfg["query_results"]["foll_lines_filename"]
    elif query_type == "cycles":
        filename = cfg["query_results"]["foll_cycles_filename"]
    elif query_type == "adms":
        filename = cfg["query_results"]["foll_adms_filename"]
    elif query_type == "tox_in_cycle":
        filename = cfg["query_results"]["tox_filename"]
    elif query_type == "meddra_cui_of_tox":
        filename = cfg["query_results"]["meddra_cui_filename"]
    
    elif query_type == "all_infos_by_pat":
        filename = cfg["query_results"]["all_infos_by_pat_filename"]
    elif query_type == "all_infos":
        filename = cfg["query_results"]["all_infos_filename"]
    
    else :
        print(message)
        sys.exit()
        
    ## Encode query 
    percent_encode_query(query_file = query_file, encoded_query_file = encoded_query_file)
    
    ## Query chemOnto
    query_chemonto(url = url, proxies = proxies, headers = headers, input_enc_query_file = encoded_query_file, output_path = output_path, filename=filename)
    
    ## json file to dict
    if results_file_format == "json" :
        path_to_json_file = output_path + filename + ".json"
        res_dict = json_file_to_dict(path_to_json_file)

        if res_dict['results']['bindings'] == []:
            no_sparql_results(path_to_log_file=cfg["log_files"]["empty_sparql_res"],
                              query_type = query_type,
                              filter_variable = filter_variable, 
                              query_file = query_file)
            res_dict=None
    else :
        res_dict=None
    
    
    return res_dict


def no_sparql_results(path_to_log_file, query_type, filter_variable, query_file):
    with open(query_file, 'r') as file:
        query_data = file.read()

    file_exists = exists(path_to_log_file)
    if not file_exists:
        with open(path_to_log_file, 'w', newline="") as csvfile:
            fieldnames = ['query_type', 'filter_variable', 'query']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'query_type': query_type,
                             'filter_variable': filter_variable,
                             'query': query_data})
    else:
        with open(path_to_log_file, 'a', newline="") as csvfile:
            fieldnames = ['query_type', 'filter_variable', 'query']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'query_type': query_type,
                             'filter_variable': filter_variable,
                             'query': query_data})
    return None