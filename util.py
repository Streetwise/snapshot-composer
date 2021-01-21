import json
import ast

def legend_reader(path):
    with open(path, 'r') as legend:
        document = json.load(legend)
        legend = document['views'][0]['spec']['legend']
    return legend

def translate(legend):
    custom_styles = [0 for x in range(len(legend))]
    for idx, leg in enumerate(legend):
        for k, v in leg.items():
            if k == 'label':
                custom_styles[idx]= (dict(label=v))
            elif k == 'fillColor':
                custom_styles[idx].update(fill='true', fillColor=v)
            elif k == 'fillOpacity':
               custom_styles[idx].update(fillOpacity=v)
            elif k == 'strokeColor':
               custom_styles[idx].update(stroke='true', strokeColor=v)
            elif k == 'strokeWidth':
               custom_styles[idx].update(weight=v)
            elif k == 'size':
                custom_styles[idx].update(radius=v)

    return custom_styles

def translate_marker(legend):
    custom_styles = [0 for x in range(len(legend))]
    for idx, leg in enumerate(legend):
        for k, v in leg.items():
            if k == 'label':
                custom_styles[idx]= (dict(label=v))
            elif k == 'fillColor':
                custom_styles[idx].update(fill='true')
                custom_styles[idx]['marker-color'] = v
                custom_styles[idx]['marker-size'] = "small"
                custom_styles[idx]['stroke-width'] = 0
                custom_styles[idx]['stroke-opacity'] = 0
                custom_styles[idx]['fill-opacity'] = 0.3
                # custom_styles[idx]['marker-symbol'] = "square"
                # custom_styles[idx]['bubblingMouseEvents'] = 'false'
            elif k == 'fillOpacity':
               custom_styles[idx].update(fillOpacity=v)
            elif k == 'strokeColor':
               custom_styles[idx].update(stroke='true', strokeColor=v)

    return custom_styles



def getting_dictionary(path):
    with open(path, 'r') as inFile:
        d = ast.literal_eval(inFile.read())
    return(d)
