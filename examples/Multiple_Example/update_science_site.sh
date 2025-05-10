#!/bin/bash

# Create a catalog of a multiple directories as an example
# of an entire site's data being cataloged.

#################################
# Settings that can be configured
#################################

data_dir="science"      # The directory to read.
site_dir="science_site" # The directory to write the Markdown files into.

# Location of the Python virtual environment that provides the 
# MkDocs static website generator.
# This directory should contain the "bin/activate" script.
# Do not add a trailing slash at the end of this location.
virt_env="$HOME/virt_environments/mkdocs"

ddc="../../ddc.py"      # Where to find the DDC program.

#############################
# Check for missing stuff etc
#############################

# Check this script is being run from the "Multiple_Example" directory.
PWD=$(pwd)
if [ ${PWD##*/} != 'Multiple_Example' ]; then
    echo "This script needs to be run from within the \"Multiple_Example\" directory."
    echo "Exiting"
    exit 0
fi

# Check we have the virtual env to activate.
if [ -d $virt_env ]; then
    source "${virt_env}/bin/activate"
else
    echo "Cannot find directory $virt_env"
    echo "This should be a Python virtual environment with MkDocs installed."
    echo "Exiting"
    exit 0    
fi

# Finally check we now have a mkdocs command found.
which mkdocs > /dev/null 2>&1
if [ "$?" -ne 0 ]; then
    echo "Cannot find the mkdocs command: ${virt_env}/bin/mkdocs"
    echo "Exiting"
    exit 0
fi

###########################
# We should be good to go !
###########################

echo ""
echo "=== Creating Multipage Example Site ==="

echo "Found these README files under ${data_dir}:"
find $data_dir -name README.yaml | sed 's/^/  /'

echo "Running ddc.py to collate their contents into $site_dir/docs/"
# The docs directory will already contain a standard index.md and
# an about.md file. The commands below will add Markdown files
# using information from the README.yaml files found.
$ddc $data_dir           > $site_dir/docs/science.md
$ddc $data_dir/astronomy > $site_dir/docs/astronomy.md
$ddc $data_dir/biology   > $site_dir/docs/biology.md
$ddc $data_dir/geology   > $site_dir/docs/geology.md
$ddc $data_dir/physics   > $site_dir/docs/physics.md

echo "Using MkDocs to build site ..."
pushd $site_dir > /dev/null
# The site will be built using the mkdocs.yml in this directory.
# The sed just removes any leading "INFO" string. 
mkdocs build 2>&1 | sed 's/INFO\s*/  /'
popd > /dev/null

echo ""
echo "You should now be able to view $site_dir/site/index.html in a web browser."
echo ""
echo "If you are running the local MkDocs server it will have automatically updated"
echo "the science site at http://localhost:8080/"
echo ""

