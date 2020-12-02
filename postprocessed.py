#!/usr/bin/python
import subprocess
import os
curr = os.getcwd()
path = curr + '/output'
items = [ name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
for item in items:
    os.chdir(path + '/' + item)
    subprocess.call(["sed 's/markercolor/marker-color/g' datapackage.json >> final.json"], shell=True)
