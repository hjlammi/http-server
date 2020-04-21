#!/bin/bash
# script for generating a csv file to be used in creating a graph of the accumulation of lines of source code and test code during the development process.
# Example of the csv file contents to be created:
# date,source,unittest,e2e
# 2019-12-26 09:48:50 +0200,0,0,0
set -eu

function source_loc {
    find server -name '*.py' | xargs cat | sed -re '/^($|\s*#)/d' | wc -l
}

function unittest_loc {
    find tests -name '*.py' | xargs cat | sed -re '/^($|\s*#)/d' | wc -l
}

function acceptance_tests_loc {
    find tests/acceptance/cypress/integration tests/e2e/cypress/integration -name '*.js' | xargs cat | sed -re '/^$/d' | wc -l
}

function get_date {
    git show -s --format=%ai HEAD
}

echo date,source,unittest,e2e > stats.csv
for commit in $(git rev-list --reverse master)
do
    git checkout $commit
    echo $(get_date),$(source_loc),$(unittest_loc),$(acceptance_tests_loc) >> stats.csv
    sleep 0.1
done
