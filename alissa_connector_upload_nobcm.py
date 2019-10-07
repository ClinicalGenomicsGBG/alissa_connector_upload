#!/apps/bio/software/anaconda2/envs/vilma_general/bin/python

# Uploads vcf files and/or patientregistration
# using alissa connector.

import os
import sys
import json
import argparse
import subprocess
import time
import psutil

##############################################

parser = argparse.ArgumentParser(prog="alissa_connector_upload")
parser.add_argument("-a", "--accession", \
                        required=True, \
                        help="Sample name (accession-id, required for both patient registration and vcf upload)")
parser.add_argument("-v", "--vcfpath", \
                        help="Full path to vcf file")
parser.add_argument("-p", "--patientfolder", \
                        help="Name of patient folder (required for patient registration)")
parser.add_argument("-g", "--gender", \
                        help="Gender, female/male (required for patient registration)")
parser.add_argument("-f", "--filename", \
                        help="alissa file name, name of vcf file (required for vcf upload)")
parser.add_argument("-x", "--samplename", \
                        help="sample name, found in vcf (required for vcf upload)")
parser.add_argument("-o", "--outputdir", \
                        help="directory to put the logs in")
#parser.add_argument("-c", "--comments", \
 #                       help="comments (doesn't work for the moment)")
args = parser.parse_args()

patientfolder = ""
if args.patientfolder == "KK":
	patientfolder = "Klinisk kemi"
if args.patientfolder == "KG":
	patientfolder = "Klinisk Genetik"

# Make outputdir for log files
outputdir = ""
if args.outputdir:
	outputdir = args.outputdir
	if not os.path.isdir(outputdir):
		os.mkdir(outputdir)
else:
	outputdir = '.'

#json_name = args.filename+".json"
##############################################

# Creating json file for input to alissa connector. 
def jsonfile():
	if args.vcfpath:
		json_name = f"{outputdir}/{args.filename}.json"
		file = open(json_name,"w")
		file.write(json.dumps({'username': 'bcm', \
					'vcf': {
					'file_path': args.vcfpath, \
					'alissa_file_name': args.filename, \
					'file_type': 'VCF_FILE', \
					'samples': [ \
					{ \
					'accession': args.accession, \
					'sample': args.samplename}, \
					]}}, \
					indent=4))
		file.close()
		return json_name
	else:
		#json_name = args.filename+".json"
		json_name = f"{outputdir}/{args.accession}.json"
		file = open(json_name,"w")
		file.write(json.dumps({'username': 'bcm', \
					'patient_folder': patientfolder, \
					'patient': { \
					'accession': args.accession, \
					'sex': args.gender, \
					},#'comments': args.comments}\
					}, \
					indent=4))
		file.close()
		return json_name

# Submit using json file, customize url after
# input to json file.
def submit(url, json_name):
	# Command for uploading.
	accession = args.accession
	log = open(f'{outputdir}/alissa_upload_stderror_{accession}.log','a')
	cmd = ('curl \
		-X POST \
		-H  "Content-Type:application/json" \
		--data-binary @%s \
		%s -k') \
		% (json_name, url)
	process = subprocess.Popen(cmd, \
				stdout=subprocess.PIPE, \
				shell=True)
	while process.wait() is None:
		pass

	for line in process.stdout:
		log.write(line.decode('utf-8'))
		print((line.decode('utf-8')))

	process.stdout.close()
	log.close()


def main():
	# Make json,
	json_name = jsonfile()

	# Depending on input change url.
	# This will probably change when not dev?
	if args.vcfpath:
		# Starts alissa connector, bcm.sh.
		#log_file = open('alissa_upload.log','a')
		#cmd = ('/apps/bio/software/bench_connector/Gothenburg-1.0.1-SNAPSHOT-package/bcm.sh')
		#p = subprocess.Popen(cmd, \
                #	stdout=subprocess.PIPE, \
		#			shell=True, \
		#			cwd="/apps/bio/software/bench_connector/Gothenburg-1.0.1-SNAPSHOT-package/")
		
		#time.sleep(60)

		submit("https://127.0.0.1:8082/bcm/assayregistration/upload", json_name)

		# Killing childprocess and grandchild process.
		#parent = psutil.Process(p.pid)
		#for child in parent.children(recursive=True):
		#	child.terminate()

		#for line in p.stdout:
		#    log_file.write(line.decode('utf-8'))

		#parent.terminate()
		#p.stdout.close()
		#p.kill()
		#log_file.close()

	else:
		# Starts alissa connector, bcm.sh.
		#log_file = open('alissa_upload.log','a')
		#cmd = ('/apps/bio/software/bench_connector/Gothenburg-1.0.1-SNAPSHOT-package/bcm.sh')
		#p = subprocess.Popen(cmd, \
                #	stdout=subprocess.PIPE, \
		#			shell=True, \
		#			cwd="/apps/bio/software/bench_connector/Gothenburg-1.0.1-SNAPSHOT-package/")

		#time.sleep(60)

		submit("https://127.0.0.1:8082/bcm/assayregistration/create", json_name)

		# Killing childprocess and grandchild process.
		#parent = psutil.Process(p.pid)
		#for child in parent.children(recursive=True):
		#	child.terminate()

		#for line in p.stdout:
		#    log_file.write(line.decode('utf-8'))

		#parent.terminate()
		#p.stdout.close()
		#p.kill()
		#log_file.close()
	

if __name__ == "__main__":
	main()
