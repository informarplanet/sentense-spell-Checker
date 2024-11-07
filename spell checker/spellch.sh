#!/bin/bash

# Check if aspell is installed
if ! command -v aspell &> /dev/null; then
    echo "Error: Aspell is not installed. Please install it using 'sudo apt-get install aspell'"
    exit 1
fi

# Usage message
usage() {
    echo "Usage: $0 [-f file] [-o output]"
    echo "  -f FILE       Specify the file to check for spelling errors."
    echo "  -o OUTPUT     Specify an optional output file to save results."
    exit 1
}

# Parse arguments
while getopts ":f:o:" opt; do
    case ${opt} in
        f )
            input_file="$OPTARG"
            ;;
        o )
            output_file="$OPTARG"
            ;;
        \? )
            usage
            ;;
    esac
done

# Ensure an input file is specified
if [ -z "$input_file" ]; then
    usage
fi

# Check if the input file exists
if [ ! -f "$input_file" ]; then
    echo "Error: File '$input_file' not found."
    exit 1
fi

# Process file with aspell
if [ -n "$output_file" ]; then
    aspell list < "$input_file" > "$output_file"
    echo "Spell check complete. Results saved to '$output_file'."
else
    echo "Misspelled words:"
    aspell list < "$input_file"
fi

# Display suggestions for each misspelled word
if [ -n "$output_file" ]; then
    while IFS= read -r misspelled_word; do
        echo -e "\nSuggestions for '$misspelled_word':"
        aspell -a <<< "$misspelled_word" | tail -n +2
    done < "$output_file"
else
    echo -e "\nSuggestions for misspelled words:"
    aspell list < "$input_file" | while IFS= read -r misspelled_word; do
        echo -e "\nSuggestions for '$misspelled_word':"
        aspell -a <<< "$misspelled_word" | tail -n +2
    done
fi
