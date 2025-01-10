#!/bin/bash

# Check if the number of arguments is correct
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input-json-file> <output-json-file>"
    exit 1
fi

# Input JSON folder from argument
INPUT_JSON="$1"
# Output JSON folder from argument
OUTPUT_JSON="$2"

# For each file in the input folder if it is a json file
for file in "$INPUT_JSON"/*.json; do
    if [ -f "$file" ]; then
        # Check if the file is a JSON file
        if [[ "$file" == *.json ]]; then
            # Transform the JSON
            jq '(.authorizationSettings.policies[] | select(.name == "Default Policy")) |= 
              (.type = "regex" |
               .config = {
                  "targetContextAttributes": "false",
                  "pattern": ".*",
                  "targetClaim": "sub"
               })' "$file" > "$OUTPUT_JSON/$(basename "$file")"
        fi
    fi
done

echo "Transformation complete. Check the output in $OUTPUT_JSON"