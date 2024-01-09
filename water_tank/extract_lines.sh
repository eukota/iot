#!/usr/bin/env bash

function usage() {
    echo "**************";
    echo "This script is intended to be used to read between two given partial line lookups in a file.";
    echo "    Sample Usage:";
    echo "    $0 \\";
    echo "      --from_search 2023-05-01\\";
    echo "      --to_search 2023-10-01\\";
    echo "      --data_file /var/log/water_distance.txt\\"; 
    echo "      --out_file ~/data_extract_file.txt\\"; 
    echo "      --zip"; 
}

# Parse Inputs
while [[ $# > 0 ]]; do
    case "$1" in
        --from_search|-f) FROM_SEARCH=${2}; shift;shift;;
        --to_search|-t) TO_SEARCH=${2}; shift;shift;;
        --data_file|-d) DATA_FILE=${2}; shift;shift;;
        --out_file|-o) OUT_FILE=${2}; shift;shift;;
        --zip) ZIP=1; shift;;
        *) usage; exit 1;
    esac
done

# Print Inputs
echo "************************";
echo "FROM_SEARCH: ${FROM_SEARCH}";
echo "TO_SEARCH:   ${TO_SEARCH}";
echo "DATA_FILE:   ${DATA_FILE}";
echo "OUT_FILE:    ${OUT_FILE}";
echo "ZIP:         ${ZIP}";
echo "************************";

# search for file lines
echo "Finding date lines..."
FROM_INPUT="/${FROM_SEARCH}/{print NR; exit}"
FROM_LINE=$(awk "${FROM_INPUT}" ${DATA_FILE})
echo "${FROM_SEARCH} found on line ${FROM_LINE}"
TO_INPUT="/${TO_SEARCH}/{print NR; exit}"
TO_LINE=$(awk "${TO_INPUT}" ${DATA_FILE})
echo "${TO_SEARCH} found on line ${TO_SEARCH}"

# extract from line to line
echo "Extracting to file ${OUT_FILE}..."
TO_FILE=~/summer_2023.txt
sed -n "${FROM_LINE},${TO_LINE}p" ${DATA_FILE} > ${OUT_FILE}

if [[ ! -z ${ZIP} ]]; then
    zip ${OUT_FILE}.zip ${OUT_FILE}
fi

echo "DONE!"
