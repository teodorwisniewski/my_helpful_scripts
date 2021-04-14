import glob
import re
import os

script_name = os.path.basename(__file__)

print(f"Starting the script {script_name}")
for filename in glob.glob('*.*'):
    flag = re.findall(r"[^a-zA-Z0-9\.\_]",filename)
    if flag:
        new_file_name =  re.sub('[^a-zA-Z0-9\.\_]', '_', filename)
        os.rename(filename,new_file_name)
        print(f"I have just renamed a file from  called {filename} to {new_file_name}")

print(f"The end {script_name}")