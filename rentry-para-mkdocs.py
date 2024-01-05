import re, sys, os
from googletrans import Translator

sys.stdout = open(f"rentry-para-mkdocs.log", 'w')

def format_text_with_regex(line):
    """
    Format a line using regular expressions.

    Args:
        line (str): The input line to be formatted.

    Returns:
        str: The formatted line.
    """
    try:
        line = re.sub(r'^\*{5}\n\[Go back to top\]\(https://rentry\.org/pgames/#pirated-games-mega-thread\)\n\*{5}$', '', line)

        line = re.sub(r'^!!!\s*(note|info)\s*(.*)$', r'!!! \1 "\2"', line)

        line = re.sub(r'!!! info ""', '!!! info "Informação"', line)

        line = re.sub(r'^->.*<-$', '', line)

        return line

    except Exception as e:
        print(f"Error formatting line: {str(e)}")
        return line  # Return the original line in case of an error

def process_file(input_file_path, output_file_path):
    """
    Process the input file by removing specific lines and applying regex formatting.

    Args:
        input_file_path (str): Path to the input file.
        output_file_path (str): Path to the output file.

    Returns:
        None
    """
    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file:
            lines = input_file.read().splitlines()

        formatted_lines = []

        remove_next_line = False

        for line in lines:
            if "Go back to top" in line:
                remove_next_line = True
                continue
            elif remove_next_line:
                remove_next_line = False
                continue

            formatted_lines.append(format_text_with_regex(line))

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write('\n'.join(formatted_lines))

        print(f"Markdown file has been processed. New file created: {output_file_path}")

    except Exception as e:
        print(f"Error processing file: {str(e)}")

def translate_file(input_file, lang):
    """
    Translates the content of an input file to the specified language and saves it to a new file.

    Args:
        input_file (str): Path to the input file.
        lang (str): Target language code for translation.

    Returns:
        None
    """
    translator = Translator()

    file_name = os.path.basename(input_file)
    file_name_without_extension, file_extension = os.path.splitext(file_name)

    destination_folder = os.path.dirname(input_file)
    destination_file = os.path.join(destination_folder, f"{file_name_without_extension}.{lang}.md")

    try:
        with open(input_file, 'r', encoding='utf-8') as source_file:
            text = source_file.read()

        if len(text) > 5000:
            blocks = [text[i:i+5000] for i in range(0, len(text), 5000)]
            translations = [translator.translate(block, dest=lang).text for block in blocks]
            translated_text = ' '.join(translations)
        else:
            translated_text = translator.translate(text, dest=lang).text

        with open(destination_file, 'w', encoding='utf-8') as target_file:
            target_file.write(translated_text)

        print(f"Translation completed for {file_name}. Translated file saved at {destination_file}")

    except Exception as e:
        print(f"Error translating {file_name}: {str(e)}")

input_folder = 'rentry'
output_folder = 'mkdocs'

os.makedirs(output_folder, exist_ok=True)

try:
    for filename in os.listdir(input_folder):
        if filename.endswith('.md'):
            print(f"Processing current input file: {filename}")

            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename)

            process_file(input_file_path, output_file_path)

            print(f"Translating file: {filename}")

            translate_file(output_file_path, 'pt')

    print("Processing and translation completed for all eligible files.")

except Exception as e:
    print(f"Error: {str(e)}")