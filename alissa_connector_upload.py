#!/apps/bio/software/anaconda2/envs/vilma_general/bin/python

# Uploads vcf files and/or patientregistration
# using alissa connector.

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
#parser.add_argument("-c", "--comments", \
 #                       help="comments (doesn't work for the moment)")
args = parser.parse_args()

patientfolder = ""
if args.patientfolder == "KK":
	patientfolder = "Klinisk kemi"
if args.patientfolder == "KG":
	patientfolder = "Klinisk Genetik"

##############################################

# Creating json file for input to alissa connector. 
def jsonfile():
	if args.vcfpath:
		file = open("vcf.json","w")
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

	else:
		file = open("vcf.json","w")
		file.write(json.dumps({'username': 'bcm', \
					'patient_folder': patientfolder, \
					'patient': { \
					'accession': args.accession, \
					'sex': args.gender, \
					},#'comments': args.comments}\
					}, \
					indent=4))
		file.close()


# Submit using json file, customize url after
# input to json file.
def submit(url=""):
	# Command for uploading.
	log = open('alissa_upload_stderror.log','a')
	cmd = ('curl \
		-X POST \
		-H  "Content-Type:application/json" \
		--data-binary @vcf.json \
		%s -k') \
		% (url)
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
	jsonfile()

	# Depending on input change url.
	# This will probably change when not dev?
	if args.vcfpath:
		# Starts alissa connector, bcm.sh.
		log_file = open('alissa_upload.log','a')
		cmd = ('/apps/bio/software/bench_connector/Gothenburg-1.0.1-SNAPSHOT-package/bcm.sh')
		p = subprocess.Popen(cmd, \
                	stdout=subprocess.PIPE, \
					shell=True, \
					cwd="/apps/bio/software/bench_connector/Gothenburg-1.0.1-SNAPSHOT-package/")
		
		time.sleep(60)

		submit("https://127.0.0.1:8082/bcm/assayregistration/upload")

		# Killing childprocess and grandchild process.
		parent = psutil.Process(p.pid)
		for child in parent.children(recursive=True):
			child.terminate()

		for line in p.stdout:
			log_file.write(line.decode('utf-8'))

		parent.terminate()
		p.stdout.close()
		p.kill()
		log_file.close()

	else:
		# Starts alissa connector, bcm.sh.
		log_file = open('alissa_upload.log','a')
		cmd = ('/apps/bio/software/bench_connector/Gothenburg-1.0.1-SNAPSHOT-package/bcm.sh')
		p = subprocess.Popen(cmd, \
                	stdout=subprocess.PIPE, \
					shell=True, \
					cwd="/apps/bio/software/bench_connector/Gothenburg-1.0.1-SNAPSHOT-package/")

		time.sleep(60)

		submit("https://127.0.0.1:8082/bcm/assayregistration/create")

		# Killing childprocess and grandchild process.
		parent = psutil.Process(p.pid)
		for child in parent.children(recursive=True):
			child.terminate()

		for line in p.stdout:
			log_file.write(line.decode('utf-8'))

		parent.terminate()
		p.stdout.close()
		p.kill()
		log_file.close()
	

if __name__ == "__main__":
	main()
