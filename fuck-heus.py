import re, sys, os

sys.stdout = open("fuck-heus.log", 'w')

def remove_lines_from_markdown(input_file_path, output_file_path, patterns):
    with open(input_file_path, 'r') as input_file:
        lines = input_file.readlines()

    filtered_lines = [line for line in lines if not any(re.match(pattern, line) for pattern in patterns)]

    output_directory = os.path.dirname(output_file_path)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(output_file_path, 'w') as output_file:
        output_file.writelines(filtered_lines)

if __name__ == "__main__":
    input_markdown_file_path = "example/lorem-ipsum.md"
    output_markdown_file_path = "mkdocs/lorem-ipsum.md"

    # regex101.com
    patterns_to_remove = [
        r'\-\-\-\s*\n',
        r'^title:.*\n'
    ]

    remove_lines_from_markdown(input_markdown_file_path, output_markdown_file_path, patterns_to_remove)
    print(f"As linhas foram removidas. Novo arquivo criado: {output_markdown_file_path}")
