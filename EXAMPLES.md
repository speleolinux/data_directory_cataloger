---
title: README for the DDC Examples
toc: true
---

# Description

In this directory are some examples of the output of the Data Directory Cataloger.

The first example is a single web page which describes the contents under one
directory. Open `example.html` in your web browser.    
See [A Single Webpage for One Directory](#a-single-webpage-for-one-directory)
for a detailed description of how it was generated.

The second example is a screenshot of a website which describes the contents
of multiple directories.    
See [A MkDocs Website for Multiple Directories](#a-mkdocs-website-for-multiple-directories)

# A Single Webpage for One Directory

This example shows how to create single webpage describing the directories below
our `/shared/opt/` directory. This contains shared optional programs for our HPC.
The contents of this directory is like the list below:

    $ ls -1 /shared/opt/
    centos6
    fastqc-0.10.1
    fastqc-0.11.9
    gromacs-2018.8
    gromacs-2019.6
    gromacs-2020.4
    gromacs-2021.4
    intel
    julia-1.0.0
    julia-1.6.2
    matlab_R2021b
    mmseqs2-v12
    openmpi-4.0.4
    openmpi-4.1.2
    R-3.4.4

We need to create a README.yaml file under each of these directories.

## Write the README.yaml Files

This short script just saves a bit of time by writing a README.yaml
file into each of the sub-directories. The text of the README.yaml file
that will be written is in the script. You can edit it to change the text.
For this example nothing needed to be changed so it was just run.

    $ ./write_readmes.py /shared/opt

Each of the top level directories now contains a README.yaml file.

## The README.yaml files under `/shared/opt/`

These are what some of the README.yaml files now look like under the
directory `/shared/opt/`.

/shared/opt/R-3.4.4/README.yaml

    Title: R version 3.4.4
    Description: R version 3.4.4. This is old and can be removed.
    Data Manager: Mike Lake

/shared/opt/centos6/README.yaml

    Title: Old Centos 6 programs
    Description: Older programs compiled under Centos 6. They may work under Centos 8.
    Data Manager: Mike Lake

/shared/opt/fastqc-0.10.1/README.yaml

    Title: FastQC is a high throughput sequence QC analysis tool
    Description: FastQC reads a set of sequence files and produces from each one a quality control report. 
    Data Manager: Mike Lake

/shared/opt/gromacs-2018.8/README.yaml

    Title: GROMACS 2018.8
    Description: Molecular dynamics package mainly designed for simulations of proteins, lipids, and nucleic acids. Compiled with PBS MPI.
    Data Manager: Mike Lake

/shared/opt/intel/README.yaml

    Title: Intel Compiler
    Description: Intel compiler version 2018
    Data Manager: Mike Lake

As you can see above the READMEs contain the metadata describing each sub-directory in the READMEs.

## Run the DDC Program

I then ran the Data Directory Cataloger program over the top level directory directory, directing
the output to `example.md`:
    
    $ ./ddc.py /shared/opt > example.md

## Use pandoc to Create a Webpage

Then I used "pandoc" to convert the "example.md" Markdown document into the
"example.html" HTML page. 
    
    $ pandoc --css=styles.css --self-contained example.md > example.html

This requires the `styles.css` to be in this directory. It will produce a
standalone HTML doc. The `--self-contained` option will insert the styles
into the head of the doc. Hence it will not require the separate styles.css
file to be present when viewing the web page.

You can install `pandoc` from your Linux distribution's repositories.

# A MkDocs Website for Multiple Directories

The image here shows one of the pages of the eResearch website at the
University of Technology Sydney. This was created using the Data Directory
Cataloger to process several directories containing terabytes of data.
The README.yaml files found one level below each of these directories were
processed and a Markdown file created for each directory. They were then
combined into a single web site using the static website generator "MkDocs". 

You can create a similar site by copying the MkDocs `mkdocs_uts_example.yml` to 
`mkdocs.yml` and editing it to suit your site. 
Also copy the script `update_uts_site_example.sh` and edit it to suit your site.

<p align="center" width="100%" style="text-align:center;">
<img src="examples/mkdocs_screenshot.png" alt="MkDocs site example" width="80%" style="border: 1px solid black;"/>
</p>

Mike Lake    
June 2022

