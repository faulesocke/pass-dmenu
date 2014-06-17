#!/usr/bin/env python3

# Copyright (C) 2014  Urs Schulz
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os
import sys
import subprocess

from os.path import expanduser, expandvars, splitext, normpath, relpath
from os.path import join as joinpath


SEARCHPATH=normpath(expanduser("~/.password-store"))
DMENU_OPTIONS=["-p", "Password:", "-i", "-l", "35"]
PASS_OPTIONS=["-c"]


def main():
    def preppath(path):
        return splitext(relpath(path, SEARCHPATH))[0]

    def getext(path):
        return splitext(path)[1]

    pws = []

    for d, dirs, files in os.walk(SEARCHPATH):
        for f in files:
            if getext(f) != ".gpg":
                continue

            pws.append(preppath(joinpath(d, f)))


    print(pws)
    pws_str = "\n".join(pws)

    # launch dmenu
    try:
        result = subprocess.check_output(["dmenu"] + DMENU_OPTIONS, input=pws_str.encode())

    except subprocess.CalledProcessError as e:
        print("dmenu returned code %d. Output was: %s" % (e.returncode, e.output), file=sys.stderr)
        return 1

    result = result.decode().strip()

    if not result in pws:
        print("Invalid input", file=sys.stderr)
        return 1

    subprocess.call(["pass"] + PASS_OPTIONS + [result.encode()])


if __name__ == "__main__":
    main()

