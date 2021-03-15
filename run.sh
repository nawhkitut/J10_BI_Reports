#!/bin/bash

for dir in ./J10_Reports/*/; 
do
    dir=${dir%*/}   
    echo "-------${dir##*/}-------"
    for dir2 in ./J10_Reports/${dir##*/}/*;
    do
        dir2=${dir2%*/}   
        echo ${dir2##*/}
        python ./scripts/html_only.py --path J10_Reports/${dir##*/}/${dir2##*/} --level 1
        rm -rf J10_Reports/${dir##*/}/${dir2##*/}/first_level
    done
done