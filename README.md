Snapshot composer
---

This collection of scripts prepares Data Packages (in the "Snapshots" format) for upload to the [Gemeindescan Web platform](https://github.com/cividi/spatial-data-package-platform/issues). Currently it is being used to publish the analytical results of the [Streetwise](https://github.com/streetwise) project for a number of municipalities, as detailed on the website https://streetwise.space

This repository has a `data` submodule with input sources specified by a template in YAML. Therefore make sure you check out the complete sources:

```
git clone https://github.com/Streetwise/snapshot-composer.git
cd snapshot-composer
git submodule update --init
```

## Usage notes

An input template YAML file (`template/*.yml`) specifies the metadata for each municipality we are publishing, as well as general style configurations for the legend and other content displayed.

For example, for the Safety campaign in Zürich the configuration looks like this:

```
- name: zurich
  geodata: safety_scores/zurich.json
  reduce_density: 100
  bounds: [47.41977, 8.46222, 47.33589, 8.61728]
```

- The **name** will specify the output filename and ID, displayed names and link to municipal IDs are currently configured by the user while uploading.
- Provide valid GeoJSON as **geodata**
- To improve performance use **reduce_density** to scale down the number of data points by a factor.
- To set the viewpoint and crop any outlier data points, use the **bounds** variable.

The `template/template.txt` file contains additional standard parameters, such as the license, to build the rest of the Data Package.

For configuration of the point rendering style, see `maputil.py`. For code that provides geographic transformation, see `geoutil.py`.

## Installation

The script depends on [GDAL](https://gdal.org/) which you would best install using your system packager, e.g. `yum install gdal-devel`

PyPROJ may also be required, installable via `python3-pyproj`

Install the rest of the environment with [Pipenv](https://pipenv.pypa.io/en/latest/):

```
pipenv --site-packages install
pipenv shell
```

or using pyvenv:

```
pyvenv .env --system-site-packages
. .env/bin/activate
pip install -r requirements.txt
```

And run the main script, providing the filename of the template as input:

```
$ python main.py template/safety.yml
```

If you have any questions, contact the Cividi team.

## License

[MIT License](LICENSE)
