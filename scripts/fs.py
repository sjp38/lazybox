#!/usr/bin/env python3

import argparse
import json
import os

def read_fs(root, strip_content, max_depth, current_depth=1):
    contents = {}
    for filename in os.listdir(root):
        filepath = os.path.join(root, filename)
        if os.path.isdir(filepath):
            if max_depth != None and current_depth + 1 > max_depth:
                continue
            contents[filename] = read_fs(filepath, strip_content, max_depth,
                    current_depth + 1)
        else:
            with open(filepath, 'r') as f:
                contents[filename] = f.read()
                if strip_content:
                    contents[filename] = contents[filename].strip()
    return contents

def write_fs(root, contents):
    if isinstance(contents, list):
        for c in contents:
            write_fs(root, c)
        return

    for filename in contents:
        filepath = os.path.join(root, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'w') as f:
                f.write(contents[filename])
        else:
            write_fs(filepath, contents[filename])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['read', 'write'],
            help='command to do')
    parser.add_argument('--root', help='root to do the reads or writes')
    parser.add_argument('--max_depth', type=int,
            help='depth to read')
    parser.add_argument('--dont_strip_content', action='store_true',
            help='strip contents of files')
    parser.add_argument('--contents', help='contents to write')
    parser.add_argument('--content_file',
            help='file having the content to write')
    args = parser.parse_args()

    if args.command == 'read':
        if args.root == None:
            print('--root is not given')
            exit(1)
        print(json.dumps(read_fs(args.root, not args.dont_strip_content,
            args.max_depth), indent=4, sort_keys=True))
    elif args.command == 'write':
        if args.contents != None:
            contents = args.contents
        elif args.content_file:
            with open(args.content_file, 'r') as f:
                contents = f.read()
        write_fs(args.root, json.loads(contents))

if __name__ == '__main__':
    main()
