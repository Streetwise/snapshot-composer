##########
import json, ast, yaml

import geopandas as gpd
import pandas as pd
import numpy as np

from maputil import (
  legend_reader, translate_marker, getting_dictionary
)
from geoutil import (
  points_reduce, bounds_to_set, set_to_bounds, html_geo_thumb
)

def generateDataPackage(output_from_parsed_template, location, config_data):
  name = location['name']
  geodata = 'data/%s' % location['geodata']

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
  dpp_legend = legend_reader('output/temp.datapackage.json')
  if 'as_circle' in config_data:
    custom_styles = translate_marker(dpp_legend, True)
  else:
    custom_styles = translate_marker(dpp_legend)

  # Prepare style dictionary
  custom_dict = []
  for i in range(len(custom_styles)):
    custom_dict.append({**default_dict[i], **custom_styles[i]})
  with open('output/temp.custom_dict.txt', 'w') as custom:
    custom.write(str(custom_dict))

  #########
  # Optimization steps
  #########

  if 'reduce_density' in location:
    if not isinstance(location['reduce_density'], int):
      print("Reducing density by default to one half")
      location['reduce_density'] = 2
    # Optimizes the GeoJSON, returns a new (temporary) filename
    geodata = points_reduce(geodata, location['reduce_density'])

  #########
  # Preprocessing, creating categories according to the score
  ########

  # Read and optionally apply bounding box
  bbox = None
  if 'bounds' in location:
    bbox = bounds_to_set(location['bounds'])
    print('Cropping data to bounds', bbox)
    gdf = gpd.read_file(geodata, bbox=bbox)
  else:
    gdf = gpd.read_file(geodata)

  # If there are values out of the interval <0,50> transform them
  gdf['score'].mask(gdf['score'] < 0, 0, inplace=True)
  gdf['score'].mask(gdf['score'] > 50, 50, inplace=True)

  gdf['description'] = ["%s<br>Streetwise Score: %s" % (html_geo_thumb(gdf['name'][i]), gdf['score'][i]) for i in range(len(gdf))]

  # create a list of our conditions
  conditions = [
    (gdf['score'] <= 9),
    (gdf['score'] > 9) & (gdf['score'] <= 19),
    (gdf['score'] > 19) & (gdf['score'] <= 29),
    (gdf['score'] > 29) & (gdf['score'] <= 39),
    (gdf['score'] >= 40)
    ]

  # list of the values we want to assign for each condition
  legend_labels = [v['label'] for v in config_data['legend']]
  legend_values = [ix for ix in range(0, len(config_data['legend']))]

  # set the category frame based on conditions and values above
  if len(conditions) != len(legend_values):
    print("Mismatch in data (%d) and legend (%d) value steps!" %
      (len(conditions), len(legend_values)))
    exit()
  gdf['category'] = np.select(conditions, legend_values)
  gdf['label'] = np.select(conditions, legend_labels)

  #########
  # Transformation of original json to create styled geojson
  ########

  ### Unique categories from DataFrame
  ### TODO: consider using default_dict or custom_styles for styling
  d = getting_dictionary('output/temp.custom_dict.txt')
  d = d[:5]

  ### Fill style values to the corresponding columns according to category
  masks = [gdf['category'] == cat for cat in legend_values]
  for k in d[0].keys():
    vals = [l[k] for l in d]
    gdf[k] = np.select(masks, vals, default=np.nan)

  ### Write styled GeoJSON to file
  gdf.to_file("output/%s/preview.geojson" % name, driver='GeoJSON')
  #####

  ### Boundary settings

  # Set final viewport
  if 'viewport' in location and location['viewport']:
    bbox = bounds_to_set(location['viewport'])
    print('Using preset viewport')

  # Calculate viewport if it is missing
  if bbox is None:
    minx, miny, maxx, maxy = gdf.geometry.total_bounds
    bbox = [minx, miny, maxx, maxy]
    print('Calculated geometry bounds', bbox)

  # Convert to geo: format
  bbox = set_to_bounds(bbox)

  #####

  # Export engine, creates datapackage
  with open("output/temp.datapackage.json", 'r') as j, \
       open("output/%s/preview.geojson" % name, 'r') as l, \
       open("output/%s/datapackage.json" % name, 'w') as r:
     data = json.load(j)
     feed = json.load(l)
     data['views'][0]['spec']['bounds'] = bbox
     data['resources'][0]['data']['features'] = feed['features']
     if 'as_circle' in config_data:
       data['resources'][0]['mediatype'] = "application/vnd.simplestyle-extended"
     json.dump(data, r)
