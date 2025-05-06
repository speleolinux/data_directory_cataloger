---
title: Usage
toc: true
include-before: |
  <a name="top"></a>
  [README](README.html) &nbsp; 
  [FAQ](FAQ.html) &nbsp;
  USAGE &nbsp; 
  [SECURITY](SECURITY.html)
---


This covers some details on how you would use the Data Directory Cataloger to manage
a collection of data directories. In this example I'm using my `hpc_examples` directory.
This contains example scripts for a High Performance Computer cluster.

<!--
* [What a README.yaml Looks Like](#what-a-readmeyaml-looks-like)
* [Writing your Initial README.yaml Files](#writing-your-initial-readmeyaml-files)
* [How to run the DDC Program](#how-to-run-the-ddc-program)
* [Sections in the Markdown Document Output](#sections-in-the-markdown-document-output)
* [Other Metadata Fields One Could Use](#other-metadata-fields-one-could-use)
* [Looking at README.yaml Files](#looking-at-readmeyaml-files)
* [Adding a Field](#adding-a-field)
* [Removing a Field](#removing-a-field)
* [Modifying a Field](#modifying-a-field)
* [Disallowed Characters](#disallowed-characters)
-->

# What a README.yaml Looks Like

Example: `/shared/opt/fastqc-0.10.1/README.yaml`

    Title: FastQC is a high throughput sequence QC analysis tool
    Description: FastQC reads a set of sequence files and produces a quality control report.
    Data Manager: Mike Lake
 
In each subdirectory the README.yaml keys are metadata fields and their values
describe the contents of the subdirectory.
The keys used in the YAML should be named the same as what is available in any
Data Management Plans that you may be using.

The README.yaml files should contain the same metadata fields for each subdirectory 
*at the same level*. The idea being is that each subdirectory at a given level are 
in some way related and would have the same required metadata fields. The DDC program
looks at all the keys and if any README.yaml file is missing a key then that is
flagged as a warning that a metadata field might be missing.

The README.yaml should be in StrictYAML format (https://github.com/crdoconnor/strictyaml).

# Writing your Initial README.yaml Files 

This short script can save a lot of time by writing a README.yaml
file into each of the immediate subdirectories of a top level directory.
The text of the README.yaml file that will be written is in the script. 
You need to edit it to change the text. Read the script.

    $ ./write_readmes.py top_level-directory [-t | --test]

# How to run the DDC Program

Get brief help on the program:

    $ ./ddc.py -h

Run the program on a single "top level" directory to find and parse the README.yaml
files in the immediate subdirectories of that directory. For example our 
`/shared/opt` directory contains a dozen subdirectories containing scientific software,
and each of those directories contain a README.yaml file.

    $ ./ddc.py /shared/opt

or

    $ cd /shared/opt
    $ /pathto/ddc.py .

It will print a single Markdown document containing the metadata in the READMEs. 

We actually need to save this output so it can be converted to a HTML page so
redirect it to a file:
    
    $ ./ddc.py /shared/opt > CATALOG.md

Now you can use a utility like `pandoc` to convert the Markdown to a HTML page:

    $ pandoc --css=styles.css --self-contained CATALOG.md > CATALOG.html

See the examples directory in this repo for an example of running this on our
`/shared/opt/` directory. This also contains an example `styles.css` file.

Of course most users will have many directories to manage. A better option is to
run a bash script that runs this script over those directories, and combining the
Markdown docs into a website using a static site generator like MkDocs 
https://www.mkdocs.org. A short example of such a script is included `update_site_example.sh` 
and an example mkdocs configuration file `mkdocs_example.yml`.

# Sections in the Markdown Document Output

The "**Summary**" section of the Markdown document will summarize *some* of the metadata fields.
This will always show the *Directory* that each README.yaml file was found in. 
Not all README metadata fields will be shown. We show just the fields that are likely be
useful to users. You can add other metadata fields if you wish by editing the program,
see `columns = ['Title', 'Description', 'Data Manager']`.

The "**Metadata Information**" section will contain a list of *all* the metadata fields
found in the READMEs for this level of subdirectories.
This section is more likely to be used by administrators wanting to know what metadata
can be found in the READMEs. You can have any number of fields. Just make sure that
each subdirectory at the same level has the same fields.

A "**Metadata Warnings**" section will be shown at the top of the page if there are
README.yaml files that are possibly missing a metadata field, or if a
subdirectory is missing a README.yaml file.

# Other Metadata Fields One Could Use

* Maintainer:
* Provenance: Downloaded from xxx on 2020.01.01
* RDMP link:
* Data retention and disposal:
* Minimum retention period:

# Looking at README.yaml Files

Find all the README.yaml files under just the immediate subdirectories.
The `-mindepth 2` is added to the find command so it will not pick up
any README in the current directory.

    $ find . -mindepth 2 -maxdepth 2 -name README.yaml
    ./job_arrays/README.yaml
    ./mpi/README.yaml
    ./primes/README.yaml

This is how to quickly look at all the README.yaml files under the immediate subdirectories.

    $ for f in `find . -mindepth 2 -maxdepth 2 -name README.yaml`; do echo "$f"; cat $f | sed 's/^/   /'; done
    ./job_arrays/README.yaml
       Title: PBS Job Arrays
       Description: 
       Data Manager: Mike Lake
    ./mpi/README.yaml
       Title: HPC Job Examples for MPI
       Description: HPC Job Examples for MPI
       Data Manager: Mike Lake
       Earliest possible disposal date: 2024
    ./primes/README.yaml
       Title: PBS Primes
       Description: Example of submitting a primes job via PBS
       Data Manager: Mike Lake

To see what README.yaml files just contain the field "Earliest possible disposal date"
in a compact manner we can use:

    $ for f in `find . -mindepth 2 -maxdepth 2 -name README.yaml`; do echo -n "$f  "; cat $f | grep Earliest || echo ''; done
    ./job_arrays/README.yaml
    ./mpi/README.yaml  Earliest possible disposal date: 2024
    ./primes/README.yaml

# Adding a Field

We can see from the output of the script below that most of my README.yaml
files are missing the "Earliest possible disposal date" field. I'd like to
append this to the files that are missing this field.

    hpc_examples/$ for f in `find . -maxdepth 2 -name README.yaml`; do echo -n "$f  "; cat $f | grep disposal || echo ''; done
    ./.git/README.yaml  
    ./primes/README.yaml  
    ./job_arrays/README.yaml  
    ./mpi/README.yaml  Earliest possible disposal date: 2024
    ./profiling/README.yaml  
    ./checkpointing_dmtcp/README.yaml  
    ./overtime/README.yaml  
    ./cuda/README.yaml  
    ./README.yaml  Earliest possible disposal date: 2024
    ./matlab/README.yaml  

*Well there is a script to do that for you!* &nbsp; Under `useful_scripts` you will find
`ddc_field_add.sh`. Edit that and insert into there the string that you wish to
add.

Make sure you change into the top level directory above the subdirectories that
need their README.yaml files changed:

    $ cd hpc_examples
    hpc_examples$

Run it:

    hpc_examples$ path_to/ddc_field_add.sh 
    Added to ./.git/README.yaml
    Added to ./primes/README.yaml
    Added to ./job_arrays/README.yaml
    Added to ./profiling/README.yaml
    Added to ./checkpointing_dmtcp/README.yaml
    Added to ./overtime/README.yaml
    Added to ./cuda/README.yaml
    Added to ./matlab/README.yaml

Done. If you run it again nothing will be changed.

    hpc_examples$ path_to/ddc_field_add.sh 
    $ 

# Removing a Field

*Well there is also a script to help you do this!* &nbsp; Under `useful_scripts` you
will find `ddc_field_remove.sh`. Edit that and insert into there the string
that you wish to remove.

Here is an example:

Many of my READMEs have a field that is not required, and in fact conflics with another field.
I wish to remove the field "Minimum retention period".

    ./pbs_manuals/README.yaml
      Title: Copies of the PBS Manuals for Users
      Description: Contains copies of the PBS manuals which users can download.
      Data Manager: Mike Lake
      Minimum retention period: 2 years        <== We wish to remove this line.
      Earliest possible disposal date: 2024

First though check how many READMEs have this line.
Change into the top level directory above the subdirectories.

    $ cd hpc_examples
    hpc_examples$

Of the 7 READMEs, 6 of them have the field that I wish to remove.

    $ for f in `find . -maxdepth 2 -name README.yaml`; do echo -n "$f  "; cat $f | grep retention || echo ''; done
    ./README.yaml
    /ansys/README.yaml  Minimum retention period: 1 years
    ./hpc_users/README.yaml  Minimum retention period: 2 years
    ./singularities/README.yaml  Minimum retention period: 2 years
    ./pbs_logs/README.yaml  Minimum retention period: 2 years
    ./pbs_job_examples/README.yaml  Minimum retention period: 2 years
    ./pbs_manuals/README.yaml  Minimum retention period: 2 years
    $

First backup the READMEs. The command below will create a tarball of them.
After the editing, if all is OK, we can remove this backup.

    $ tar cvf README_backups.tar `find . -maxdepth 2 -name README.yaml`

Now we can do the fix for all the README files! Edit `ddc_field_remove.sh` and set
`remove='Minimum Retention Period'`

Check your in the top level directory, above the subdirectories that contain the
READMEs that you wish to change. Run the script. There should be no output if all
goes OK. No harm done if you accidentally run it again, nothing will be changed.

    hpc_examples$ path_to/ddc_field_remove.sh
    hpc_examples$

Now just repeat the command that printed the READMEs and check they all look OK.

    $ for f in `find . -mindepth 2 -maxdepth 2 -name README.yaml`; do echo -n "$f  "; cat $f | grep retention || echo ''; done

If you are certain that all is OK then you can now remove the `README_backups.tar`.

# Modifying a Field

*Yes, there is a script to help you do this!*

Under `useful_scripts` you will find `ddc_field_modify.sh`. Edit that and
set there the strings that you wish to modify.

Make sure you change into the top level directory above the subdirectories that
need their README.yaml files modified. 

Make a backup as shown above, then run the script.

    $ path_to/ddc_field_modify.sh
    Changed ./primes/README.yaml
    Changed ./job_arrays/README.yaml
    Changed ./mpi/README.yaml

You can use the example find commands above to look at the READMEs before and after the change.

# Disallowed Characters

There are some characters that should not include in the README.yaml files.
These characters are: `<  >  {  }  (  )  ;`
If those characters are included then some of those characters may be removed
from the text. The right hand side "Table of contents" for that page will also
show a link "Metadata Warnings" and the bottom of the page will show:

> Metadata Warnings    
> The following README.yaml files contained at least one of the disallowed characters: < > { } ( ) ;

This might be a bit inconvenient but it helps to ensure the security of users
browsing the site.

