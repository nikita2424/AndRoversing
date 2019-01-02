import re
import glob
import os
import fnmatch
import frida
import sys
import base64

LAST_FILE = ""
REPLACE_PAIRS = []


def main(argv):

    #g_java = glob.glob(DIRECTORY)
    #print g_java

    if len(argv) != 3:
        print "Usage: find_code_calls.py <SOURCES_DIRECTORY> <APP_PACKAGE_NAME>"
        return

    DIRECTORY = argv[1]
    APP_PACKAGE_NAME = argv[2]
    
    matches = find_java_files(DIRECTORY)
    #print matches

    process = frida.get_usb_device().attach(APP_PACKAGE_NAME)

    #matches = [FILENAME]
    #code_exps = find_code_expressions_in_files(matches)
    for filename in matches:
        #print "Looking for code expressions in ", filename

        code_exps = find_code_expressions_in_file(filename)
        if len(code_exps) > 0:
            print "Found %d Code expressions in %s" % (len(code_exps), filename)
            deobfuscate_with_frida(filename, code_exps, process)

        rb64_exps = find_rb64_expressions_in_file(filename)
        if len(rb64_exps) > 0:
            print "Found %d rb64 expressions in %s" % (len(rb64_exps), filename)
            replace_rb64_expressions(filename, rb64_exps)

        arr_exps = find_code_array_expressions_in_file(filename)
        if len(arr_exps) > 0:
            print "Found %d code arr expressions in %s" % (len(arr_exps), filename)
            deobfuscate_with_frida("", arr_exps, process)
            #replace_rb64_expressions(filename, rb64_exps)

        appsee_exps = find_appsee_code_obfuscations(filename)
        if len(appsee_exps) > 0:
            print "Found %d appsee code expressions in %s" % (len(appsee_exps), filename)
            print appsee_exps
            deobfuscate_appsee_with_frida(filename, appsee_exps, process)


    
    #for express in code_exps:
    #    deobfuscate_with_frida(express, process)
    print "finished"
    sys.stdin.read()


def replace_rb64_expressions(filename, rb64_expressions):
    pairs_to_replace = []
    for exp in rb64_expressions:
        orig_exp  = exp
        i1 = exp.find("\"")
        i2 = exp.rfind("\"")
        print exp
        exp = exp[i1+1:i2]

        try:
            pairs_to_replace.append((orig_exp,base64.b64decode(exp[::-1])))

        except Exception as e:
            print e

    replace_codes_in_file(filename, pairs_to_replace)

def deobfuscate_with_frida(orig_filename, code_expressions, process):
    jscode = """
Java.perform(function () {
     
     printAfterDecode("%s", %s);
});

function printAfterDecode(orig_filename, codes_to_execute) {
    
    GlowPadView = { 

        TYPE_CENTER_DRAWABLE: 101,
        TYPE_CLOUD_DRAWABLE: 102,
        TYPE_FAKE: 100,
        TYPE_LOCK_DRAWABLE: 103,
        TYPE_LOLIPOP_CENTER: 102,
        TYPE_LOLIPOP_CLOUD: 103,
        TYPE_LOLIPOP_LOCK: 104,
        TYPE_NORMAL_CENTER: 105,
        TYPE_NORMAL_CLOUD: 106,
        TYPE_NORMAL_LOCK: 107,
        TYPE_OUTERING: 101
    };

    TYPE_CENTER_DRAWABLE = 101;
    TYPE_CLOUD_DRAWABLE = 102;
    TYPE_FAKE = 100;
    TYPE_LOCK_DRAWABLE = 103;
    TYPE_LOLIPOP_CENTER = 102;
    TYPE_LOLIPOP_CLOUD = 103;
    TYPE_LOLIPOP_LOCK = 104;
    TYPE_NORMAL_CENTER = 105;
    TYPE_NORMAL_CLOUD = 106;
    TYPE_NORMAL_LOCK = 107;
    TYPE_OUTERING = 101;

    PARAM_APPLICATION_BUNDLE = 18;
    PARAM_APPLICATION_LOCALIZATION = 19;
    PARAM_APPLICATION_VERSION = 20;
    PARAM_APPLICATION_VERSION_CODE = 21;
    PARAM_BUILD_SERIAL = 52;
    PARAM_CHAINS_IN_SPOT = 44;
    PARAM_CHAINS_IN_SPOT_REMAINING = 45;
    PARAM_CORE_VERSION_CODE = 79;
    PARAM_CURRENT_CORE_VERSION_CODE = 17;
    PARAM_CURRENT_DEVICE_ORIENTATION = 33;
    PARAM_CURRENT_INJECTOR_VERSION_CODE = 16;
    PARAM_CURRENT_OPENED_APPLICATION_BUNDLE = 30;
    PARAM_DEVICE_ID = 14;
    PARAM_DEVICE_IMEI = 41;
    PARAM_DEVICE_MODEL = 35;
    PARAM_DEVICE_OS_API = 31;
    PARAM_DEVICE_SCREEN_DPI = 38;
    PARAM_DEVICE_SCREEN_HEIGHT = 37;
    PARAM_DEVICE_SCREEN_WIDTH = 36;
    PARAM_DEVICE_TYPE = 13;
    PARAM_DEVICE_VENDOR = 34;
    PARAM_DNS_LATENCY = 59;
    PARAM_DOMAIN = 58;
    PARAM_FORMAT_ID = 27;
    PARAM_GOOGLE_AD_ID = 51;
    PARAM_GPMARKET_AVAILABLE = 40;
    PARAM_GPSERVICE_AVAILABLE = 39;
    PARAM_HORIZONTAL_ACCURACY = 56;
    PARAM_LATITUDE = 54;
    PARAM_LEGAL = 61;
    PARAM_LINE_ID = 42;
    PARAM_LONGTITUDE = 55;
    PARAM_NETWORK_ID = 25;
    PARAM_NETWORK_KEY_PACK_ID = 26;
    PARAM_NETWORK_QUEUE_SORT_TYPE = 23;
    PARAM_NETWORK_REQUESTING_SUCCESSFULL_STATE = 24;
    PARAM_NETWORK_TYPE = 29;
    PARAM_NEW_CORE_VERSION = 7;
    PARAM_NEW_CORE_VERSION_CODE = 8;
    PARAM_NEW_INJECTOR_VERSION = 5;
    PARAM_NEW_INJECTOR_VERSION_CODE = 6;
    PARAM_OLD_CORE_VERSION = 3;
    PARAM_OLD_CORE_VERSION_CODE = 4;
    PARAM_OLD_INJECTOR_VERSION = 1;
    PARAM_OLD_INJECTOR_VERSION_CODE = 2;
    PARAM_OPTOUT_STATE = 22;
    PARAM_PERMISSION_LOCATION_GRANTED = 53;
    PARAM_PERMISSION_STORAGE_GRANTED = 90;
    PARAM_PIRACY_DETECTION_APP_SKU = 85;
    PARAM_PIRACY_DETECTION_IS_LEGAL_APP = 86;
    PARAM_PIRACY_DETECTION_IS_LEGAL_GEO = 82;
    PARAM_PIRACY_DETECTION_IS_LEGAL_SKU = 83;
    PARAM_PIRACY_DETECTION_IS_MARKET_WHITELIST_ENTRY = 81;
    PARAM_PIRACY_DETECTION_MARKET_WHITELIST = 80;
    PARAM_PIRACY_DETECTION_PUB_SKU = 84;
    PARAM_PIRACY_NOTIFIER_CLOSE_ACTION_ERROR = 89;
    PARAM_PIRACY_NOTIFIER_CLOSE_ACTION_ID = 88;
    PARAM_PIRACY_NOTIFIER_DISCLAIMER_ID = 87;
    PARAM_PUSH_AD_AWARDED_RESULT = 65;
    PARAM_PUSH_AD_CANCEL_REASON = 64;
    PARAM_PUSH_AD_REQUESTED_RESULT = 63;
    PARAM_PUSH_ID = 60;
    PARAM_QUEUE_ID = 43;
    PARAM_REASON = 47;
    PARAM_REWARDED = 62;
    PARAM_RULE_ID = 15;
    PARAM_SEARCH_WIDGET_REQUEST = 48;
    PARAM_SESSION_EVENTS = 76;
    PARAM_SESSION_EVENT_NAME = 77;
    PARAM_SESSION_EVENT_TIME = 78;
    PARAM_SESSION_ID = 66;
    PARAM_SESSION_RESULT = 69;
    PARAM_SESSION_START_TIME = 68;
    PARAM_SOURCE_INSTALL = 12;
    PARAM_SPOT_CHAIN_ID = 32;
    PARAM_SPOT_FAILED_REASON = 75;
    PARAM_SPOT_ID = 28;
    PARAM_SPOT_LIFECYCLE_CHAIN_ID = 72;
    PARAM_SPOT_TIME_SINCE_ADD = 73;
    PARAM_SPOT_TIME_SINCE_LAUNCH = 74;
    PARAM_STAT_DEVICE_TIME = 11;
    PARAM_STAT_ID = 0;
    PARAM_STAT_TIME = 10;
    PARAM_SUCCESS_CHAIN_ID = 71;
    PARAM_SUCCESS_SPOT_ID = 70;
    PARAM_TAPCORE_APP_ID = 9;
    PARAM_TIME_FROM_PREVIOUS_SESSIONS = 67;
    PARAM_TUID = 49;
    PARAM_TUID_TIME = 50;
    PARAM_USER_AGENT = 57;
    PARAM_USER_ID = 91;
    
    var classAtomicBoolean = Java.use("java.util.concurrent.atomic.AtomicBoolean");
    classAtomicBoolean.get.implementation = function() {
        return true;
    };

    var className = "com.core.CoreExternalFunctions$Code"
    var Code = Java.use(className);
    
    var Integer = Java.use("java.lang.Integer");
    
    results = []
    for (i in codes_to_execute) {

        var result = eval(codes_to_execute[i]);
        console.log(codes_to_execute[i] + " --> " + result);
        //send(orig_filename + " --> " + codes_to_execute[i] + " --> " + result);
        results.push(codes_to_execute[i] + " --> " + result);            
    }
    
    final_results = []
    final_results.push(orig_filename);
    final_results.push(results);
    send(final_results);
}

"""
    for i in xrange(0, len(code_expressions)):
        code_expressions[i] = format_code_expression(code_expressions[i])
    jscode = jscode % (base64.b64encode(orig_filename), str(code_expressions))
    #print jscode

    script = process.create_script(jscode)
    #script = process.compile_script(jscode)
    script.on('message', on_message)
    script.load()


def deobfuscate_appsee_with_frida(orig_filename, code_expressions, process):
    jscode = """
Java.perform(function () {
     
     printAfterDecode("%s", %s);
});

function printAfterDecode(orig_filename, codes_to_execute) {
      
    var eb = Java.use("com.appsee.eb");
    var wc = Java.use("com.appsee.wc");
    var hd = Java.use("com.appsee.hd");
    var ie = Java.use("com.appsee.ie");
    var kd = Java.use("com.appsee.kd");
    var db = Java.use("com.appsee.db");
    var nh = Java.use("com.appsee.nh");
    var rm = Java.use("com.appsee.rm");
    var rk = Java.use("com.appsee.rk");

    results = []
    for (i in codes_to_execute) {

        var result = eval(codes_to_execute[i]);
        console.log(codes_to_execute[i] + " --> " + result);
        //send(orig_filename + " --> " + codes_to_execute[i] + " --> " + result);
        results.push(codes_to_execute[i] + " --> " + result);            
    }
    
    final_results = []
    final_results.push(orig_filename);
    final_results.push(results);
    send(final_results);
}

"""
    #for i in xrange(0, len(code_expressions)):
    #    code_expressions[i] = format_code_expression(code_expressions[i])
    jscode = jscode % (base64.b64encode(orig_filename), str(code_expressions))
    #print jscode

    script = process.create_script(jscode)
    #script = process.compile_script(jscode)
    script.on('message', on_message)
    script.load()

script = None

def on_message(message, data):
    if message['type'] == 'send':
        payload = message['payload']
        #print payload
        orig_filename = ""
        try:
            orig_filename = base64.b64decode(payload[0])
        except Exception as e:
            print e

        if orig_filename == "":
            return

        pairs_to_replace = []
        for replace_pair in payload[1]:
            splitted = replace_pair.split(' --> ')
            code_exp = reformat_code_expression(splitted[0])
            resolved_str = splitted[1]
            pairs_to_replace.append((code_exp, resolved_str))

         
        replace_codes_in_file(orig_filename, pairs_to_replace)

         #print orig_filename
         #print code_exp
         #print resolved_str
          #print("[*] {0}".format(message['payload']))
    else:
        print(message)

    #print script
    #script.unload()

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

def find_code_expressions_in_files(filenames):
    code_exps = []
    for filename in filenames:
        
        code_exps += find_code_expressions_in_file(filename)

    return code_exps

def find_rb64_expressions_in_file(filename):
    #print "Look for Code expressions in %s" % filename

    found = None
    with open(filename) as f:
        file_data = f.read()

        code_reg = re.compile("rb64\(.*?\)")
        found = code_reg.findall(file_data)
        
        #for f1 in found:
        #    print f1
        #    print "\n"

    return found


def find_code_expressions_in_file(filename):
    #print "Look for Code expressions in %s" % filename

    found = None
    with open(filename) as f:
        file_data = f.read()

        code_reg = re.compile("Code.decode.?\(.*?Code.code.?\(.*?Code.some.?\(.*?\)\)\)")
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

def find_java_files(source_directory):
    matches = []

    for root, dirnames, filenames in os.walk(source_directory):
        for filename in fnmatch.filter(filenames, "*.java"):
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