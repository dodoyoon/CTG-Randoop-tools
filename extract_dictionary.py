import os, re, sys

def determine_num(n):
    if '.' in n:
        natural = n.split(".")[0]
        decimal = n.split(".")[1]
        if len(natural) + len(decimal) > 7:
            return n, "double"
        elif len(decimal) > 0:
            return n, "float"
        else: # number that ends with '.'
            num = int(natural)
            if -2147483648 <= num <= 2147483647: 
                return natural, "int"
            else:
                return natural, "long"
    else:
        num = int(n)
        if -2147483648 <= num <= 2147483647: 
            return n, "int"
        else:
            return n, "long"

def main():
    ''' 
    Regular Expression Description
    1. number literal: ^[^/\*\d\+\-\"]*([+-]?([0-9]*[.])?[0-9]+)
    2. string literal: ^[^/*\(]*?(\".*?\")
    Both num and str literal regex ignores lines starting with comments
    '''
    final_regex = r'^[^/\*\d\+\-\"]*([+-]?([0-9]*[.])?[0-9]+)|^[^/*\(]*?(\".*?\")'

    src_file_path = sys.argv[1]
    save_file_path = sys.argv[2] + "/literalsfile.txt"

    f = open(save_file_path, "w")

    for dirpath, dirs, files in os.walk(src_file_path): 
        for filename in files:
            if '.java' in filename:
                f.write("START CLASSLITERALS\n\n")
                f.write("CLASSNAME\n")
                class_name = filename.split('.')[0]
                fname = os.path.join(dirpath,filename)
                temp_dirpath = dirpath.replace('/', '.').lstrip('.')
                class_name = temp_dirpath + '.' + class_name
                to_be_removed = src_file_path.rsplit("/", 1)[0]
                to_be_removed = to_be_removed.replace("/", ".") + "."
                class_name = class_name.replace(to_be_removed, "")

                print("class name: ", class_name)

                f.write(class_name+'\n\n')
                f.write("LITERALS\n")

                # prevent duplication
                literal_set = set()

                with open(fname) as myfile:
                    lines = myfile.readlines()
                    for line in lines:
                        matches = re.findall(final_regex, line)

                        if matches:
                            for match in matches:
                                if match:
                                    for val in match:
                                        if val:
                                            val = val.strip()
                                            if val[0].isdigit() or (val[0] == '-' and val[1].isdigit()):
                                                num, num_type = determine_num(val)
                                                literal_set.add(num_type+':'+num+'\n')
                                            elif val[0] == '"':
                                                if len(val) != 2:
                                                    literal_set.add('String:'+val+'\n')


                # here is the end of the file
                for literal in literal_set:
                    f.write(literal)

                f.write("\nEND CLASSLITERALS\n\n")

    f.close()


if __name__ == "__main__":
    # execute only if run as a script
    main()

