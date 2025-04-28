#!/bin/bash

# Create HTML versions of the Markdown documentation files.
# Running this script just uses pandoc to write a HTML copy into a
# temporary directory where they can be viewed using a web browser.

# This text file supplies the $styles and $options.
source $HOME/public_html/css/pandoc.txt

if [ ! -d tmp ]; then
    mkdir tmp
fi

pandoc --css=$styles $options FAQ.md      > tmp/FAQ.html
pandoc --css=$styles $options README.md   > tmp/README.html
pandoc --css=$styles $options SECURITY.md > tmp/SECURITY.html
pandoc --css=$styles $options USAGE.md    > tmp/USAGE.html

pandoc --css=$styles $options --toc ../misc_scratch/ddc_scratch/TODO_Mikes.md > tmp/TODO_Mikes.html

pandoc --css=examples/styles.css $options examples/README_examples.md > tmp/README_examples.html

# Generate HTML of the test site.
#./ddc.py tmp > test.md
#pandoc --css=$styles --self-contained test.md > test.html

