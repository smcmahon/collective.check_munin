Introduction
============

This is a reimplementation of `check_munin_rrd.pl <https://code.google.com/p/nagios-munin/>`_ in Python.
It is used as a Nagios plugin command to read data collected from a Munin node by a Munin server.

It uses `rrdtool <http://oss.oetiker.ch/rrdtool/>`_ directly via "rrdtool lastupdate".
rrdtool is a dependency for Munin servers, so it should be reliably available.

Installation is typical for a Python package; virtualenv is recommended.

Run the check_munin script for options.
Command-line options allow you to set domain, host, Munin-node plugin module, various include/exclude filters, and warning/critical ranges.
Options generally match check_munin_rrd.
Differences: -o option values may be globs; warning/critical specifications may be ranges, e.g., "-w 0:85" for warn when outside 0-85 range.

Typical usage::

    check_munin -d dcn.org -H www.dcn.org -M df -o "_dev_*" -i _dev_shm -w 85 -c 95

This reads the /var/lib/munin/dcn.org/www.dcn.org RRD files for the "df" module, including only RRD df files that match _dev_* and excluding _dev_shm::

    /var/lib/munin/dcn.org/www.dcn.org-df-_dev_*-g.rrd

ignoring /var/lib/munin/dcn.org/www.dcn.org-df-_dev_shm-g.rrd

Sample output::

    DF WARNING - /dev/sdi is 87.75 (greater than 85) | '/dev/sda1'=42.0611407378;85;95;0 '/dev/sdb'=31.7252599179;85;95;0 '/dev/sdh'=41.0162765108;85;95;0 '/dev/sdi'=87.7540702356;85;95;0 '/dev/sdj'=56.5373419066;85;95;0 '/dev/sdk'=54.4599777102;85;95;0
