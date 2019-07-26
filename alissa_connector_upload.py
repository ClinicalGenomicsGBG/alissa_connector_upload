#!/apps/bio/software/anaconda2/envs/vilma_general/bin/python

# Uploads vcf files and/or patientregistration
# using alissa connector.

import json
import argparse
import subprocess
import time

##############################################

parser = argparse.ArgumentParser(prog="vcf_to_fasta")
parser.add_argument("-s","--samplename", \
#                        required=True, \
                        help="Sample name (accessionid)")
parser.add_argument("-v", "--vcfpath", \
#                        required=True, \
                        help="Path to vcf file")
parser.add_argument("-p", "--patientfolder", \
#                        required=True, \
                        help="Name of patient folder")
parser.add_argument("-g", "--gender", \
#                        required=True, \
                        help="Gender, f/m")
parser.add_argument("-c", "--comments", \
                        help="comments")
args = parser.parse_args()

##############################################

# Creating json file for input to alissa connector. 
def jsonfile():
	if args.comments:
		file = open("vcf.json","w")
		file.write(json.dumps({'username': 'bcm', \
					'patientFolder': args.patientfolder, \
					'filePath': args.vcfpath, \
					'patient': {\
					'accession': args.samplename, \
					'gender': args.gender, \
					'comments': args.comments}\
					}, \
					indent=4))
		file.close()

	else:
		file = open("vcf.json","w")
		file.write(json.dumps({'username': 'bcm', \
					'patientFolder': args.patientfolder, \
					'filePath': args.vcfpath, \
					'patient': {\
					'accession': args.samplename, \
					'gender': args.gender}\
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
		cmd = ('/apps/bio/software/bench_connector/Gothenburg-Connector-1.0.0/bcm.sh')
		p = subprocess.Popen(cmd, \
                	                stdout=subprocess.PIPE, \
					shell=True, \
					cwd="/apps/bio/software/bench_connector/Gothenburg-Connector-1.0.0/")
		
		time.sleep(15)

		submit("https://127.0.0.1:8082/bcm/test/vcfFileUpload")

		p.stdout.close()
		p.kill()

	else:
		# Starts alissa connector, bcm.sh.
		cmd = ('/apps/bio/software/bench_connector/Gothenburg-Connector-1.0.0/bcm.sh')
		p = subprocess.Popen(cmd, \
                	                stdout=subprocess.PIPE, \
					shell=True, \
					cwd="/apps/bio/software/bench_connector/Gothenburg-Connector-1.0.0/")

		time.sleep(15)

		submit("https://127.0.0.1:8082/bcm/test/patientregistration")

		p.stdout.close()
		p.kill()

	print(p.pid)
	

if __name__ == "__main__":
	main()
