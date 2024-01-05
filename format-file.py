import re, os, sys

sys.stdout = open(f"format-file.log", 'w')

def format_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as input_file:
        content = input_file.read()

        pattern = re.compile(r'# (.+?)\n', re.UNICODE)
        match = pattern.search(content)

        if match:
            output_content = '---\ntitle: {}\ntype: docs\n---\n{}'.format(match.group(1), content[match.end():] if match else content)

            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(output_content)

            print("Done!")
        else:
            print("Couldn't find the title.")

input_path = 'docs'
output_path = 'docs-output' 

os.makedirs(output_path, exist_ok=True)

for filename in os.listdir(input_path):
    if filename.endswith('.md'):
        print(f"Processing current input file: {filename}")

        input_file_path = os.path.join(input_path, filename)
        output_file_path = os.path.join(output_path, filename)

        format_file(input_file_path, output_file_path)

print("Processing completed for all eligible files.")
