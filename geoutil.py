import geopandas as gpd


def bounds_to_set(bounds):
    if not isinstance(bounds, list):
        print('Unknown boundary format, ignoring')
        return None
    if isinstance(bounds[0], str) and bounds[0].startswith('geo:'):
        btl = bounds[0].strip('geo:').split(',')
        bbr = bounds[1].strip('geo:').split(',')
        bounds = [
          float(btl[0].strip()),
          float(btl[1].strip()),
          float(bbr[0].strip()),
          float(bbr[1].strip()),
        ]
    # Thorben: "Safest bet currently: lower left, upper right corner notation."
    if bounds[0] > bounds[1]:
        bounds[0], bounds[1] = bounds[1], bounds[0]
        bounds[2], bounds[3] = bounds[3], bounds[2]
    if bounds[0] > bounds[2]:
        bounds[0], bounds[2] = bounds[2], bounds[0]
    if bounds[1] > bounds[3]:
        bounds[1], bounds[3] = bounds[3], bounds[1]
    return tuple(bounds)


def set_to_bounds(bounds):
    if bounds is None:
        return []
    if len(bounds) == 2 and bounds[0].startswith('geo:'):
        return bounds
    if len(bounds) < 4:
        raise Exception("Invalid bounds", bounds)
    print("setting", bounds)
    return [
        'geo:%f,%f' % (bounds[1], bounds[0]),
        'geo:%f,%f' % (bounds[3], bounds[2])]


def points_reduce(filename, factor=2):
    data = gpd.read_file(filename)
    newgp = data.copy().iloc[::factor, :]
    print('Original: %d - Reduced: %d' % (len(data), len(newgp)))
    newgp.reindex()
    newfile = "output/temp.reduced.geojson"
    print('Writing 1/%d reduced data to' % factor, newfile)
    newgp.to_file(newfile, driver='GeoJSON')
    return newfile


def html_geo_embed(imgkey):
    frame_code = "<iframe style='width:100%%;height:300px;border:0' " + \
        "src='https://www.mapillary.com/embed?" + \
        "map_style=Mapillary%%20streets" + \
        "&image_key=%s&style=photo'></iframe>"
    return frame_code % imgkey


def html_geo_thumb(imgkey):
    frame_code = "<img width='100%%' " + \
        "src='https://mapillary-proxy.vercel.app/thumb?key=%s' />"
    return frame_code % imgkey


def html_geo_frame(imgkey, score):
    frame_url = "https://www.mapillary.com/embed?image_key=%s" % imgkey
    return \
        "<a href='%s&style=classic'" % frame_url + \
        " target='mapillary'>" + \
        html_geo_thumb(imgkey) + \
        "</a>" + \
        "<div style='width:300px;text-align:center'>Streetwise Score: " + \
        "<b>%s</b></div>" % score
