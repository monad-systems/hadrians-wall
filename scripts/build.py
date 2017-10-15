#!/usr/bin/python

import tempfile
import subprocess
import datetime
import time
from shutil import copyfile, rmtree
import os
import sys

tmp_dir = tempfile.mkdtemp()
script_dir = os.path.dirname(os.path.abspath(__file__))

mode = sys.argv[1]
if len(sys.argv) == 3:
    ghc_dir = sys.argv[2]
else:
    subprocess.call("git clone --depth 1 --recursive git://github.com/ghc/ghc", cwd=tmp_dir)
    ghc_dir = tmp_dir + "/" + "ghc"
    subprocess.call("git clone https://github.com/snowleopard/hadrian", cwd=ghc_dir)

print("Putting logs in " + tmp_dir)

fout = open(tmp_dir + "/out.log", "w")
ferr = open(tmp_dir + "/err.log", "w")

t1 = time.time()

hadrian_dir = ghc_dir + "/hadrian"

print("Running commands in " + hadrian_dir + "...")
p = subprocess.Popen([script_dir + "/" + mode + ".sh"],
                     stdout=fout, stderr=ferr, cwd=hadrian_dir,
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

logs_dir = script_dir + "/../static/logs/"
os.system("mkdir -p " + logs_dir)

copyfile(tmp_dir + "/out.log", logs_dir + filename + ".out.log")
copyfile(tmp_dir + "/err.log", logs_dir + filename + ".err.log")
