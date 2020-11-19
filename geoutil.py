import geopandas as gpd
import tempfile

def bounds_to_set(bounds):
  if not isinstance(bounds, list):
    print('Unknown boundary format, ignoring')
    return None
  if bounds[0].startswith('geo:'):
    btl = bounds[0].strip('geo:').split(',')
    bbr = bounds[1].strip('geo:').split(',')
    return (
      float(btl[1].strip()),
      float(btl[0].strip()),
      float(bbr[1].strip()),
      float(bbr[0].strip()),
    )
  else:
    return set(bounds)

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
