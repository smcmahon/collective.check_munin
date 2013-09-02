Introduction
============

This is a reimplementation of check_munin_rrd.pl in python.

It uses rrdtool directly via "rrdtool lastupdate".

Installation is typical for a Python package; virtualenv is recommended.

Run the check_munin script for options.

Typical usage::

    check_munin -d dcn.org -H www.dcn.org -M df -o "_dev_*" -i _dev_shm -w 85 -c 95

This reads the /var/lib/munin/dcn.org/www.dcn.org RRD files for the "df" module, including only RRD df files that match _dev_* and excluding _dev_shm.
