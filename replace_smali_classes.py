import re
import glob
import os
import fnmatch
import sys
import base64


LAST_FILE = ""
REPLACE_PAIRS = []


def main(argv):

    #g_java = glob.glob(DIRECTORY)
    #print g_java

    if len(argv) != 2:
        print "Usage: replace_smali_classes.py <SMALI_SOURCES_DIRECTORY>"
        return

    DIRECTORY = argv[1]
    
    matches = find_smali_files(DIRECTORY)
    #print matches

    #for x in matches:
    #    print x

    #matches = [FILENAME]
    classname_replaces = find_source_filename_in_files(matches)

    #print classname_replaces
    
    for filename in matches:
        print "Replacing in ", filename

        with open(filename) as f:
            s = f.read()
        for replacement in classname_replaces:
            s = s.replace(replacement, classname_replaces[replacement])

        with open(filename, "w") as f:
            f.write(s)



    
    print "\nfinished"
    #sys.stdin.read()

def find_source_filename_in_files(filenames):
    print "Look for source filenames in %s" % filenames
    source_filenames = {}
    for filename in filenames:
        
        found_filenames = find_source_filename_in_file(filename)
        if found_filenames != []:
            print "Found %s" % found_filenames
            #source_filenames += found_filenames

            found_classnames = find_classname_in_file(filename)
            if found_classnames != []:
                print "Found %s" % found_classnames
                orig_classname = found_classnames[0][found_classnames[0].find("L"):]
                print "Original class name: %s" % orig_classname


                newclassname = found_filenames[0][found_filenames[0].find("\"")+1:found_filenames[0].rfind(".")]
                newclassname = orig_classname[:orig_classname.rfind("/")+1] + newclassname + ";"
                print "New class name:      %s" % newclassname

                if orig_classname.find("$") != -1:
                    print "Detected subclass, skipping..."
                    continue

                if orig_classname == newclassname:
                    print "Both class names same, skipping..."
                    continue

                print "replacing %s with %s" % (orig_classname, newclassname)
                source_filenames[orig_classname] = newclassname

    return source_filenames

def find_source_filename_in_file(filename):
    print "Look for source filename in %s" % filename

    found = None
    with open(filename) as f:
        file_data = f.read()

        code_reg = re.compile("\.source \".*?\"")
        found = code_reg.findall(file_data)
        
        #for f1 in found:
        #    print f1
        #    print "\n"

    return found

def find_classname_in_file(filename):
    print "Look for classname in %s" % filename

    found = None
    with open(filename) as f:
        file_data = f.read()

        code_reg = re.compile("\.class .*?;")
        found = code_reg.findall(file_data)
        
        #for f1 in found:
        #    print f1
        #    print "\n"

    return found


def replace_codes_in_file(filename, replace_pairs):

    if filename == "":
        return
    print "Replacing codes in %s" % filename
    data = ""
    with open(filename) as f:
        data = f.read()
        for pair in replace_pairs:
            print "Replace %s with %s" % (pair[0], pair[1])
            data = data.replace(pair[0], "\"" + pair[1] + "\"")
    
    print "----data----"
    print data
    #newfilename = os.path.splitext(filename)[0] + "_modified" + os.path.splitext(filename)[1]
    #newfilename = filename.replace("classes_sources", "classes_sources_modified")
    newfilename = filename
    if not os.path.exists(os.path.dirname(newfilename)):
        os.makedirs(os.path.dirname(newfilename))
    with open(newfilename, "wt") as f:    
        f.write(data)

    #replace_pairs = []


def find_appsee_code_obfuscations(filename):
    found = None
    with open(filename) as f:
        file_data = f.read()

        code_reg = re.compile("(wc.D\(\".*?\"\)|eb.D\(\".*?\"\)|hd.D\(\".*?\"\)|ie.D\(\".*?\"\)|kd.m\(\".*?\"\)|db.D\(\".*?\"\)|nh.D\(\".*?\"\)|rm.D\(\".*?\"\)|rk.D\(\".*?\"\))")
        #code_reg = re.compile("(wc|eb).D\(\".*?\"\)")
        found = code_reg.findall(file_data)
        
        #for f1 in found:
        #    print f1
        #    print "\n"

    return found



def find_rb64_expressions_in_file(filename):
    print "Look for source filename in %s" % filename

    found = None
    with open(filename) as f:
        file_data = f.read()

        code_reg = re.compile("rb64\(.*?\)")
        found = code_reg.findall(file_data)
        
        #for f1 in found:
        #    print f1
        #    print "\n"

    return found


def find_code_array_expressions_in_file(filename):
    #print "Look for Code expressions in %s" % filename

    found = None
    with open(filename) as f:
        file_data = f.read()

        #code_reg = re.compile("objArr+\[0\] = Integer\.valueOf\(1\).*?Code.code.*?Code.decode\(.*?\)", re.S)
        code_reg = re.compile("Code.code\(Code.some\(.*?Code.decode\(.*?\)", re.S)
        found = code_reg.findall(file_data)
        
        found_formatted = []

        for f1 in found:
            #print f1

            splitted = f1.split("\n")
            print "1: " + splitted[0]
            print "2: " + splitted[1]

            reformatted = "Code.decode(Integer.valueOf(1), " + splitted[0][:-1] + ")"
            print reformatted
            found_formatted.append(reformatted)

            print "\n"


    #return found
    return found_formatted

def find_smali_files(source_directory):
    matches = []

    for root, dirnames, filenames in os.walk(source_directory):
        for filename in fnmatch.filter(filenames, "*.smali"):
            matches.append(os.path.join(root, filename))
        
    return matches

def format_code_expression(expression_str):

    expression_str = expression_str.replace("Integer", "[Integer").replace(")))", "]))])")
    if expression_str.find("someD") != -1:
        #expression_str = expression_str.replace("decodeD(", "decode(").replace("codeD(", "code(").replace("someD(", "some([")
        expression_str = expression_str.replace("someD(", "someD([")
    else:
        expression_str = expression_str.replace("some(", "some([")

    return expression_str

def reformat_code_expression(expression_str):
    
    expression_str = expression_str.replace("[Integer", "Integer").replace("]))])", ")))")

    if expression_str.find("someD") != -1:
        expression_str = expression_str.replace("someD([", "someD(")
    else:
        expression_str = expression_str.replace("some([", "some(")
    return expression_str


if __name__ == "__main__":
    main(sys.argv)