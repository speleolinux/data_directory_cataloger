#!/bin/bash

# Create HTML versions of the Markdown documentation files.
# Running this script just uses pandoc to write a HTML copy into a
# temporary directory where they can be viewed using a web browser.

# In pandoc version 3 the option --self-contained is deprecated and is now a
# synonym for --embed-resources --standalone
# Pandoc will deprecate --self-contained in a future version.
pandoc_version=$(pandoc --version | head -1 | cut -d ' ' -f2)

# Note: Each options needs a space at the end.
if [[ "$pandoc_version" =~ ^2 ]]; then
    # This is pandoc version 2
    options="--self-contained "
elif [[ "$pandoc_version" =~ ^3 ]]; then
    # This is pandoc version 3
    options="--embed-resources --standalone "
else
    echo "This version of pandoc is not supported, exiting."
    exit 0
fi

# Note: Each options needs a space at the end.
options="$options --toc --toc-depth=2 "
options="$options --shift-heading-level-by=1 "

styles="css/styles.css"

# Create tmp directory if it does not exist.
if [ ! -d tmp ]; then echo "Creating directory tmp"; mkdir tmp; fi

echo "Converting Markdown docs to HTML pages ..."
pandoc --css=$styles $options README.md   > tmp/README.html
pandoc --css=$styles $options FAQ.md      > tmp/FAQ.html
pandoc --css=$styles $options SECURITY.md > tmp/SECURITY.html
pandoc --css=$styles $options USAGE.md    > tmp/USAGE.html
pandoc --css=examples/styles.css $options examples/README_examples.md > tmp/README_examples.html

echo "HTML versions of the docs have been written to the tmp/ directory."

