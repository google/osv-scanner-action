#!/usr/bin/env python3

"""
Performs the three git commit required to do a release. See help output for more details.
"""

import subprocess
import re
import sys


def cmd(command: list[str]) -> str:
    print('$ ' + ' '.join(command))
    process = subprocess.run(command, capture_output=True, text=True)
    if process.returncode != 0:
        print('failed to run above command, got exit code: %d', process.returncode)
        print('stderr: ' + process.stderr.strip())
        exit(process.returncode)

    output = process.stdout.strip()
    print('# ' + output)
    return output


def find_and_replace_regex_in_file(file_path: str, find_regex: str,
                                   replace: str):

    print(f'Performing find and replace on "{file_path}": s/{find_regex}/{replace}')
    # Read in the file
    with open(file_path, 'r') as file:
        filedata = file.read()

    filedata = re.sub(find_regex, replace, filedata)

    # Write the file out again
    with open(file_path, 'w') as file:
        file.write(filedata)


def print_help():
    print('''update-script.py <target-tag> <optional:previous-tag>

Performs a series of git merges to update all references of the previous version to the specified tag of osv-scanner. This script expects upstream remote to be named `upstream`
1. Fetch upstream main branch
2. Create new branch on the most recent version tag (the last release commit)
3. Update references to the old osv-scanner tag to the new tag.
4. Commit the changes.

After this script is complete, push the new branch and create a PR.
Then create the new release tag on this merged PR commit.''')


if len(sys.argv) != 2 and len(sys.argv) != 3:
    print_help()
    exit()

target_tag = sys.argv[1]
if not target_tag.startswith('v'):
    print_help()
    print('Target tag needs to begin with v')
    exit()

cmd(['git', 'fetch', 'upstream'])
print("fetched and checkout upstream/main")

if len(sys.argv) == 3:
    latest_tag = sys.argv[2]
else:
    latest_tag = cmd(['git', 'describe', '--tags', '--abbrev=0'])

branch_name = cmd(['git', 'branch', '--show-current'])

cmd(['git', 'checkout', '-b', 'update-to-' + target_tag, 'upstream/main'])

find_and_replace_regex_in_file('osv-reporter-action/action.yml',
                               re.escape(latest_tag), target_tag)
find_and_replace_regex_in_file('osv-scanner-action/action.yml',
                               re.escape(latest_tag), target_tag)
find_and_replace_regex_in_file('README.md', re.escape(latest_tag), target_tag)

cmd([
    'git', 'commit', '-a', '-m',
    f'"Update actions to use {target_tag} osv-scanner image"'
])

print('Success!')
  
