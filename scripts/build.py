#!/usr/bin/python

import tempfile
import subprocess
import datetime
import time
from shutil import copyfile, rmtree
import os
import sys

mode = sys.argv[1]

dir = tempfile.mkdtemp()

fout = open(dir + "/out.log", "w")
ferr = open(dir + "/err.log", "w")

print("Running commands in " + dir + "...")

t1 = time.time()
p = subprocess.Popen([os.getcwd() + "/" + mode + ".sh"],
                     stdout=fout, stderr=ferr, cwd=dir,
                     shell=True)
ret = p.wait()
t2 = time.time()

fout.close()
ferr.close()

now = datetime.datetime.now().isoformat()

if ret == 0:
    status = "success"
else:
    status = "failure"

filename = now + "%" + mode + "%" + str(t2 - t1) + "%" + status

copyfile(dir + "/out.log", "../static/logs/" + filename + ".out.log")
copyfile(dir + "/err.log", "../static/logs/" + filename + ".err.log")

# if status == "success":
#    rmtree(dir)
