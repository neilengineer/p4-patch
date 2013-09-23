This tool written in python will apply patches genereated by diff to perforce managed files. 
It'll check if the target file(s) are opened, if not, check them out and apply the patches.

Usage: ./p4-patch.py patch_file level(same as the 'N' in '-pN' option for 'patch' cmd)
