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
    parser.add_argument('--output', help='Specify a output file')

    options = parser.parse_args()
    if isinstance(options, tuple):
        args = options[0]
    else:
        args = options
    del options

    output_filename = args.output or "output"
    output_file = open(output_filename, 'w')

    filename = args.file or "result.json"
    with open(filename, 'r') as infile:
        stats = json.load(infile)

        stats_sorted = sorted(stats, key=lambda entry: int(entry['id']))

        for a in stats_sorted:
            s = "%s-%s-%fkm %s %f %f %f\n" % (a['cc'], a['name'], a['d'] ,  a['id'], a['latency'], a['download']/1000.0/1000.0*8, a['upload']/1000.0/1000.0*8)
            output_file.write(s)
    output_file.close()
    plot_script = """#!/usr/local/bin/gnuplot
set term svg enhanced mouse size %d,600 jsdir "./js/"
set output '%s.svg'
set boxwidth 1.0
set style fill solid 1.00 border lt -1
set autoscale x
set xtics nomirror rotate by -55
set xtics font "Times-Roman, 8" 
set yrange [ 0.0 : 500]
set y2range [ 0.0 : 100.0]
set y2tics
set ylabel "(ms)"
set y2label "(Mbits)"
set grid y y2
set style data histograms
plot "%s" using 3:xticlabels(1) axis x1y1 ti 'latency' , '' u 4 axis x1y2 ti 'download', '' u 5 axis x1y2 ti 'upload'""" % ( 600 + 20*len(stats_sorted), output_filename, output_filename )
    plot_script_name = "%s.plot" % output_filename
    with open(plot_script_name, 'w') as infile:
        infile.write(plot_script)
    

def main():
    try:
        plot()
    except KeyboardInterrupt:
        print_('\nCancelling...')

if __name__ == '__main__':
    main()
