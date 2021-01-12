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
      float(btl[0].strip()),
      float(btl[1].strip()),
      float(bbr[0].strip()),
      float(bbr[1].strip()),
    )
  else:
    return set(bounds)

def set_to_bounds(bounds):
  if bounds is None: return []
  if len(bounds) == 2 and bounds[0].startswith('geo:'): return bounds
  if len(bounds) < 4: raise Exception("Invalid bounds", bounds)
  print("setting", bounds)
  return ['geo:%f,%f' % (bounds[1], bounds[0]), 'geo:%f,%f' % (bounds[3], bounds[2])]

def points_reduce(filename, factor=2):
  data = gpd.read_file(filename)
  newgp = data.copy().iloc[::factor, :]
  newgp.reindex()
  newfile = "output/temp.reduced.geojson"
  print('Writing 1/%d reduced data to' % factor, newfile)
  newgp.to_file(newfile, driver='GeoJSON')
  return newfile

def html_geo_thumb(imgkey):
  return \
    ("<a target=\"_blank\" href=\"https://www.mapillary.com/map/im/%s\">" + \
    "<img style=\"width:200px\" " + \
    "src=\"https://images.mapillary.com/%s/thumb-320.jpg\"></a>") % \
    (imgkey, imgkey)
