# meta information about the build
# JSON format

import psutil
import subprocess
import platform

def get_meta():
	ghc_version = subprocess.Popen(["ghc", "--numeric-version"], stdout=subprocess.PIPE).stdout.read().rstrip()
	gcc_version = subprocess.Popen(["gcc", "-dumpversion"], stdout=subprocess.PIPE).stdout.read().rstrip()
	return {
		"cpu_count" : psutil.cpu_count(),
		"memory" : str(float(psutil.virtual_memory().total) / 1024 / 1024 / 1024) + " GB",
		"platform" : platform.platform(),
		"ghc_version": ghc_version,
		"gcc_version": gcc_version
	}
