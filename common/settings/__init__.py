import os
import json

# read actual file path
file_path = os.path.dirname(os.path.realpath(__file__))
# read files in the folder
content = os.listdir(file_path)
# set working directory to file path: like cd folder/..
os.chdir(file_path)

for file in content:
    ending = os.path.splitext(file)[1]
    constant_name = os.path.splitext(file)[0].upper()

    if ending == ".json":
        with open(file) as content:
            dictionary = json.load(content)
            # set the uppercase name of the file as the name of
            # the constant that carries the json content of that file
            globals()[constant_name] = dictionary
