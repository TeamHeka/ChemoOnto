from DB_modules.SQLexecution import i2b2_interaction
import re
import pandas as pd
import utils as u



def execute_query_and_save_results(path_to_query_file, path_to_results_file, db_config_dict):
    i2b2Interac = i2b2_interaction(db_config_dict)
    request = open(path_to_query_file, 'r+').read()
    i2b2_response = i2b2Interac.executeRequest(request)
    headers=[colname for colname in i2b2_response[0]]
    output_Res = open(path_to_results_file, 'w')
    output_Res.write(';'.join(att for att in headers) + "\n")
    # output_Res.write(';'.join(att for att in
    #                           ['PATIENT_NUM', 'DOCUMENT_DATE', 'ENCOUNTER_NUM', 'DOCUMENT_ORIGIN_CODE', 'VAL_NUMERIC',
    #                            'VAL_TEXT']))

    #list_new_patients = []

    for i2b2_response_line in i2b2_response:
        # print(i2b2_response_line)
        # i2b2_response_line['path_to_text'] = str(i2b2_response_line['patient_num'][0:4]) + "/" + str(i2b2_response_line['patient_num'][4:7]) + "/" + str(i2b2_response_line['patient_num'][7:10]) + str(i2b2_response_line['document_origin_code']) + ".txt"
        output_Res.write(';'.join([str(i2b2_response_line[key]) for key in i2b2_response_line]) + "\n")

        # str_patient_num = i2b2_response_line['patient_num']
        #
        # if str_patient_num not in list_existing_patients:
        #     list_new_patients.append(i2b2_response_line['patient_num'])

    output_Res.close()
    return None


### 2022-08-25 : list of patients
def execute_queries_and_save_results(pat_to_chimio_path_dict, patients_list, path_to_query_file, path_to_results_dir, db_config_dict, log_chimiodata_query_results, log_yaml_errors, path_to_no_chimiodata):
    #print("\n\n CALL i2b2Interac  \n\n")
    i2b2Interac = i2b2_interaction(db_config_dict)
    cursor_i2b2 = i2b2Interac.connect_i2b2()
    for pat_num in patients_list:
        pat_num = str(pat_num)
        path_to_results_file = path_to_results_dir + pat_num + ".csv"
        pat_to_chimio_path_dict = pat_to_chimio_path_dict

        patnum_in_yaml, parserError, scannerError = u.addPatNumToYamlFile(yml_key=pat_num,
                                                                          yml_value=path_to_results_file,
                                                                          yml_file=pat_to_chimio_path_dict)

        if not patnum_in_yaml:
            #print("Querying i2b2 on " + pat_num)

            if not parserError and not scannerError:
                modify_CHIMIO_patient_query(pat_num=pat_num,
                                            path_to_query_file=path_to_query_file)


                request = open(path_to_query_file, 'r+').read()
                
                #print("\n\n\n-------------------------  request: -------------------- \n\n\n", request)
                #print("\n\n\n--------------------------------------------- \n\n\n")
                
                i2b2_response = executeRequest(request, cursor_i2b2)
                if i2b2_response != [] :
                    headers = [colname for colname in i2b2_response[0]]
                    output_Res = open(path_to_results_file, 'w')
                    output_Res.write(';'.join(att for att in headers) + "\n")

                    for i2b2_response_line in i2b2_response:
                        output_Res.write(';'.join([str(i2b2_response_line[key]) for key in i2b2_response_line]) + "\n")

                    output_Res.close()

                    check_chimiodata_query_results(path_to_log_file=log_chimiodata_query_results,
                                               path_to_chimiodata_query_results=path_to_results_file,
                                               patnum=pat_num)
                else :
                    u.addsPatNumToNoChimioData(path_to_log_file = path_to_no_chimiodata,
                                             patnum = pat_num)


                    # with open(bash_script_progress + pat_num + ".txt", "w") as f:
                    #                 f.write('false')
                    #                 f.close()

            elif parserError:
                u.addsPatNumToErrorFiles(path_to_log_file=log_yaml_errors,
                                         patnum=pat_num,
                                         function_name="addPatNumToYamlFile",
                                         yaml_error_type="parserError")
                # with open(bash_script_progress + pat_num + ".txt", "w") as f:
                #     f.write('true')

            else:
                u.addsPatNumToErrorFiles(path_to_log_file=log_yaml_errors,
                                         patnum=pat_num,
                                         function_name="addPatNumToYamlFile",
                                         yaml_error_type="scannerError")

                # with open(bash_script_progress + pat_num + ".txt", "w") as f:
                #     f.write('true')
        else:
            print(pat_num + " already done.")
            # with open(bash_script_progress + pat_num + ".txt", "w") as f:
            #     f.write('true')

    cursor_i2b2.close()

    return None



## 2022-08-25 :
def executeRequest(request_i2b2, cur):
    """
    2022-08-25 modifications : not connect to i2b2 each time you query it : put cursor in params
    :param request_i2b2:
    :return:
    """
    # return a dictionary :
    # dic[concept1] = [(key1, value11, ...), (key2, value21, ...), ...]
    res = []
    cur.execute(request_i2b2.encode('utf-8'))
    field_names = [i[0] for i in cur.description]
    for row in cur:
        dic_resp = {}
        for i in range(0, len(field_names)):
            #dic_resp[field_names[i].lower()]=str(row[i])
            dic_resp[field_names[i]]=str(row[i])
        res.append(dic_resp)
    #cur.close() il faut l'enlever !!! sinon le cursor nexiste plus
    return res



def modify_CHIMIO_patient_query(pat_num, path_to_query_file):
    with open(path_to_query_file, 'r') as sql_file:
        query=sql_file.read()
    new_query = re.sub(r'PATIENT_NUM = [0-9]{10}', "PATIENT_NUM = " + str(pat_num), query)
    with open(path_to_query_file, 'w') as sql_file:
        sql_file.write(new_query)
    return None

def check_chimiodata_query_results(path_to_log_file, path_to_chimiodata_query_results, patnum):
    df_chimiodata = pd.read_csv(path_to_chimiodata_query_results, header = 0, sep = ";")
    if str(df_chimiodata['PATIENT_NUM'].values[0]) != str(patnum):
        with open(path_to_log_file, "a") as logfile:
            logfile.write("\n")
            logfile.write("Problem with query of patient : "+ patnum + " . ")
            logfile.write("Chimio data concerns another patient. (PATNUM " + str(df_chimiodata['PATIENT_NUM'].values[0]) + ")")
    return None







# def execute_queries_and_save_results(pat_to_chimio_path_dict, patients_list, path_to_query_file, path_to_results_file, db_config_dict, log_chimiodata_query_results, bash_script_progress, log_yaml_errors):
#     i2b2Interac = i2b2_interaction(db_config_dict)
#     for pat_num in patients_list:
#         path_to_results_file = path_to_results_file + str(pat_num) + ".csv"
#         pat_to_chimio_path_dict = pat_to_chimio_path_dict
#
#         patnum_in_yaml, parserError, scannerError = u.addPatNumToYamlFile(yml_key=pat_num,
#                                                                           yml_value=path_to_results_file,
#                                                                           yml_file=pat_to_chimio_path_dict)
#
#         if not patnum_in_yaml:
#             print("Querying i2b2 on " + pat_num)
#
#             if not parserError and not scannerError:
#                 modify_CHIMIO_patient_query(pat_num=pat_num,
#                                             path_to_query_file=path_to_query_file)
#
#                 i2b2Interac = i2b2_interaction(db_config_dict)
#
#                 request = open(path_to_query_file, 'r+').read()
#                 i2b2_response = i2b2Interac.executeRequest(request)
#                 headers = [colname for colname in i2b2_response[0]]
#                 output_Res = open(path_to_results_file, 'w')
#                 output_Res.write(';'.join(att for att in headers) + "\n")
#
#                 for i2b2_response_line in i2b2_response:
#                     output_Res.write(';'.join([str(i2b2_response_line[key]) for key in i2b2_response_line]) + "\n")
#
#                 output_Res.close()
#
#                 check_chimiodata_query_results(path_to_log_file=log_chimiodata_query_results,
#                                            path_to_chimiodata_query_results=path_to_results_file,
#                                            patnum=pat_num)
#
#                 with open(bash_script_progress + str(pat_num) + ".txt", "w") as f:
#                                 f.write('false')
#                                 f.close()
#
#             elif parserError:
#                 u.addsPatNumToErrorFiles(path_to_log_file=log_yaml_errors,
#                                          patnum=pat_num,
#                                          function_name="addPatNumToYamlFile",
#                                          yaml_error_type="parserError")
#                 with open(bash_script_progress + str(pat_num) + ".txt", "w") as f:
#                     f.write('true')
#
#             else:
#                 u.addsPatNumToErrorFiles(path_to_log_file=log_yaml_errors,
#                                          patnum=pat_num,
#                                          function_name="addPatNumToYamlFile",
#                                          yaml_error_type="scannerError")
#
#                 with open(bash_script_progress + str(pat_num) + ".txt", "w") as f:
#                     f.write('true')
#         else:
#             print(str(pat_num) + " already done.")
#             with open(bash_script_progress + str(pat_num) + ".txt", "w") as f:
#                 f.write('true')
#
#     return None
