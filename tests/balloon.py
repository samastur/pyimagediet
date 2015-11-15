#!/usr/bin/env python

import sys


def main(filename, content, *args):
    with open(filename, 'a') as f:
        f.write(content)
        f.write('\n')


if __name__ == '__main__':
    main(*sys.argv[1:])
