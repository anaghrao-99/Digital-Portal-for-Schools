import subprocess

import os

# path = os.path.abspath(os.getcwd())
# print(path)
# subprocess.call('cd automated_correction_module', shell=True)
# path = os.path.abspath(os.getcwd())
# print(path)
# pipe = subprocess.check_call(["python", "Prediction.py"] , cwd = path + '/automated_correction_module/classification/')

file = open('marks.txt', "r")
counter = 0
for line in file:
	if(counter > 1):
		break
	if(counter == 0):
		files = line[1:len(line)-2].split(',')

	if(counter == 1):
		marks = line[2:len(line)-2].split()


	counter += 1

print(files)
print(marks)