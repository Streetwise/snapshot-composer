##########
##########
import json, ast, yaml, os
import geopandas as gpd
import pandas as pd
import numpy as np

from jinja2 import Environment, FileSystemLoader

from generator import generateDataPackage

#####
### Generation of .yaml file from template.txt and data_to_feed.yaml
# data_to_feed.yaml, input from user
# generated .yaml file is to be used for datapackage

# Load input from user
config_data = yaml.load(open('template/data_to_feed.yml'), Loader=yaml.FullLoader)
env = Environment(loader = FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)

# Load template
template = env.get_template('template/template.txt')

# Render input to template
output_from_parsed_template=(template.render(config_data))

# Save generated .yaml file
for location in config_data['locations']:
    name = location['name']
    filename = location['geodata']
    try:
        os.mkdir('output/%s' % name)
    except FileExistsError:
        pass
    generateDataPackage(output_from_parsed_template, name, filename)
