#!/usr/bin/env python3

'''
This is the Data Directory Cataloger. The purpose of it is to help manage numerous
directories of data by having a README.yaml in most directories and which stores
metadata about the contents of that directory.

This program expects a "top level" directory as input.

Under this top level directory it then looks for subdirectories, but only ONE level down.
In each first level subdirectory it looks for the README.yaml file that should describe
the data under that subdirectory.

Once it has found the README.yaml file it parses that file, and appends the metadata
to a Markdown document summarising the metadata in the READMEs.

This Markdown doc is just printed to standard output so it can be viewed or redirected
to an output file. Single output files can be converted to HTML using pandoc or if you
have many Markdown docs they can be used for the content of a static website generator
such as MkDocs.

To get help for using the program just run: ./ddc.py -h

License
Copyright 2022 Mike Lake

'''

# Filename of the README in each directory that contains the directory meta information.
# This does not need to be literally "README.yaml". It just needs to not clash with other
# filenames in the directory that you are processing. Example, if you don't want to use
# README.yaml then you might use CATALOG.yaml.
readme='README.yaml'

# Users provide the content for the README.yaml files and the data ends up on a 
# web page. So for security there is a set of characters that will be replaced.
# This is a dictionary. For the key specify the single character to be replaced,
# and for its value specify its replacement character. This can be None.
# This can be printed as a string with:
# print('Disllowed characters are: ', ' '.join(deny_list.keys()))
deny_list = {
    '<':'&lt;',
    '>':'&gt;',
    '{':'',
    '}':'',
    '(':'',
    ')':'',
    ';':'' }

# The version string will be automatically updated by the install script from the git repo.
# We use Semantic Versioning https://semver.org/spec/v2.0.0.html
version = "VERSION_STRING"

DEBUG = False

import argparse, os, sys, copy
import yaml, datetime
    
def debug_data(data):
    '''
    Pretty print the data dictionary containing the YAML docs.
    Just call this function at some point in the code.
    '''
    import pprint
    print('DEBUGGING START ------------')
    pprint.pprint(data)
    print('DEBUGGING END ------------')


def parse_args():
    '''
    There is one mandatory positional arg (a directory) plus
    an optional arg to display the program version.
    '''

    parser = argparse.ArgumentParser( \
        description='Program to catalog %s docs under a directory.' % readme)

    # Add the positional arg, being the input directory required.
    parser.add_argument('directory', help='The directory to catalog.')

    # Add an optional arg to show the programs version number.
    parser.add_argument('-v', '--version', action='version', \
        version='This is %(prog)s version {}'.format(version))

    args = parser.parse_args()
    return args

def get_readmes(topdir):
    '''
    Given a top level directory return two lists:
    1. A found list of all directory paths that have a README.yaml
    2. A missing list of directory paths that do not have a README.yaml
    They are sorted alphabetically for the convenience of the user.
    '''

    found = []      # List of paths for found READMEs.
    missing = []    # List of paths missing READMEs.

    # scandir returns an iterator of DirEntry objects for the given path.
    subdirs = [ f.path for f in os.scandir(topdir) if f.is_dir() ]

    for dir in subdirs:
        # Append the path to the directory to either the found list or the
        # missing list, depending on whether the README was found or not.
        if os.path.isfile(os.path.join(dir, readme)):
            found.append(dir)
        else:
            missing.append(dir)

    # Sort alphabetically.
    found.sort()
    missing.sort()

    # Return a tuple of a list of the found and the missing READMEs.
    return (found, missing)

def parse_readmes(found):
    '''
    Takes a list of directories containing a README.yaml file and parses that README doc.
    Each doc's YAML structure is a dictionary.
    '''

    # The "data" variable is a dictionary. It's keys will be the README.yaml
    # file paths and the values are the YAML structures for that README.yaml
    data = {}

    for dir in found:
        file = os.path.join(dir, readme)
        with open(file, 'r') as stream:
            try:
                # Note here, use safe_load() and not load()! Do not trust user input!
                doc = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                # Although the error (e) is available here do not send it to stdout
                # as stdout becomes the web page that is displayed to a user. That
                # could be a security problem. Just output the path to the README.
                print('')
                print('<span style="color:red;" >')
                print('Error in reading YAML file: ', os.path.join(dir, readme), '<br>')
                print('</span>')
                print('')
                # And we set an empty dictionary for this directories "doc".
                # This is the safest thing to do.
                doc = {}

        # Debugging lines
        #print('---------------------------')
        #print('README: %s' % file)
        #print('KEYS:', doc.keys())
        #print('PYTHON OBJECT: ', doc)
        #print('YAML DUMP:')
        #print(yaml.dump(doc, default_flow_style=False))

        # Add this YAML doc to the data dictionary with the directory path as the key.
        if doc is not None:
            data[dir] = doc

    return data

def sanitise_data(data, deny_list):
    '''
    Users provide the content for the README.yaml files, these in turn are processed,
    and the data ends up on a web page. There is potential here for misuse. We already
    use safe_load only, which just loads subset of the YAML language safely, but users
    could still insert javascript into the YAML files. Here we look for several chars
    that might indicate javascript content and replace or strip them out. This might
    cause some inconvenience to users. They are set in the "deny_list.
    '''

    warnings = set()

    # str.maketrans takes a dictionary. For the key specify the single character
    # to be replaced, and for its value specify its replacement.
    # It returns a translation table usable for str.translate().
    trans_table = str.maketrans(deny_list)

    for directory in data.keys():
        # We don't need to check the keys in the data dictionary as they
        # are the directory paths, found and entered by this program.
        # The values in the data dictionary are the YAML docs, each one being a
        # dictionary. We have to check their keys and values.

        doc = data[directory]  # Each doc is a single row in the Markdown table.
        sanitised = False
        path = os.path.join(directory, readme)

        # We have to make a shallow copy, otherwise we get a RuntimeError;
        # "dictionary changed size during iteration".
        # Also, sanitise the keys in a separate iteration to the values.
        doc_copy = copy.copy(doc)
        for key in doc_copy.keys():
            value = doc[key]
            # We do have to check all the keys and values in each "doc"
            # TODO Can this can be simplified into a list comprehension using a small function?
            key_sanitised = key.translate(trans_table)
            if key_sanitised != key:
                doc[key_sanitised] = value  # Insert a new key, with old keys value.
                doc.pop(key)                # Remove the old key.
                sanitised = True
                warnings.add(path)   # Append directory only, not key.
                if DEBUG:
                    print('DEBUG KEY REPLACED: ', key, '==>', key_sanitised)

        for key in doc.keys():
            value = doc[key]
            if type(value) == str:
                # We have to check its a string as a user could have just a numeric value here.
                value_sanitised = value.translate(trans_table)
                if value_sanitised != value:
                    doc[key] = value_sanitised
                    sanitised = True
                    warnings.add(path)  # Append directory only, not value.
                    if DEBUG:
                        print('DEBUG VALUE REPLACED: ', value, ' ==> ', value_sanitised)

        if sanitised:
            data[directory] = doc

    return (data, warnings)

def get_metadata(data):
    '''
    Ideally all the READMEs should have the same metadata keys, but some might
    have missing keys. What we do here is use a set to get a unique set of all
    the metadata keys used by all the READMEs.
    '''

    # This set starts off as empty but will, at the end of the loop, contain
    # the complete set of all metadata values from all the README.yam files.
    metadata = set()

    for directory in data.keys():
        doc = data[directory]
        this_set = set(doc.keys())
        # The | operator gives the union of the two sets. By doing a union of sets
        # we are effectively adding this latest set to the final metadata set.
        metadata = metadata | this_set

    # Return a 'set'.
    return metadata

def print_metadata(metadata):
    '''
    Print the metadata as a Markdown list.
    '''

    print('\n## Metadata Information')
    print('\nThe following are all the %d metadata attributes found in the %s files at this level.' \
        % (len(metadata), readme))
    print('These should all be unique. If not edit and correct the %s files.' % readme)
    print('')
    [print(' -', item) for item in sorted(metadata)]

def check_metadata(data, metadata, warnings, deny_list):
    '''
    Check if any READMEs are missing any metadata values or
    if any keys or values contain disallowed characters.
    '''

    passed = True
    newline = False
    title_printed = False

    # First check if all of the README.yaml files all have the same metadata fields.
    # If any of them are missing a metadata field set passed to False.
    for directory in data.keys():
        doc = data[directory]
        this_set = set(doc.keys())
        if len(doc) != len(metadata):
            # Print a newline just once, it's needed at the start of the Markdown list.
            if not newline:
                print('\n## Metadata Warnings')
                title_printed = True
                print('\nThe following %s files had different metadata to the list above ... ' % readme)
                print('\n', end='')
                newline = True

            # The 4 spaces at the end cause Markdown to insert a HTML <BR>.
            print(' -', os.path.join(directory, readme), '    ')

            # This is probably the clearest in Markdown for printing the set differences.
            # Note: The set difference used below isn’t commutative!
            print('    Possibly missing: ', end='')
            l = ['"%s"' % item for item in (metadata - this_set)]
            print('` %s `' % ', '.join(l))

            # Alternatives to printing the set differences.
            #print('    Possibly missing: ', metadata - this_set)
            #print('    Possibly missing: `%s`' % str(metadata - this_set))
            #print('    Possibly missing: ', end='')
            #print([str(item) for item in (metadata - this_set)])

            passed = False

    if passed:
        # Note the 4 spaces at the end cause Markdown to insert a HTML <BR>.
        print('\nChecking each %s file against the metadata list above ... passed OK.    ' % readme)

    # Second, check if there are any warnings from the sanitise_data function.
    # If so print the name of the file that contains the disallowed data character.
    if len(warnings):
        if not title_printed:
            print('\n## Metadata Warnings')
        print('\nThe following %s files contained at least one of the disallowed characters:' % readme)
        print(' '.join(deny_list.keys()))
        print('')
        [print(' -', item) for item in warnings]
    else:
        print('\nChecking each %s file for disallowed characters ... passed OK.' % readme)

def create_markdown_header(timenow):
    '''
    Valid Markdown docs have some metadata at the top. Set that here.
    Note we use a backslash here to suppress the leading newline
    as we do not want that in the Markdown.
    '''

    metadata = '''\
---
pagetitle: %s
creator: %s version %s
date: %s
---''' % ('Data Directory Cataloger', sys.argv[0], version, timenow)

    print(metadata)

def create_markdown_footer(version, timenow):
    '''
    Stuff to be printed at the end of each page.
    The spaces at the end of the first print ensure a newline in the HTML.
    '''
    print('\nCreated by DDC version %s.     ' % version)
    print('This page was updated on %s' % timenow)

def create_markdown_table(data):
    '''
    This takes a list of the keys to print out and the YAML data.
    The columns is a list and might be like this: ['Title', 'Description', 'Data Manager']
    The data is a dictionary of all the YAML docs keyed by their path.
    The final Markdown doc summarising this would be like this:

    | Directory | Title | Description | Data Manager |
    | --------- | ----- | ----------- | ------------ |
    | examples/arrays        | Job Examples for PBS Job Arrays | some description | Mike Lake |
    | examples/checkpointing | Job Examples for Checkpointing  | "                | Mike Lake |
    | examples/mpi           | Job Examples for MPI            | "                | Mike Lake |
    '''

    # Place in this list the keys that you wish to print out.
    # Capitalisation is important. They have to match the keys in your README YAML files.
    columns = ['Title', 'Description', 'Data Manager']
    # The first column in the Markdown table will always be the directory of the README YAML
    # file and the subsequent colums will be the keys in found in the the README YAML file.
    columns.insert(0, 'Directory')

    print('') # We need a blank line before the Markdown.table.

    # Print the Markdown header from the keys.
    # e.g. | Directory | Title | Description | Data Manager |
    print('| ', end='')
    print(' | '.join(columns), end='')
    print(' |')

    # Print the underlining for the header above.
    # e.g. | ----- | ----------- | ------------ |
    l = [ '-' * len(col) for col in columns ]
    print('| ', end='')
    print(' | '.join(l), end='')
    print(' |')

    # Print the data.
    for directory in data.keys():
        doc = data[directory]
        # Remember that 'Directory' is the first in our list of columns to print
        # and the value of this is the key in the data dictionary. But the actual
        # docs don't contain a value for this so we add this now.
        doc['Directory'] = directory

        l = []
        for col in columns:
            if col not in doc:
                # This doc is missing this key.
                doc[col] = ''
            if not doc[col]:
                # This doc has the key but its missing a value.
                doc[col] = ''
            l.append(doc[col])
        print('| ', end='')
        print(' | '.join(l), end='')
        print(' |')

        # We have to remove this entry as we don't want it to appear
        # in the metadata list.
        del doc['Directory']

def main():

    # Get the program args.
    args = parse_args()
    topdir = args.directory

    # This arg should be a directory.
    if not os.path.isdir(topdir):
        print('Error: you must supply a directory, %s is not a directory.' % topdir)
        print('For help run: %s -h' % sys.argv[0])
        sys.exit()

    # Get the time and todays date.
    timenow = datetime.datetime.now().strftime('%a, %d %b %Y at %I:%M %p')

    create_markdown_header(timenow)
    print('# Directory `%s`' % topdir)

    # Get all the READMEs under the top level directory.
    (found, missing) = get_readmes(topdir)

    # Print info in Markdown format on the READMEs found or otherwise.
    if len(missing) != 0:
        print('\n## Warnings\n')
        print('\nThe following subdirectories are missing a %s file:\n' % readme)
        for path in missing:
            print(' -', path)

    print('\n## Summary\n')
    print('\nFound %d `%s` files in the directories under `%s`.' % (len(found), readme, topdir))
    if len(found) == 0:
        print('Exiting.')
        sys.exit()

    # Parse these README YAML docs into a data structure.
    data = parse_readmes(found)

    # Sanitise the data as this is user input.
    (data, warnings) = sanitise_data(data, deny_list)

    print('A summary of the metadata in these files follows.')
    # Place in this list the keys that you wish to print out.
    # Capitalisation is important. They have to match the keys in your README YAML files.
    create_markdown_table(data)

    metadata = get_metadata(data)
    print_metadata(metadata)

    # Check the metadata in these READMEs for consistency.
    check_metadata(data, metadata, warnings, deny_list)

    create_markdown_footer(version, timenow)

if __name__ == '__main__':
    main()

