#!/bin/bash

# This takes the example.md Markdown document and converts it to a HTML page.
# This requires pandoc. It also requires a styles.css to be in this directory.
# The --embed-resources option inserts the styles into the head of the doc.
# Hence it will not require the separate styles.css file to be present.

pandoc --css=styles.css --embed-resources --standalone example.md > example.html

