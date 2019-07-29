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
args = parser.parse_args()

###########################################

vcf1 = args.vcf1
vcf2 = args.vcf2
print(vcf1)
vcf_bg1 = os.path.basename(vcf1)+".bgz"
print(vcf_bg1)
vcf_bg2 = os.path.basename(vcf2)+".bgz"
merged_vcf = 'merged_' + os.path.basename(vcf1) + '_' + os.path.basename(vcf2) + '.gz'

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
cmd_5 = ['bcftools', 'merge', \
	'--force-samples', \
        vcf_bg1, vcf_bg2, \
        '-Oz', '-o', merged_vcf]   
process_5 = subprocess.Popen(cmd_5, \
            stdout=subprocess.PIPE)
while process_5.wait() is None:
    pass
process_5.stdout.close()
