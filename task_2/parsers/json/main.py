#!/usr/bin/env python

from factory import Creator
import argparse
import os


def main():
    if args.type.lower() == 'json':
        des_ext = 'json'
    elif args.type.lower() == 'yaml':
        des_ext = 'yaml'
    elif args.type.lower() == 'toml':
        des_ext = 'toml'
    elif args.type.lower() == 'pickle':
        des_ext = 'pickle'
    else:
        raise TypeError("Wrong type of extension passed! Available formats are: JSON/Toml/Yaml/Pickle")

    if args.start[(len(args.start) - 5):] == '.json':
        start_ext = '.json'
    elif args.start[(len(args.start) - 5):] == '.yaml':
        start_ext = '.yaml'
    elif args.start[(len(args.start) - 5):] == '.toml':
        start_ext = '.toml'
    elif args.start[(len(args.start) - 7):] == '.pickle':
        start_ext = '.pickle'
    else:
        raise TypeError("Wrong type of file passed! You must provide file with extension like JSON/Toml/Yaml/Pickle")

    if start_ext[1:] == des_ext:
        print("Type of destination file is same as extension of existing file. I will not convert one type of data "
              "into the same type! See you later!")
        exit()

    obj = Creator.createDeserializer(type=start_ext[1:], filePath=args.start, isBuffer=True)

    if args.dest is not None:
        pf = args.dest
    else:
        pf = args.start[:(len(args.start) - len(start_ext))] + "." + des_ext

    Creator.createSerializer(obj, des_ext, pf)


# converter --from "ORIGINATOR" -t JSON --WHERE "ADENOPATHIES"
parser = argparse.ArgumentParser(description='Convert files from one notation into another')
parser.add_argument('-t', '--type', type=str, metavar='T', required=True,
                    help='Type of converter(JSON, Toml, Yaml, Pickle). In this format your file will be converted')
parser.add_argument('-s', '--start', type=os.path.abspath, metavar='S', required=True,
                    help='Path to starting file')
parser.add_argument('-d', '--dest', type=os.path.abspath, metavar='D',
                    help='Path to file where to put the result of conversation')
args = parser.parse_args()

main()
