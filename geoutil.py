import geopandas as gpd
import tempfile

def points_reduce(filename, factor=2):
  data = gpd.read_file(filename)
  newgp = data.iloc[::factor, :]
  newgp.reindex()
  # print(data.head())
  # print(newgp.head())
  # newfile = tempfile.mkstemp('.geojson')[1]
  newfile = "output/temp.reduced.geojson"
  print('Writing reduced data to', newfile)
  newgp.to_file(newfile, driver='GeoJSON')
  return newfile
