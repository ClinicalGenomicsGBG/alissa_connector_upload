#!/apps/bio/software/anaconda2/envs/vilma_general/bin/python

# Rquires bcftools/1.9

import sys
import subprocess
import argparse
import os

###########################################

parser = argparse.ArgumentParser(prog="merge_vcf.py")
parser.add_argument("-v1", "--vcf1", \
        required=True, \
        help="VCF 1 input, unzipped")
parser.add_argument("-v2", "--vcf2", \
        required=True, \
        help="VCF 2 input, unzipped")
parser.add_argument("-m", "--merge", \
        action="store_true", \
        help="Merge two VCF")
parser.add_argument("-c", "--concat", \
        action="store_true", \
        help="Concat two VCF, allows overlaps")
parser.add_argument("-o", "--output", \
        help="Output name")
args = parser.parse_args()

###########################################

vcf1 = args.vcf1
vcf2 = args.vcf2
vcf_bg1 = os.path.basename(vcf1) + ".bgz"
vcf_bg2 = os.path.basename(vcf2) + ".bgz"

output = ""
if args.output:
    output = args.output
else:
	if args.concat:
	    output = 'concat_' + os.path.basename(vcf1) + '_' + os.path.basename(vcf2) + '.gz'
	if args.merge:
	    output = 'merged_' + os.path.basename(vcf1) + '_' + os.path.basename(vcf2) + '.gz'

###########################################

# bgzip vcf file.
cmd_1 = ['bcftools', 'view', vcf1, '-Ob', '-o', vcf_bg1]
process_1 = subprocess.Popen(cmd_1, \
            stdout=subprocess.PIPE)
while process_1.wait() is None:
    pass
process_1.stdout.close()

cmd_2 = ['bcftools', 'view', vcf2, '-Ob', '-o', vcf_bg2]
process_2 = subprocess.Popen(cmd_2, \
            stdout=subprocess.PIPE)
while process_2.wait() is None:
    pass
process_2.stdout.close()

# Index files, required for bcftools merged.
cmd_3 = ['bcftools', 'index', vcf_bg1]
process_3 = subprocess.Popen(cmd_3, \
            stdout=subprocess.PIPE)
while process_3.wait() is None:
    pass
process_3.stdout.close()

cmd_4 = ['bcftools', 'index', vcf_bg2]
process_4 = subprocess.Popen(cmd_4, \
            stdout=subprocess.PIPE)
while process_4.wait() is None:
    pass
process_4.stdout.close()

# Merge vcf files.
if args.merge:
	cmd_5 = ['bcftools', 'merge', \
        	'--force-samples', \
		    vcf_bg1, vcf_bg2, \
		    '-Oz', '-o', output]   
	process_5 = subprocess.Popen(cmd_5, \
		    stdout=subprocess.PIPE)
	while process_5.wait() is None:
	    pass
	process_5.stdout.close()

# Concat vcf files.
if args.concat:
	cmd_6 = ['bcftools', 'concat', \
		    '--allow-overlaps', \
		    vcf_bg1, vcf_bg2, \
		    '-Oz', '-o', output]   
	process_6 = subprocess.Popen(cmd_6, \
		    stdout=subprocess.PIPE)
	while process_6.wait() is None:
	    pass
	process_6.stdout.close()

# Remove the intermediate files, bgzip and index.
os.remove(vcf_bg1)
os.remove(vcf_bg2)
os.remove(vcf_bg1+'.csi')
os.remove(vcf_bg2+'.csi')
