#!/usr/bin/env python3

import subprocess
import re
import sys


def cmd(command: list[str]) -> str:
    return subprocess.run(command, capture_output=True,
                          text=True).stdout.strip()


def find_and_replace_regex_in_file(file_path: str, find_regex: str,
                                   replace: str):
    # Read in the file
    with open(file_path, 'r') as file:
        filedata = file.read()

    filedata = re.sub(find_regex, replace, filedata)
    # filedata = filedata.replace(find, replace)

    # Write the file out again
    with open(file_path, 'w') as file:
        file.write(filedata)


def print_help():
    print('update-script.py <target-tag>')


if len(sys.argv) != 2:
    print_help()
    exit()

target_tag = sys.argv[1]
if not target_tag.startswith('v'):
    print_help()
    print('Target tag needs to begin with v')
    exit()

lastest_tag = cmd(['git', 'describe', '--tags', '--abbrev=0'])
branch_name = cmd(['git', 'branch', '--show-current'])

cmd(['git', 'checkout', '-b', 'update-to-' + target_tag])

find_and_replace_regex_in_file('osv-reporter-action/action.yml',
                               re.escape(lastest_tag), target_tag)
find_and_replace_regex_in_file('osv-scanner-action/action.yml',
                               re.escape(lastest_tag), target_tag)
find_and_replace_regex_in_file('README.md', re.escape(lastest_tag), target_tag)

cmd([
    'git', 'commit', '-a', '-m',
    f'Update actions to use {target_tag} osv-scanner image'
])

first_commit_hash = cmd(['git', 'rev-parse', 'HEAD'])
print(first_commit_hash)

find_and_replace_regex_in_file(
    '.github/workflows/osv-scanner-reusable.yml',
    'uses: google/osv-scanner-action/osv-(.*?)-action@.*? # .*',
    f'uses: google/osv-scanner-action/osv-\\1-action@{first_commit_hash} # {target_tag}'
)

find_and_replace_regex_in_file(
    '.github/workflows/osv-scanner-reusable-pr.yml',
    'uses: google/osv-scanner-action/osv-(.*?)-action@.*? # .*',
    f'uses: google/osv-scanner-action/osv-\\1-action@{first_commit_hash} # {target_tag}'
)

cmd([
    'git', 'commit', '-a', '-m',
    f'Update reusable workflows to point to {target_tag} actions'
])

second_commit_hash = cmd(['git', 'rev-parse', 'HEAD'])
print(second_commit_hash)

find_and_replace_regex_in_file(
    '.github/workflows/osv-scanner-unified-workflow.yml',
    'uses: "google/osv-scanner-action/\\.github/workflows/osv-scanner-reusable(.*?)@.*?" # .*',
    f'uses: "google/osv-scanner-action/.github/workflows/osv-scanner-reusable\\1@{second_commit_hash}" # {target_tag}'
)

cmd([
    'git', 'commit', '-a', '-m',
    f'Update unified workflow example to point to {target_tag} reusable workflows'
])

# cmd(['git', 'tag', target_tag, ])
