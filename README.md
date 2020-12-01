##### Streetwise snapshots builder for Gemeindescan


The file "test.json" is sample of input geodata with some attributes (here is one attribute named "score").

The file input YAML file (.yml) needs to be filled, regarding metadata information and style.

To use the builder, install the environment:

```
pyvenv .env
. .env/bin/activate
pip install -r requirements.txt
```

And run the main script, providing the filename of the input:

```
$ python main.py template/safety.yml
```

## Sample configuration

Here is an example configuration for a Zürich dataset:

```yaml
name: "Streetwise: Safety"
title: "Safety scores"
description: "Relative visual perception of urban spaces"
is_showcase: "false"
keywords: ["Streetwise", "Safety", "Urban" ]
maintainers_web_github: "https://github.com/streetwise"
maintainers_name: "Streetwise team"
legend: [{'label': 'Unsafe', 'size': 3.0, 'shape': 'circle', 'primary': false, 'fillColor': '#f30000', 'fillOpacity': 0.7, 'strokeColor': '#232323', 'strokeWidth': 1.0, 'strokeOpacity': 1.0}, {'label': 'Neutral', 'size': 3.0, 'shape': 'circle', 'primary': false, 'fillColor': '#ffff00', 'fillOpacity': 0.7, 'strokeColor': '#232323', 'strokeWidth': 1.0, 'strokeOpacity': 1.0}, {'label': 'Safe', 'size': 3.0, 'shape': 'circle', 'primary': false, 'fillColor': '#05ff09', 'fillOpacity': 0.7, 'strokeColor': '#232323', 'strokeWidth': 1.0, 'strokeOpacity': 1.0}]
locations:
  - name: zurich
    geodata: zurich_test.geojson
    bounds: ["geo:45.15, 5.967", "geo:52.883, 12.467"]
    reduce_density: 2
```
