import sys
import subprocess
import glob
import zipfile


#"dexdump.exe %s | grep \"Class descriptor\" | cut -d':' -f2 | cut -c4- | cut -d'/' -f1-2 | uniq |sort"

def find_dex_packages(dex_filename):
	p = subprocess.Popen("dexdump.exe %s" % dex_filename, stdout=subprocess.PIPE)
	result = p.communicate()[0]
	result = result.split("\n")

	packages = []

	for i in result:
		if i.find("Class descriptor") != -1:
			package = i[24:].split("/")
			if len(package) >= 2:
				final_package = package[0]+"."+package[1]
				#if len(package) >= 3:
				#	final_package += "."+package[2]
				#if ";" in final_package:
				#	continue
				packages.append(final_package)

				
	packages = list(set(packages))
	packages.sort()
	return packages
	#print packages
	#for p in packages:


def print_app(app_path):
	print "***************************************"
	print "Testing %s" % app_path
	print "***************************************"
	
def unzip_apk(apk_path):
	zip_ref = zipfile.ZipFile(apk_path, 'r')
	zip_ref.extractall(apk_path[:-4])
	zip_ref.close()

def process_apk(apk_path):
	print_app(apk_path)
	print "Unzipping..."
	unzip_apk(apk_path)
	dex_glob = glob.glob(apk_path[:-4] + "\\*.dex")
	packages = []
	for dex_path in dex_glob:
		packages += find_dex_packages(dex_path)
	print packages
	return packages
	
def main(argv):
	if len(argv) != 2:
		print "Usage: print_packages.py <APKS_DIRECTORY>"
		return
	apks_directory = argv[1]
	g1 = glob.glob(apks_directory + "\\*.apk")

	packages1 = process_apk(g1[0])

	for apk in g1:
		packages2 = process_apk(apk)
		packages1 =  list(set(packages1).intersection(packages2))
		
	print "***************************************"
	print "Common packages"
	print packages1
	
if __name__ == "__main__":
	main(sys.argv)