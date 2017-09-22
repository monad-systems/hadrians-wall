#!/usr/bin/python

import tempfile
import subprocess
import datetime
import time
import json
from shutil import copyfile, rmtree
import os
import sys

import meta

tmpdir = tempfile.mkdtemp()

helpinfo = "usage: ./build.py <mode> [optional-ghc-path]"

if len(sys.argv) < 2:
    print(helpinfo)
    sys.exit(-1)

if sys.argv[1] == "--help":
    print(helpinfo)
    sys.exit(0)

if len(sys.argv) == 2:
    mode = sys.argv[1]
    subprocess.call(["git", "clone", "--depth", "1", "--recursive", "git://github.com/ghc/ghc"], cwd = tmpdir)
    subprocess.call(["git", "clone", "https://github.com/snowleopard/hadrian", "ghc/hadrian"], cwd = tmpdir)
    ghc_path = tmpdir + "/ghc"
elif len(sys.argv) == 3:
    ghc_path = sys.argv[2]
else:
    print(helpinfo)
    sys.exit(-1)

fout = open(tmpdir + "/out.log", "w")
ferr = open(tmpdir + "/err.log", "w")
fmeta = open(tmpdir + "/meta.log", "w")

meta_info = meta.get_meta()

def git_hash(path):
    return subprocess.Popen(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                            stdout=subprocess.PIPE, cwd=path).stdout.read().rstrip()

hadrian_path = ghc_path + "/hadrian"

meta_info["ghc_hash"] = git_hash(ghc_path)
meta_info["hadrian_hash"] = git_hash(hadrian_path)

print("Running commands in " + hadrian_path + "...")

t1 = time.time()
p = subprocess.Popen([os.getcwd() + "/" + mode + ".sh"],
                     stdout=fout, stderr=ferr, cwd=hadrian_path,
                     shell=True)
ret = p.wait()
t2 = time.time()

fmeta.write(json.dumps(meta_info))

fout.close()
ferr.close()
fmeta.close()

now = datetime.datetime.now().isoformat()

if ret == 0:
    status = "success"
else:
    status = "failure"

filename = now + "%" + mode + "%" + str(t2 - t1) + "%" + status

copyfile(tmpdir + "/out.log", "../static/logs/" + filename + ".out.log")
copyfile(tmpdir + "/err.log", "../static/logs/" + filename + ".err.log")
copyfile(tmpdir + "/meta.log", "../static/logs/" + filename + ".meta.log")
