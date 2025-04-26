#!/bin/bash

# This installs or updates the data directory cataloger from the git directory.
# You will need to set the directory where you wish to install the programs below.
# Run this script with sudo if the destination directory is only writable by root.
#
# Usage:
#
#   $ ./install_ddc.sh
#
# or:
#
#   $ sudo ./install_ddc.sh

# Set the full path to the directory where you wish to install the DDC
# programs here. Do not add any trailing / on the end.
dest='/opt/eresearch/ddc/bin'

# Nothing else below here needs to be changed.

function get_installed_version {
    # This checks if the user already has an installed version of DDC
    # and if so gets the version of this.
    # If the program is not installed then installed_version is set
    # to an empty string.
    if [ -f ${dest}/ddc.py ]; then
        # A grep will return something like this:
        # version = "1.3.0 + 5 (gbb38009)"
        installed_version=$(grep 'version = ' ${dest}/ddc.py)
        # Strip the text 'version = '.
        installed_version=${installed_version#version = }
        # Strip the leading and training quotes.
        installed_version=${installed_version//\"}
    else
        installed_version=''
    fi
}

function get_git_version {
    # THIS FUNCTION IS NO LONGER USED.
    #
    # This gets the current git version string.
    #
    # If this repo is checked out at a tagged release version then just
    # use the tag number only for the displayed version, like 2.0.0.
    # If this repo is not at a tagged release then we wish to know the exact
    # patch that a user might be using so use the long "git describe" string
    # like 2.0.0-6-g382c9e0.
    #
    # The command "git describe" string format is:
    #   'tag' - 'number of commits' - 'abbreviated commit name'
    #
    # e.g. git describe 2.0.0 --long
    #      2.0.0-0-g7ef3b13  <== The middle number is zero.
    #
    # e.g. git describe --long
    #      2.0.0-6-g382c9e0  <== The middle number is not zero.
    #
    description=$(git describe --long)
    version_num=$(echo $description | cut -d '-' -f1)  # e.g. 2.0.0
    num_commits=$(echo $description | cut -d '-' -f2)  # e.g. 1
    commit_hash=$(echo $description | cut -d '-' -f3)  # e.g. g1d02627
    if [ $num_commits -eq 0 ]; then
        # This is a tagged release.
        # The git_version will be just e.g. 1.3.0
        git_version=$version_num
    else
        # This version has commits after the last tagged release.
        # The git_version will be like e.g. 1.3.0-34-gb0df536
        git_version="$version_num + $num_commits ($commit_hash)"
    fi
}

function create_backup {
    # Backup any existing ddc.py program and rename it with todays date.
    # But once todays backup is created, don't overwrite it again.

    TODAY=$(date "+%Y.%m.%d")   # Todays date, 2013.12.26
    
    if [ -f ${dest}/ddc.py ] && [ ! -f ${dest}/ddc_${TODAY}.py ]; then
        echo "Copying ddc.py to backup."
        cp ${dest}/ddc.py ${dest}/ddc_${TODAY}.py
        if [ $? -ne 0 ]; then
            echo "Could not create backup."
            echo "Perhaps you need to use sudo. Exiting."
            exit 1
        else    
            exit 0
        fi
    fi
}

function install_new_version {

    # Copy the main DDC program to the destination.
    echo "Installing:"
    echo "  ddc.py"
    cat ddc.py | sed "s/VERSION_STRING/$git_version/" > ${dest}/ddc.py

    # Copy useful scripts to the destination.
    # Users should not run these from the destination. They should copy 
    # them to their own directory, edit to suit, then run their own copy. 
    # So we set them here as non executable.
    for script in ddc_field_add.sh ddc_field_modify.sh ddc_field_remove.sh; do
        echo "  $script"
        cp useful_scripts/$script ${dest}/
        chmod 644 ${dest}/$script
    done

    # Allow any user to run ddc.py and write_readmes.py.
    # Because ddc.py only writes to stdout and write_readmes.py will not overwrite
    # existing READMEs its safe for those with write access to those directories
    # to run this.
    cp useful_scripts/write_readmes.py ${dest}
    chmod 755 ${dest}/write_readmes.py
    chmod 755 ${dest}/ddc.py
    echo ""
}

######
# Main
######

echo ""
echo "----------------------------------------------"
echo "Install or Update the Data Directory Cataloger"
echo "----------------------------------------------"
echo ""

# Get the current git version and if the user already has
# a version installed get the version of that as well.
# get_git_version <== This function is no longer used.
git_version=$(git describe --abbrev=0)
get_installed_version

# Check user really wants to install.
echo "This script will install the DDC programs to ${dest}/"
echo "The programs to be installed are ddc.py and a few unversioned scripts."
echo ""

# Show the currently installed version number, if installed.
if [ "$installed_version" != '' ]; then
    echo "The currently installed version of ddc.py $installed_version"
fi

# Show the version number to be installed.
echo "The version of ddc.py to be installed is $git_version"
echo ""
read -r -p "Type \"y\" to install. Any other key will exit: " REPLY
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "exiting"
    exit 0
fi

# If the destination directory does not exist, then create it.
if [ ! -d $dest ]; then
    echo "Creating directory $dest"
    mkdir -p $dest
    if [ $? -ne 0 ]; then
        echo "Could not create directory $dest"
        echo "Perhaps you need to use sudo. Exiting."
        exit 0
    fi
fi

create_backup
install_new_version

