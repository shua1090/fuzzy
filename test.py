# Author: Govind Gnanakumar

def recursive_search(fileExt='*'):
    import os

    home = os.path.expanduser('~')
    collection = []

    from pathlib import Path

    for path in Path(home).rglob(f'*.{fileExt}'):
        collection.append( str(path) )

    return collection


def fuzzy_finder(user_input, collection):
    import re

    suggestions = []
    pattern = ".*?".join(user_input)
    regex = re.compile(pattern)
    for item in collection:
        match = regex.search(item)
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    return [x for _, _, x in sorted(suggestions)]


import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("fileExtension", nargs='?', default='*', help="File extension")
    args = parser.parse_args()
    return args


def lower_format():
    args = get_args()
    return args.fileExtension.lower()

if __name__ == "_main_":
    a = lower_format(get_args())
    print(fuzzy_finder(recursive_search(a)))