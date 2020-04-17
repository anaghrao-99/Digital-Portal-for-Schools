import subprocess

import os

path = os.path.abspath(os.getcwd())
print(path)
subprocess.call('cd automated_correction_module', shell=True)
path = os.path.abspath(os.getcwd())
print(path)
pipe = subprocess.check_call(["python", "Prediction.py"] , cwd = path + '/automated_correction_module/classification/')

