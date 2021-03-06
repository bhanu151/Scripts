#!/bin/bash
#http://stackoverflow.com/questions/2803823/how-can-i-delete-all-unversioned-ignored-files-folders-in-my-working-copy
# make sure this script exits with a non-zero return value if the
# current directory is not in a svn working directory
svn info >/dev/null || exit 1

svn status | grep '^[I?]' | cut -c 9- |
# setting IFS to the empty string ensures that any leading or
# trailing whitespace is not trimmed from the filename
while IFS= read -r f; do
    # tell the user which file is being deleted.  use printf
    # instead of echo because different implementations of echo do
    # different things if the arguments begin with hyphens or
    # contain backslashes; the behavior of printf is consistent
    if [[ ".git" =~ "${f}" ]]; then
        printf '%s\n' "Deleting ${f}..."
        # if rm -rf can't delete the file, something is wrong so bail
        echo "Deleting ${f}"
        rm -rf "${f}" || exit 1
    fi
done 
