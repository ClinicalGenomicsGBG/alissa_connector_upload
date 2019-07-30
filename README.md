# alissa_connector_upload

Uploads vcf files and/or patientregistration
using alissa connector.

Requires full path to vcf file.

Different url:s depending on input, 
think this will change when not dev(?)

## Utility    

`merge_vcf.py` is a script that merges two vcf files.
Output is a gzipped vcf file.
It uses bcftools `view`, `index` and `merge`.   

**Usage**:  

`./merge_vcf.py --vcf1 --vcf2` 

## Dependencies    

bcftools version 1.9
