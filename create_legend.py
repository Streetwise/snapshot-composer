#####
# Input: palette and one exemplary dictionary (e.g. from defualt dictionary).
# It creates list of N dictionaries, then it would be updated with customized palette.
# In this example, our exemplary dictionary is "l", colors is our palette. 
#####
import ast

l = [{'label': '0', 'size': '3.0', 'shape': 'circle', 'primary': 'false', 'fillColor': '#f52900', 'fillOpacity': 0.7, 'strokeColor': '#232323', 'strokeWidth': 1.0, 'strokeOpacity': 1.0}]
colors = ['#f30000', '#f30a00', '#f41400', '#f41f00', '#f52900', '#f53300', '#f63d00', '#f64700', '#f75200', '#f75c00', '#f86600', '#f87000', '#f97a00', '#f98500', '#fa8f00', '#fa9900', '#fba300', '#fbad00', '#fcb800', '#fcc200', '#fdcc00', '#fdd600', '#fee000', '#feeb00', '#fff500', '#ffff00', '#f5ff00', '#eaff01', '#e0ff01', '#d5ff02', '#cbff02', '#c1ff02', '#b6ff03', '#acff03', '#a1ff03', '#97ff04', '#8cff04', '#82ff05', '#78ff05', '#6dff05', '#63ff06', '#58ff06', '#4eff06', '#44ff07', '#39ff07', '#2fff08', '#24ff08', '#1aff08', '#0fff09', '#05ff09']
# List of N dictionaries, N-1 = 49 
for i in range(5):
    l.append(l[0])
# Create list of palette dictioneries
farby = ['#f30000', '#f97a00', '#ffff00', '#82ff05', '#05ff09']
colors_dict = [{'fillColor':farby[i]} for i in range(5)]
values =  [{'label':v} for v in ['very dangerous', 'dangerous', 'neutral', 'safe', 'very safe']]
# Create legend with cutomzied palette
legend = [{**l[i], **colors_dict[i]} for i in range(5)]
legend = [{**legend[i], **values[i]} for i in range(5)]
#with open('legend_palette.txt.', 'w') as palette:
#     palette.write(legend)
#print(str(legend).replace('false', false))
# legend je nasa vysnivana legenda, treba vlozit do data_to_feed.yml
# sed "s/'false'/false/g"
