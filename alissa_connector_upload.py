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

parser = argparse.ArgumentParser(prog="vcf_to_fasta")
parser.add_argument("-a", "--accession", \
#                        required=True, \
                        help="Sample name (accessionid)")
parser.add_argument("-v", "--vcfpath", \
#                        required=True, \
                        help="Full path to vcf file")
parser.add_argument("-p", "--patientfolder", \
#                        required=True, \
                        help="Name of patient folder")
parser.add_argument("-g", "--gender", \
#                        required=True, \
                        help="Gender, f/m")
parser.add_argument("-f", "--filename", \
#                        required=True, \
                        help="alissa file name, name of vcf file")
parser.add_argument("-x", "--samplename", \
#                        required=True, \
                        help="sample name, found in vcf")
parser.add_argument("-c", "--comments", \
                        help="comments (doesn't work for the moment)")
args = parser.parse_args()

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
					'patient_folder': args.patientfolder, \
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
	process.stdout.close()


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
		
		time.sleep(15)

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

		time.sleep(15)

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
