# README

This is the Data Directory Cataloger. The purpose of it is to help manage
numerous directories by having a README.yaml in most directories and which
stores metadata about the contents of that directory. Typical metadata that
you would store might be "Description", "Data Manager" and "Disposal Date".

This was developed for the Australian Speleological Federation to assist them
in managing their AWS S3 buckets of data. It's also currently being trialled
by Mike Lake for a data store at the University of Technology Sydney.

When the `ddc.py` program is run on a directory it looks for `README.yaml` files
in the **immediate** subdirectories. From those `README.yaml` files it reads the
metadata, and outputs a single Markdown document listing each subdirectory and
summarising the metadata in its README.
This Markdown doc can then be easily transformed to a HTML file (e.g. using `pandoc`)
which will provide a single point of information about the contents of the directories.

The real advantages of the program though are realised when multiple top level
directories are cataloged and the Markdown docs combined into a static website
which then describes the multiple top-level directories. 

Also System Administrators can look in the subdirectories and will find the `README.yaml` 
files which describe the data and who manages it. The README.yaml files can be also 
be programatically searched for metadata such as the data manager or data disposal
dates.

See the [Examples Readme](examples/README_examples.md) for a example HTML page and a screenshot.

## Requirements

Python 3.6.8 or later with PyYAML 6.0 is required for the basic `ddc.py` program.
The `write_readmes.py` program does not require any extra Python modules.

If you wish to create a MkDocs site then you will need to install the `mkdocs` module
and perhaps a module for whatever theme you wish to use. For instance I have the 
following mkdocs modules installed:

    mkdocs==1.3.1
    mkdocs-macros-plugin==0.7.0
    mkdocs-material==8.4.2

It is best to install these into a Python virtual environment which can be sourced
before running the programs. See the script `update_site_example.sh` as an example.

## License

Copyright 2022 Mike Lake     

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
the Data Directory Cataloger. If not, see http://www.gnu.org/licenses/.

Mike Lake

