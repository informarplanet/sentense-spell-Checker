import subprocess
import argparse
import os
import sys

def check_aspell_installed():
    """Check if aspell is installed."""
    try:
        subprocess.run(["aspell", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("Error: Aspell is not installed. Please install it.")
        sys.exit(1)

def spell_check_file(input_file, output_file=None):
    """Run aspell on the file and optionally write misspelled words to an output file."""
    with open(input_file, "r") as file:
        # Run aspell list to find misspelled words
        result = subprocess.run(["aspell", "list"], input=file.read(), text=True, capture_output=True)
        misspelled_words = result.stdout.splitlines()
        
    # If an output file is specified, write misspelled words to the file
    if output_file:
        with open(output_file, "w") as file:
            file.write("\n".join(misspelled_words))
        print(f"Spell check complete. Results saved to '{output_file}'.")
    else:
        print("Misspelled words:")
        print("\n".join(misspelled_words))

    # Display suggestions for each misspelled word
    print("\nSuggestions for misspelled words:")
    for word in misspelled_words:
        print(f"\nSuggestions for '{word}':")
        suggestions = subprocess.run(["aspell", "-a"], input=word, text=True, capture_output=True).stdout
        # Skip the first line of output, which is a header
        print("\n".join(suggestions.splitlines()[1:]))

def main():
    # Check if aspell is installed
    check_aspell_installed()
    
    # Argument parsing
    parser = argparse.ArgumentParser(description="Spell checker using aspell.")
    parser.add_argument("-f", "--file", required=True, help="Specify the file to check for spelling errors.")
    parser.add_argument("-o", "--output", help="Specify an optional output file to save results.")
    args = parser.parse_args()

    # Check if the input file exists
    if not os.path.isfile(args.file):
        print(f"Error: File '{args.file}' not found.")
        sys.exit(1)

    # Run the spell check
    spell_check_file(args.file, args.output)

if __name__ == "__main__":
    main()
