# This script prefixes the folder name to all of the included_files in every folder in this scripts directory.
# e.g. "A4.pdf" becomes "Asymptotic_Notation_A4.pdf".
# This way the files have descriptive names, which otherwise would have to be done manually in Affinity Designer.
# It works even to rename the prefix if the folder name is changed (this can error if the files are named weirdly).
#
# This script also generates README.md since the table is tedious to create manually.
#
# This is used as a pre-commit hook (.git/hooks/pre-commit) but can be run separately too.

import pathlib
included_files = ['A4.pdf', 'A4.png', 'A4.svg', 'Letter.pdf', 'Letter.png',
                  'Letter.svg', 'Poster.pdf', 'Poster.png', 'Poster.svg', 'Source.afdesign']
excluded_folders = ['_Template_Folder']
root = pathlib.Path(__file__).parent


def rename_files():
    for folder in root.iterdir():
        if not folder.is_dir() or folder.name in excluded_folders:
            continue

        prefix = f'{folder.name}_'
        for file in folder.iterdir():
            if not file.is_file():
                continue

            for suffix in included_files:
                if file.name.endswith(suffix):
                    new_file = file.with_name(prefix + suffix)
                    if file.name != new_file.name:
                        print(f'Renaming {file.name} to {new_file.name}')
                        file.rename(new_file)
                        break


table_header = """
| Topic | Letter Size (8.5in&times;11in) | A4 Size (210mm&times;297mm) | Poster Size (24in&times;36in) |
| ----- | ------------------------------ | --------------------------- | ----------------------------- |
"""


def raw_link(slug, size, ext):
    return f'https://raw.githubusercontent.com/blaketyro/printables/main/Project/{slug}/{slug}_{size}.{ext}'


def make_table_cell(folder, size, image=True):
    slug, name = folder.name, folder.name.replace('_', ' ')
    png = raw_link(slug, size, "png")
    pdf_download = raw_link(slug, size, "pdf")
    pdf_view = f'https://github.com/blaketyro/printables/blob/main/Project/{slug}/{slug}_{size}.pdf'
    svg = raw_link(slug, size, "svg")
    cell = f'[![{name}]({png})]({png}) <br> ' if image else ''
    cell += f'**[View PDF]({pdf_view})&nbsp;&nbsp;[Save PDF]({pdf_download})&nbsp;&nbsp;[PNG]({png})&nbsp;&nbsp;[SVG]({svg})**'
    return cell


def make_table_row(folder):
    slug, name = folder.name, folder.name.replace('_', ' ')
    topic = f'**{name}** <br> ([folder](/Project/{slug}))'
    letter = make_table_cell(folder, "Letter")
    a4 = make_table_cell(folder, "A4", False)
    poster = make_table_cell(folder, "Poster", False)
    parts = [topic, letter, a4, poster]
    return '| ' + ' | '.join(parts) + ' |\n'


def make_readme():
    table = table_header
    for folder in sorted(root.iterdir()):
        if not folder.is_dir() or folder.name in excluded_folders:
            continue
        table += make_table_row(folder)

    text = (root / 'readme-template.md').read_text()
    text = text.replace('{{TABLE}}', table.strip())
    (root.parent / 'README.md').write_text(text)


rename_files()
make_readme()
