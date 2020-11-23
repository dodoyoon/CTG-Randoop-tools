import json, copy, sys
from json2html import *

filename = sys.argv[1]
inf = open(filename, "r")
file = inf.readlines()

final_dict = {}
l_cnt = 0
last_elem_cnt = 0
descriptions=[]
one_description={}
result_dict={}
loc_list=[]

is_exception = False
exception_list = []

for line in file:
    if line == '\n' or not line :
        continue

    line = line.strip()

    if line.split(' ', 1)[0] == 'at':
        one_description['exception'] = copy.deepcopy(exception_list)

        is_exception = False


    if line[0].isdigit() and 'test' in line:
        if loc_list:
            one_description['location'] = loc_list
            descriptions.append(copy.deepcopy(one_description))
            loc_list.clear()
            one_description.clear()
            exception_list.clear()
            one_description['id'] = line
        else:
            one_description['id'] = line

        is_exception = True

    # exception
    elif is_exception:
        exception_list.append(copy.deepcopy(line))

    # location
    elif line.split(' ', 1)[0] == 'at':
        loc_list.append(copy.deepcopy(line))

    # results
    elif line[0] == 'F':
        result_dict['word'] = line
        if last_elem_cnt == 0:
            one_description['location'] = loc_list

            descriptions.append(copy.deepcopy(one_description))
            last_elem_cnt = last_elem_cnt + 1

    elif line.split(' ', 1)[0] == 'Tests':
         result_dict['result'] = line

    else:
        continue

final_dict['descriptions'] = descriptions
final_dict['summary'] = result_dict



out_file_name = filename + '.json'
out_file = open(out_file_name, "w")
json.dump(final_dict, out_file, indent=4)
out_file.close()

