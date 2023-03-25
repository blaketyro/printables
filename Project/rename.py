# This script prefixes the folder name to all of the included files in every folder in this scripts directory.
# e.g. "A4.pdf" becomes "Asymptotic_Notation_A4.pdf".
#
# This way the files have descriptive names, which otherwise would have to be done manually in Affinity Designer.
# It works even to rename the prefix if the folder name is changed (this can error if the files are named weirdly).
# It's used as a pre-commit hook (.git/hooks/pre-commit) but can be run separately too.

import pathlib
included_files = ['A4.pdf', 'A4.png', 'A4.svg', 'Letter.pdf', 'Letter.png',
                  'Letter.svg', 'Poster.pdf', 'Poster.png', 'Poster.svg', 'Source.afdesign']
excluded_folders = ['.git']


root = pathlib.Path(__file__).parent

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
