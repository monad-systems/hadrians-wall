#!/usr/bin/python

import tempfile
import subprocess
import datetime
import time
from shutil import copyfile
import os

dir = tempfile.gettempdir()

fout = open(dir + "/out.log", "w")
ferr = open(dir + "/err.log", "w")

t1 = time.time()
p = subprocess.Popen([os.getcwd() + "/quickest.sh"],
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

filename = now + "%" + "quickest" + "%" + str(t2 - t1) + "%" + status

copyfile(dir + "/out.log", "../logs/" + filename + ".out.log")
copyfile(dir + "/err.log", "../logs/" + filename + ".err.log")
