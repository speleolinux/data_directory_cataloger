#!/bin/bash

# This will automatically update the site directory from the contents of the
# docs directory. It will read mkdocs.yml for configuration information and
# run a webserver on port 8080 to show this site..
# You need to have already created the mkdocs virtual environment below.
# You also need to run this script from within the science_site directory.

source ~/virtualenvs/mkdocs/bin/activate
mkdocs serve -a localhost:8080

