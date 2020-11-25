import json, copy, sys, subprocess
from json2html import *

''' Helping Methods '''
with open(sys.argv[1]) as f:
    data = json.load(f)

with open(sys.argv[2]) as f:
    data2 = json.load(f)

def remove_line_info(locs):
    if type(locs) == list:
        for i in range(len(locs)):
            loc = locs[i].rsplit(":", 1)[0] + ")"
            locs[i] = loc
    elif type(locs) == str:
        locs = locs.rsplit(":", 1)[0] + ")"

    return locs

def remove_description(exception):
    if exception.find(":"):
        exception = exception.split(":", 1)
        return exception[0]
    else:
        return exception

def check_topmost_stack(loc1, loc2):
    method1 = loc1.split(" ", 1)[1].rsplit("(")[0]
    line1 = loc1.split(":")[1].split(")")[0]
    method2 = loc2.split(" ", 1)[1].rsplit("(")[0]
    line2 = loc2.split(":")[1].split(")")[0]

    dic1 = {'line': line1, 'method': method1}
    dic2 = {'line': line2, 'method': method2}

    # print("methods: ", method1, method2)
    # print("list: ", changed_method_list)

    if method1 == method2:
        for method in changed_method_list:
            if method1 in method:
                print("methods: ", method1, method2)
                print("list: ", changed_method_list)

    else:
        return False
    
''' Heuristics '''
# exception type(+description), full stack, + line number
def heuristic1(case):
    equal = False
    for i in data['descriptions']:
        if(i['exception']==case['exception']):
            loc1 = i['location']
            loc2 = case['location']
            if loc1 == loc2:
                equal = True
                break

    return equal

# exception type(+description), top-most, + line number
def heuristic2(case):
    equal = False
    for i in data['descriptions']:
        if(i['exception']==case['exception']):
            loc1 = i['location'][0]
            loc2 = case['location'][0]

            # if check_topmost_stack(loc1, loc2, changed_method_list):
            #     equal = True
            # else:
            #     break

            if loc1 == loc2:
                equal = True
                break

    return equal

# exception type(+description), full stack, - line number
def heuristic3(case):
    equal = False
    for i in data['descriptions']:
        if(i['exception']==case['exception']):
            loc1 = remove_line_info(i['location'])
            loc2 = remove_line_info(case['location'])

            if loc1 == loc2:
                equal = True
                break

    return equal


# exception type(+description), top-most, -line number
def heuristic4(case):
    equal = False
    for i in data['descriptions']:
        if(i['exception']==case['exception']):
            loc1 = remove_line_info(i['location'][0])
            loc2 = remove_line_info(case['location'][0])

            if loc1 == loc2:
                equal = True
                break

    return equal


# exception type(+description), no stack
def heuristic5(case):
    equal = False
    for i in data['descriptions']:
        if(i['exception']==case['exception']):
            equal = True

    return equal


# exception type(-description), full stack, + line number
def heuristic6(case):
    equal = False
    for i in data['descriptions']:
        exception1 = remove_description(i['exception'][0])
        exception2 = remove_description(case['exception'][0])
        if(exception1 == exception2):
            loc1 = i['location']
            loc2 = case['location']
            if loc1 == loc2:
                equal = True
                break

    return equal


# exception type(-description), top-most, + line number
def heuristic7(case):
    equal = False
    for i in data['descriptions']:
        exception1 = remove_description(i['exception'][0])
        exception2 = remove_description(case['exception'][0])
        if(exception1 == exception2):
            loc1 = i['location'][0]
            loc2 = case['location'][0]

            if loc1 == loc2:
                equal = True
                break

    return equal


# exception type(-description), full stack, - line number
def heuristic8(case):
    equal = False
    for i in data['descriptions']:
        exception1 = remove_description(i['exception'][0])
        exception2 = remove_description(case['exception'][0])
        if(exception1 == exception2):
            loc1 = remove_line_info(i['location'])
            loc2 = remove_line_info(case['location'])

            if loc1 == loc2:
                equal = True
                break

    return equal


# exception type(-description), top-most, -line number
def heuristic9(case):
    equal = False
    for i in data['descriptions']:
        exception1 = remove_description(i['exception'][0])
        exception2 = remove_description(case['exception'][0])
        if(exception1 == exception2):
            loc1 = remove_line_info(i['location'][0])
            loc2 = remove_line_info(case['location'][0])

            if loc1 == loc2:
                equal = True
                break

    return equal


# exception type(-description), no stack
def heuristic10(case):
    equal = False
    for i in data['descriptions']:
        exception1 = remove_description(i['exception'][0])
        exception2 = remove_description(case['exception'][0])
        if(exception1 == exception2):
            equal = True

    return equal
    

'''
Argument explaination
python3 filter_result.py arg1 arg2 arg3 arg4 arg5 arg6 arg7
arg1: prev version json file(correct)
arg2: current version json file(buggy)
arg3: heuristic number(1~10)
arg4: prev commit hash(correct)
arg5: current commit hash(buggy)
arg6: path to source code directory
arg7: gerrit server address
arg8: number of result that will be shown(optional)
'''

def init_git_diff():
    buggy_hash = sys.argv[5]
    correct_hash = sys.argv[4]
    target_path = sys.argv[6] # source code directory
    diff_command = subprocess.Popen(["git", "diff", buggy_hash, correct_hash, target_path], stdout=subprocess.PIPE)

    lines, err = diff_command.communicate()
    lines = lines.decode('utf-8')
    diff = lines.split('\n')

    print("diff: ", diff)
    return

    result = []
    diff_dic = dict() # @@로 시작하는 부분
    block_dic = dict()
    block = []

    prev_cnt = 0
    current_cnt = 0
    for line in diff:
        if 'diff' in line:
            if block_dic:
                block_dic['prev_line_cnt'] = prev_cnt
                block_dic['current_line_cnt'] = current_cnt
                diff_dic['block_list'].append(block_dic)

            if diff_dic:
                result.append(diff_dic)
            
            # diff_dic init
            diff_dic = dict()
            diff_dic['block_list'] = list()
            block_dic = dict()

            method = line.rsplit(' ', 1)[1]
            method = method.split('/', 1)[1]
            method = method.replace("src/main/java/", "")
            method = method.rsplit(".", 1)[0]
            method = method.replace("/", ".")
            diff_dic['method'] = method
        elif '@@' in line:
            if block_dic:
                block_dic['prev_line_cnt'] = prev_cnt
                block_dic['current_line_cnt'] = current_cnt
                diff_dic['block_list'].append(block_dic)
            
            # block dict init
            block_dic = dict()
            prev_cnt = 0
            current_cnt = 0

            prev_line_num = line.split(",", 1)[0].split("-")[1]
            current_line_num = line.split("+")[1].split(",")[0]

            block_dic['prev_line_start'] = prev_line_num
            block_dic['current_line_start'] = current_line_num
        elif line:
            if line[0] == '-' and line[1] == ' ':
                prev_cnt += 1
            elif line[0] == '+' and line[1] == ' ':
                current_cnt += 1


    block_dic['prev_line_cnt'] = prev_cnt
    block_dic['current_line_cnt'] = current_cnt
    diff_dic['block_list'].append(block_dic)
    result.append(diff_dic)
    
    return result
    


def outputting_result(data):
    result_list = []

    i = 0
    for datum in data:
        if i == 3:
            break

        id_str = datum['id']
        exception_str = datum['exception'][0]
        loc_list = datum['location']
        
        result_str = id_str + '\n' + exception_str + '\n'
        for loc in loc_list:
            result_str += '\t' + loc +'\n'

        result_list.append(result_str)
        i += 1

    return result_list




def main():
    cnt = 0
    data3 = []

    heuristic_key = 'heuristic' + sys.argv[3]
    heuristic_dict = {
        'heuristic1': heuristic1,
        'heuristic2': heuristic2,
        'heuristic3': heuristic3,
        'heuristic4': heuristic4,
        'heuristic5': heuristic5,
        'heuristic6': heuristic6,
        'heuristic7': heuristic7,
        'heuristic8': heuristic8,
        'heuristic9': heuristic9,
        'heuristic10': heuristic10
    }

    diff_result = init_git_diff()
    
    for i in data2['descriptions']:
        # if not heuristic_dict[heuristic_key](i, changed_method_list):
        if not heuristic4(i): # best heuristic
            cnt+=1
            data3.append(copy.deepcopy(i))


    gerrit_server_address = sys.argv[7]
    num_of_output = sys.argv[8]

    if num_of_output.isdigit():
        num_of_output = int(num_of_output)


    result = outputting_result(data3)
    if num_of_output:
        num_of_output_final = min(len(result), num_of_output)
    else:
        num_of_output_final = len(result)

    for i in range(num_of_output_final):
        command1 = "ssh -p 29418 " + gerrit_server_address + " gerrit review —code-review 0 -m "
        command2 = " $(git rev-parse HEAD)"
        command = command1 + "cat << EOF\n" + result[i] + "EOF" + command2
        subprocess.call(command, shell=True)


if __name__ == "__main__":
    main()


