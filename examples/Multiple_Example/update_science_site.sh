#!/bin/bash

# Create a catalog of a multiple directories as an example
# of an entire site's data being cataloged.

data_dir="science"      # The directory to read.
site_dir="science_site" # The directory to write the Markdown files into.

ddc="../../ddc.py"      # Where to find the DDC program.

# Check this script is being run from the "Multiple_Example" directory.
PWD=$(pwd)
if [ ${PWD##*/} != 'Multiple_Example' ]; then
    echo "This script needs to be run from the tests directory. Exiting."
    exit
fi

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
source ~/virt_environments/mkdocs/bin/activate
pushd $site_dir > /dev/null
# The site will be built using the mkdocs.yml in this directory.
mkdocs build 2>&1 | sed 's/INFO//'
popd > /dev/null

echo ""
echo "You should now be able to view $site_dir/site/index.html in a web browser."
echo ""
echo "If you are running the local MkDocs server it will have automatically updated"
echo "the science site at http://localhost:8080/"
echo ""

