#!/bin/bash

# This is an example script showing how to use the Data Directory Cataloger
# to process several directories, creating a Markdown file for each directory. 
# Then combine those Markdown files into a single web site using the static
# website generator MkDocs and perhaps, upload the site.
#
# Usage: ./update_uts_site_example.sh

# These settings might be required depending on your terminal.
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# Create directory docs if it does not exist.
if [ ! -d docs ]; then mkdir docs; fi

# Catalog the README.yaml files under the following directories.
./ddc.py /shared                            > docs/shared.md
./ddc.py /shared/eresearch                  > docs/shared_eresearch.md
./ddc.py /shared/eresearch/pbs_job_examples > docs/shared_eresearch_pbs_job_examples.md
./ddc.py /shared/opt                        > docs/shared_opt.md
./ddc.py /shared/c3                         > docs/shared_c3.md

# Build the website. It will be created within the directory "site".
# You can also use "mkdocs serve" to view a static website at localhost.
# You will need to have created a Python 3 virtual environment called "mkdocs" first.
# Then installed MkDocs within that Python environment.
source ~/virtualenvs/mkdocs/bin/activate
mkdocs build

# Rsync the "site" directory to your website directory.
# If you wish to use --delete do not use "site/*" use "site/". Man rsync for why.
# Uncomment this to upload to your site if its under /var/www/html/
#rsync -r --delete site/ /var/www/html/

