import sys, yaml, json


### utils fontions :


def save_drug_dict(path_json_dict, name_drug_dict, drug_dict):
    with open(path_json_dict + name_drug_dict, 'w') as f:
        json.dump(drug_dict, f,  ensure_ascii=False)
    return None


def setConfigFileTheo(name_owl, empty_name_owl):
    with open('config.yml') as f:
        doc = yaml.safe_load(f)

    doc['theoretical'] = name_owl
    doc['empty'] = empty_name_owl

    with open('config.yml', 'w') as f:
        yaml.safe_dump(doc, f, default_flow_style=False)
    return None


def boolOption(op):
    if op is not None:
        op = op.lower()
        if op == "" or op == "off":
            return False
        elif op == "on":
            return True
        else:
            print(
                "\n\n\n Please read the message below : \n For boolean options please choose between 'on' and 'off' parameters. \n")
            sys.exit()
    else:
        return False



def setConfigFileFollowed(name_owl):
    with open('config.yml') as f:
        doc = yaml.safe_load(f)

    doc['followed'] = name_owl

    with open('config.yml', 'w') as f:
        yaml.safe_dump(doc, f, default_flow_style=False)