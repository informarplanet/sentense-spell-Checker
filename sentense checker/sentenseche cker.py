import language_tool_python
import argparse
import os

def check_sentence(sentence, tool):
    """Check a single sentence for spelling and grammar mistakes, return corrected sentence."""
    matches = tool.check(sentence)
    corrected_sentence = sentence
    output = [f"Original Sentence: {sentence}"]

    if matches:
        for match in matches:
            output.append(f"Error: {match.message}")
            output.append(f"Suggested Replacements: {match.replacements}")
            
            # Apply the first suggestion, if available
            if match.replacements:
                corrected_sentence = (corrected_sentence[:match.offset] 
                                      + match.replacements[0] 
                                      + corrected_sentence[match.offset + match.errorLength:])

        output.append(f"Corrected Sentence: {corrected_sentence}\n")
    else:
        output.append("No errors found.\n")
    
    return "\n".join(output)


def process_file(input_file, output_file=None):
    """Process each line in the input file and optionally write corrections to an output file."""
    tool = language_tool_python.LanguageTool('en')
    results = []

    with open(input_file, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                results.append(check_sentence(line, tool))
    
    # Display results or save to output file
    if output_file:
        with open(output_file, "w") as file:
            file.write("\n".join(results))
        print(f"Spell check complete. Results saved to '{output_file}'.")
    else:
        print("\n".join(results))


def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Sentence checker using aspell.")
    parser.add_argument("-i", "--input", required=True, help="Specify the input file with sentences.")
    parser.add_argument("-o", "--output", help="Specify an optional output file to save results.")
    args = parser.parse_args()

    # Check if the input file exists
    if not os.path.isfile(args.input):
        print(f"Error: File '{args.input}' not found.")
        return

    # Run the spell check
    process_file(args.input, args.output)


if __name__ == "__main__":
    main()
