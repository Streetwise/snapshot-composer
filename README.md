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
