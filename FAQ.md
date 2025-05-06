---
title: FAQ
toc: true
include-before: |
  <a name="top"></a>
  [README](README.html) &nbsp;
  FAQ &nbsp;
  [USAGE](USAGE.html) &nbsp;
  [SECURITY](SECURITY.html)
---

# Why does this script not recurse?

The `ddc.py` script only looks for README.yaml files in the immediate subdirectories.

The purpose of this script is to manage large amounts of data. There might be
hundreds of directories. The directories might contain thousands of files.
We don't want to unexpectedly find that this script takes hours to run and is
consuming lots of I/O bandwidth. If you wish to run this script on many
subdirectories you can write a bash script to do this.

# Why use plain text README.yaml files? A database is faster.

A database would put all the metadata in one place - inside the database.
The metadata would then no longer be with the data it describes. If the data is
moved then the connection with the data is broken. You would need to update the
database.

# What happens if this script can no longer run?

Python changes and this script might not run with Python 4 or later.

If you cannot run this script anymore nothing really breaks.
Future data owners or data managers will see be able to find and understand the data's
metadata because:

- The README.yaml files will still remain with the data in their directories.
- The generated markdown files will readable.
- The static web pages are still likely to be readable with any HTML browser even 
  if they are not being served by a web server.

