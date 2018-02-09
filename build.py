import os
import time
import subprocess
import gossip_pb2

def call(args):
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    return str(p.stdout.read(), "utf-8").strip()

def gcc_version():
    return call(["gcc", "-dumpversion"])

def ghc_version():
    ret = call(["ghc", "--version"])
    return ret.split("version ")[1]

def get_build(ip, port, toolnames, revision, log):
    start_time = time.time()
    time.sleep(5)
    end_time = time.time()

    build = gossip_pb2.AddBuildRequest()
    build.node = ip + ":" + str(port)
    build.uname = ' '.join(os.uname())
    toolchains = []
    for tool in toolnames:
        if tool == "gcc":
            toolchains.append("gcc-" + gcc_version())
        elif tool == "ghc":
            toolchains.append("ghc-" + ghc_version())
    build.toolchain = ','.join(toolchains)
    build.revision = revision
    build.start_time = int(start_time * 1000000)
    build.end_time = int(end_time * 1000000)
    build.log = log
    build.status = 0
    return build
