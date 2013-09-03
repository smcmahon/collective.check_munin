#!/usr/bin/env python

""" Nagios plugin to check Munin data via rrdtool. """

import argparse
import glob
import logging
import nagiosplugin
import os.path
import re
import subprocess
import sys
import time


def readRRDData(fn):
    try:
        s = subprocess.check_output(['rrdtool', 'lastupdate', fn, ])
    except subprocess.CalledProcessError:
        print sys.exc_value
        sys.exit(3)
    mtime, value = s.split('\n')[2].split(':')
    if time.time() - float(mtime) > 600:
        print "%s has stale data." % fn
        sys.exit(3)
    return float(value.strip())


class RRD(nagiosplugin.Resource):
    """Munin RRD Resource
    """

    def __init__(self, args):
        self.hostname = args.hostname
        self.module = args.module
        self.only = args.only
        self.ignore = args.ignore
        self.rrdpath = os.path.join(args.datadir, args.domain)

    def probe(self):
        myglob = os.path.join(
            self.rrdpath,
            '%s-%s-%s-g.rrd' % (self.hostname, self.module, self.only)
            )
        logging.info('checking %s', myglob)
        myfiles = glob.glob(myglob)
        myfiles.sort()
        for fn in myfiles:
            component_pattern = re.compile(r"^.+/%s-%s-(.+)-[a-z]\.rrd$" % (self.hostname, self.module))
            mo = component_pattern.match(fn)
            if mo:
                component = mo.group(1)
                if component not in self.ignore:
                    component = component.replace('_', '/')
                    # note that we check ignore again in case it was specified with /s
                    if component not in self.ignore:
                        logging.info('reading %s', component)
                        yield nagiosplugin.Metric(component, readRRDData(fn), min=0, context='munin')


@nagiosplugin.guarded
def main():
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument('-d', '--domain', required=True, default='')
    argp.add_argument('-H', '--hostname', required=True, default='')
    argp.add_argument('-M', '--module', required=True, default='')
    argp.add_argument('-o', '--only', default='*',
                      help='restrict to a subcomponent of module')
    argp.add_argument('-i', '--ignore', action='append', default=[],
                      help='subcomponents to ignore; may be specified multiple times')
    argp.add_argument('-w', '--warning', metavar='RANGE', default='',
                      help='return warning if load is outside RANGE')
    argp.add_argument('-c', '--critical', metavar='RANGE', default='',
                      help='return critical if load is outside RANGE')
    argp.add_argument('-D', '--datadir', default='/var/lib/munin',
                        help='munin data directory if not /var/lib/munin')
    argp.add_argument('-n', '--name', default='',
                        help='Name for the metric, if not same as module')
    argp.add_argument('-v', '--verbose', action='count', default=0,
                      help='increase output verbosity (use up to 3 times)')
    args = argp.parse_args()
    check = nagiosplugin.Check(
        RRD(args),
        nagiosplugin.ScalarContext('munin', args.warning, args.critical),
        )
    check.name = args.name or args.module
    check.main(verbose=args.verbose)

if __name__ == '__main__':
    main()
