#!/usr/bin/env python3
import os
import yaml
import click

@click.command()
@click.argument('filename')
def generator(filename):
    """ Generates geospatial Data Packages """
    from generator import generateDataPackage
    from jinja2 import Environment, FileSystemLoader

    # Load input from user
    config_data = yaml.load(open(filename), Loader=yaml.FullLoader)
    env = Environment(loader = FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)

    # Load template
    template = env.get_template('template/template.txt')

    # Render input to template
    output_from_parsed_template=(template.render(config_data))

    # Save generated .yaml file
    for location in config_data['locations']:
        name = location['name']
        filename = location['geodata']
        print("Processing location %s from %s" % (name, filename))
        try:
            os.mkdir('output/%s' % name)
        except FileExistsError:
            pass
        generateDataPackage(output_from_parsed_template, location)


if __name__ == '__main__':
    generator()

# this needs to be done for every datapackage
# sed 's/markercolor/marker-color/g' datapackage.json >> final.json