##########
import json, ast, yaml
import geopandas as gpd
import pandas as pd
import numpy as np

from jinja2 import Environment, FileSystemLoader

from util import *

def generateDataPackage(output_from_parsed_template, name, geodata='test.json'):
  with open('output/%s/datapackage.yaml' % name, "w") as fh:
      fh.write(output_from_parsed_template)

  #####
  # Convert yaml to json datapackeg.json(metadata)

  with open("output/%s/datapackage.yaml" % name, 'r') as yaml_in, \
       open("output/temp.datapackage.json", "w") as json_out:
    yaml_object = yaml.safe_load(yaml_in) # yaml_object will be a
                                          #  list or a dict
    json.dump(yaml_object, json_out)


  ##########
  # Translate legend to styles (used fo styled_geojson)
  # Update custom styles, if not default
  ##########

  default_dict = getting_dictionary('template/default_dict.txt')
  custom_styles = translate(legend_reader('output/temp.datapackage.json'))
  custom_dict = []
  for i in range(len(custom_styles)):
    custom_dict.append({**default_dict[i], **custom_styles[i]})
  with open('template/output/custom_dict.txt', 'w') as custom:
    custom.write(str(custom_dict))

  #########
  # Preporcessing, creating categories according to the score
  ########

  # If there are values out of the interval <0,50> transform them
  gdf = gpd.read_file('data/%s' % geodata)
  gdf ['score'].mask(gdf ['score'] < 0, 0, inplace=True)
  gdf ['score'].mask(gdf ['score'] > 50, 50, inplace=True)

  #conditions = [(gdf ['score'] == 0), (gdf ['score'] == 1),(gdf ['score'] == 2),(gdf ['score'] == 3),(gdf ['score'] == 4),(gdf ['score'] == 5),(gdf ['score'] == 6),(gdf ['score'] == 7),(gdf ['score'] == 8),(gdf ['score'] == 9),(gdf ['score'] == 10), (gdf ['score'] == 11),(gdf ['score'] == 12),(gdf ['score'] == 13),(gdf ['score'] == 14),(gdf ['score'] == 15),(gdf ['score'] == 16),(gdf ['score'] == 17),(gdf ['score'] == 18),(gdf ['score'] == 19),(gdf ['score'] == 20), (gdf ['score'] == 21),(gdf ['score'] == 22),(gdf ['score'] == 23),(gdf ['score'] == 24),(gdf ['score'] == 25),(gdf ['score'] == 26),(gdf ['score'] == 27),(gdf ['score'] == 28),(gdf ['score'] == 29),(gdf ['score'] == 30), (gdf ['score'] == 31),(gdf ['score'] == 32),(gdf ['score'] == 33),(gdf ['score'] == 34),(gdf ['score'] == 35),(gdf ['score'] == 36),(gdf ['score'] == 37),(gdf ['score'] == 38),(gdf ['score'] == 39),(gdf ['score'] == 40), (gdf ['score'] == 41),(gdf ['score'] == 42),(gdf ['score'] == 43),(gdf ['score'] == 44),(gdf ['score'] == 45),(gdf ['score'] == 46),(gdf ['score'] == 47),(gdf ['score'] == 48),(gdf ['score'] == 49)]
  #values = [str(i) for i in range(50)]

  # create a list of our conditions
  conditions = [
    (gdf ['score'] <= 9),
    (gdf ['score'] > 9) & (gdf ['score'] <= 19),
    (gdf ['score'] > 19) & (gdf ['score'] <= 29),
    (gdf ['score'] > 29) & (gdf ['score'] <= 39),
    (gdf ['score'] > 40)
    ]
  # create a list of the values we want to assign for each condition
  #values = ['0', '1', '2', '3', '4']
  values = ['vey dangerous', 'dangerous', 'neutral', 'safe', 'very safe']

  gdf['category'] =  np.select(conditions, values)

  #########
  # Transformation of original json to create styled geojson
  ########

  ### Unique categories from DataFrame
  categories = values  # TO DO: 'category' instead of 'type'
  ### TO DO: whether use default_dict or custom_styles for styling
  d = getting_dictionary('template/output/custom_dict.txt')
  d = d[:5]
  ### Fill style values to the corresponding columns according to category
  masks = [gdf['category'] == cat for cat in categories]
  for k in d[0].keys():
    vals = [l[k] for l in d]
    gdf[k] = np.select(masks, vals, default=np.nan)

  gdf.to_file("output/temp.data.geojson", driver='GeoJSON')

  #####

  # Export engine, creates datapackage

  with open("output/temp.datapackage.json", 'r') as j, \
       open("output/temp.data.geojson", 'r') as l, \
       open("output/%s/datapackage.geojson" % name, 'w') as r:
     data = json.load(j)
     feed = json.load(l)
     data['resources'][0]['data']['features'] = feed['features']
     # data['views'][0]['spec']['legend'] = klop
     json.dump(data, r)
