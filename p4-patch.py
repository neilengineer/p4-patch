#!/usr/bin/env python
#Neil Zhao(neil.zhao@qti.qualcomm.com), Sep.,2013
import os
import sys 
import time
import subprocess

def usage():
  print "Usage: %s patch_file level(same as the 'N' in '-pN' option for 'patch' cmd)" %sys.argv[0]
  exit(1)

if len(sys.argv)!=3:
  usage()

time=time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time()))
patchfile=sys.argv[1]
patchlevel=int(sys.argv[2])
patchlog="/tmp/patch.log.%s"%time
target_files=[]

#open log file 
log=open(patchlog,'w')

#get files to patch from the patch file
file=open(patchfile,'r')
for i in file:
    if i.find('+++')>=0:
        temp_str=i.strip().replace("+++ ","").split('\t')[0].split('/')[patchlevel:len(i)]
        target_files.append("/".join(temp_str))
file.close()

#check out files if necessary
print "================processing the target files===================="
print target_files
num_of_missing=0
for i in target_files:
    if os.path.exists(i):
        cmd='p4 opened '+i
        cmd_output=subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        if cmd_output.find('not')>=0:
            print "%s not opened, check it out now!"%i
            cmd='p4 edit '+i
            subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        else:
            print "%s: "%i+" this file's already checked out! watch out!".upper()
    else:
        print "%s doesn't exist" %i
        num_of_missing+=1

if num_of_missing==len(target_files):
    print "No target files found to patch in current directory, wrong directory?"
    exit(2)

#patch
print "================patching the target files===================="
cmd="patch -p%d < %s" %(patchlevel,patchfile)
print "patch with cmd: %s" %cmd
try:
    patch_output=subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
except (RuntimeError,subprocess.CalledProcessError):
    print "patch failed: wrong patch level? OR already patched? "
    exit(3)
log.write(patch_output)
log.close
print "Log is at: %s" %patchlog

