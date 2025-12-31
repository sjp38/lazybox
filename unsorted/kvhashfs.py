#!/usr/bin/env python3

'''
Simple key-value pairs storage system.  Save the pairs in a radix tree-style
directories on the local file system.
'''

import argparse

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='command', dest='command',
                                       metavar='<command>')
    parser_save = subparsers.add_parser('save', help='save a key-value pair')
    parser_save.add_argument('key', metavar='<string>', help='key to store')
    parser_save.add_argument(
            'value', metavar='<string>', help='value to store')

    parser_load = subparsers.add_parser('load', help='load a key-value pair')
    parser_load.add_argument('key', metavar='<string>', help='key to load')
    args = parser.parse_args()

if __name__ == '__main__':
    main()
