#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.


import logging
import polib
import urllib, json, re
from optparse import OptionParser


def read_parameters():
    parser = OptionParser()

    parser.add_option(
        "-s",
        "--source",
        action="store",
        type="string",
        dest="source_file",
        default="",
        help="Source file")

    parser.add_option(
        "-o",
        "--output",
        action="store",
        type="string",
        dest="output_file",
        default="",
        help="Output translated file as result of the process")

    (options, args) = parser.parse_args()

    if len(options.source_file) == 0 or len(options.output_file) == 0:
        print("Missing inputs file(s)")
        exit(1)

    return (options.source_file, options.output_file)
          
def main():

    print ("Clean up: fuzzy entries and comments")

    source_file, output_file = read_parameters()
    print ("Source file: " + source_file)
    print ("Output file: " + output_file)

    input_po = polib.pofile(source_file)
    for entry in input_po:
        entry.tcomment = ""

        if "fuzzy" in entry.flags:
            entry.msgstr = ""
            entry.flags.remove("fuzzy")

    input_po.save(output_file)


if __name__ == "__main__":
    main()
