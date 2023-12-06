import i2b2_utils as iu
import utils as u
import sys, os
import shutil
from os.path import exists
import pandas as pd


def usage(): print(
    """
    Take a list of patient num and a chosen prefix.
    Query i2B2 on chimio data of these patients, and put the results in data/query_result/prefix dir.
    
    
    
    --patientsListFile
    -PLF
    patient num list in a csv file
    
    --prefixConfFiles
    -PCF
    prefix
    
    """
)


def main(argv=None):
    if "-h" in argv or "--help" in argv:
        usage()
        sys.exit()

    try:
        plf = argv[argv.index("--patientsListFile") + 1]
    except ValueError:
        try:
            plf = argv[argv.index("-PLF") + 1]
        except ValueError:
            plf = "../query_results/TESTcohort.csv"

    try:
        pcf = argv[argv.index("--prefixConfFiles") + 1]
    except ValueError:
        try:
            pcf = argv[argv.index("-PCF") + 1]
        except ValueError:
            pcf = 1

    config_filename = "config_" + str(pcf) + ".yml"
    file_exists = exists(config_filename)
    if not file_exists:
        shutil.copyfile("config.yml", config_filename)

        u.modifyConfigFileWithPrefix(first_keyfield = "query_results",
                                   prefix = str(pcf),
                                   path_to_config = config_filename)
        # u.modifyConfigFileWithPrefix(first_keyfield="log_files",
        #                            prefix=str(pcf),
        #                            path_to_config=config_filename)
        u.modifyConfigFileWithPrefix(first_keyfield="sql_queries_i2b2",
                                     prefix=str(pcf),
                                     path_to_config=config_filename)

        u.modifyConfigFileWithPrefix(first_keyfield="log_files",
                                     prefix=str(pcf),
                                     path_to_config=config_filename)
        
        
        u.modifyConfigFileWithSuffix(first_keyfield = "onto", 
                                     second_keyfield = "local",
                                     third_keyfield = "chemontotox",
                                     suffix = str(pcf),
                                     path_to_config=config_filename)

        cfg = u.read_config_file(yml_file=config_filename)

        os.mkdir(cfg["query_results"]["dir_results"])
        #os.mkdir(cfg["log_files"])
        os.mkdir(cfg["sql_queries_i2b2"]["dir_queries"])
        os.mkdir(cfg["query_results"]["dir_ordered_pat_data"])
        os.mkdir(cfg["log_files"]["path_to_dir"])
        
        

        # copy log files :

        # shutil.copyfile("../sql_queries_i2b2/orderedCHIMIOPatientData.sql",
        #                 cfg["sql_queries_i2b2"]["ordered_pat_data"])
        
        shutil.copyfile("../sql_queries_i2b2/2022-12-01_orderedCHIMIOPatientData.sql",
                        cfg["sql_queries_i2b2"]["ordered_pat_data"])

        pat_to_chimio_path_dict = cfg["query_results"]["dict_pat_to_chimio_data_path"]
        open(pat_to_chimio_path_dict, "w") # create_pat_to_chimio_path_dict_yaml =

        log_files_dinamically_created = ["no_chimio_data", "yaml_errors", "attribute_error", "d2_before_d1", "data_always_None"]

        for log_file in cfg["log_files"]:
            print("cfg[log_files][log_file]", cfg["log_files"][log_file])
            if log_file != "path_to_dir" and log_file not in log_files_dinamically_created:
                with open(cfg["log_files"][log_file], "w") as file:# create_pat_to_chimio_path_dict_yaml =
                    if log_file == "info_process_dict":
                        file.write("{}")


        #shutil.copyfile("../log_files/info_process_dict.yaml", cfg["log_files"]["info_process_dict"])


    cfg = u.read_config_file(yml_file=config_filename)

    patients_list_file = pd.read_csv(plf, sep=";")
    patients_list = patients_list_file['PATIENT_NUM'].tolist()

    path_to_results_dir = cfg["query_results"]["dir_ordered_pat_data"]
    pat_to_chimio_path_dict = cfg["query_results"]["dict_pat_to_chimio_data_path"]

    db_config_dict = u.read_config_file(yml_file=cfg["DB_config"])

    path_to_query_file = cfg["sql_queries_i2b2"]["ordered_pat_data"]
    
    print("\n\n path_to_query_file :", path_to_query_file)

    log_chimiodata_query_results = cfg["log_files"]["check_chimiodata_query_results"]

    #bash_script_progress = cfg["bash_script_progress"]

    log_yaml_errors = cfg['log_files']['yaml_errors']

    path_to_no_chimiodata = cfg["log_files"]["no_chimio_data"]
    
    print("\n just before execute_queries \n")

    iu.execute_queries_and_save_results(pat_to_chimio_path_dict, patients_list, path_to_query_file, path_to_results_dir, db_config_dict, log_chimiodata_query_results, log_yaml_errors, path_to_no_chimiodata)



if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))