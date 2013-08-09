#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

try:
    from argparse import ArgumentParser as ArgParser
except ImportError:
    from optparse import OptionParser as ArgParser

try:
    import builtins
except ImportError:
    def print_(*args, **kwargs):
        """The new-style print function taken from
        https://pypi.python.org/pypi/six/

        """
        fp = kwargs.pop("file", sys.stdout)
        if fp is None:
            return

        def write(data):
            if not isinstance(data, basestring):
                data = str(data)
            fp.write(data)

        want_unicode = False
        sep = kwargs.pop("sep", None)
        if sep is not None:
            if isinstance(sep, unicode):
                want_unicode = True
            elif not isinstance(sep, str):
                raise TypeError("sep must be None or a string")
        end = kwargs.pop("end", None)
        if end is not None:
            if isinstance(end, unicode):
                want_unicode = True
            elif not isinstance(end, str):
                raise TypeError("end must be None or a string")
        if kwargs:
            raise TypeError("invalid keyword arguments to print()")
        if not want_unicode:
            for arg in args:
                if isinstance(arg, unicode):
                    want_unicode = True
                    break
        if want_unicode:
            newline = unicode("\n")
            space = unicode(" ")
        else:
            newline = "\n"
            space = " "
        if sep is None:
            sep = space
        if end is None:
            end = newline
        for i, arg in enumerate(args):
            if i:
                write(sep)
            write(arg)
        write(end)
else:
    print_ = getattr(builtins, 'print')
    del builtins

def plot():
    parser = ArgParser(description="plot script generator")
    try:
        parser.add_argument = parser.add_option
    except AttributeError:
        pass

    parser.add_argument('--file', help='Specify a result file to plot')

    options = parser.parse_args()
    if isinstance(options, tuple):
        args = options[0]
    else:
        args = options
    del options

    filename = args.file or "result.json"
    with open(filename, 'r') as infile:
        stats = json.load(infile)
        for a in stats:
            print "%s-%s-%fkm %s %f %f %f " % (a['cc'], a['name'], a['d'] ,  a['id'], a['latency'], a['download'], a['upload'])

def main():
    try:
        plot()
    except KeyboardInterrupt:
        print_('\nCancelling...')

if __name__ == '__main__':
    main()
