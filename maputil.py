import json
import ast

def legend_reader(path):
    with open(path, 'r') as legend:
        document = json.load(legend)
        legend = document['views'][0]['spec']['legend']
    return legend


def translate_marker(legend, as_circle=False):
    custom_styles = [0 for x in range(len(legend))]
    for idx, leg in enumerate(legend):
        for k, v in leg.items():
            if not isinstance(custom_styles[idx], dict):
                custom_styles[idx] = dict()
            if k == 'label':
                custom_styles[idx].update(label=v)
            elif k == 'fillColor':
                custom_styles[idx].update(fill='true')
                if not as_circle:
                    # https://github.com/mapbox/simplestyle-spec/tree/master/1.1.0
                    custom_styles[idx]['marker-color'] = v
                    custom_styles[idx]['marker-size'] = "small"
                    # custom_styles[idx]['marker-symbol'] = "square" # https://labs.mapbox.com/maki-icons/
                    custom_styles[idx]['stroke-width'] = 0
                    custom_styles[idx]['stroke-opacity'] = 0
                else:
                    custom_styles[idx]['color'] = v
                    custom_styles[idx]['fillColor'] = v
                    custom_styles[idx]['fill-opacity'] = 0.3
                    custom_styles[idx]['radius'] = "30.0"
                    custom_styles[idx]['bubblingMouseEvents'] = "true"
            elif k == 'fillOpacity' and as_circle:
                custom_styles[idx].update(fillOpacity=v)
            elif k == 'strokeColor' and as_circle:
                custom_styles[idx].update(stroke='true', strokeColor=v)

    return custom_styles


def getting_dictionary(path):
    with open(path, 'r') as inFile:
        d = ast.literal_eval(inFile.read())
    return(d)
