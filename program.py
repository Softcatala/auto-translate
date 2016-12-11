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

def _load_po_into_dictionary(filename):
    strings = {}
    input_po = polib.pofile(filename)

    for entry in input_po:
        if entry.msgstr is '' or '@@image' in entry.msgid:
            continue

        strings[entry.msgid] = _parse_accents(entry.msgstr); 

    print("Read Spanish sentences:" + str(len(strings)))
    return strings

def _parse_accents(string):
    string = string.replace(u"í",u'í')
    string = string.replace(u"á",u'á')
    string = string.replace(u"é",u'é')
    string = string.replace(u"ó",u'ó')
    string = string.replace(u"ú",u'ú')
    string = string.replace(u"ñ",u'ñ')  
    return string

def _get_marker(pos):
    return " MATCH-" + str(pos) + " "

def _get_marker_lastline(pos):
    return " MATCH-" + str(pos)

def _get_translation(text):
    
    # Request translation
    url = "https://www.softcatala.org/apertium/json/translate?langpair=es|ca&markUnknown=no"
    url += "&q=" + urllib.quote_plus(text.encode('utf-8'));
    print "url->" + url

    response = urllib.urlopen(url)
    data = json.loads(response.read())
    translated =  data['responseData']['translatedText']
    print ("Translated (returned):" + translated.encode("utf-8"))
    return translated

def _translate_from_spanish(text):

    # Create markers for HTML marks
    markers = []

    regex = re.compile(r"\<(.*?)\>", re.VERBOSE)
    matches = regex.findall(text)
    pos = 0
    for match in matches:
        match = '<' + match + '>'
        text = text.replace(match, _get_marker(pos), 1)
        markers.append(match)
        pos = pos + 1

    translated = _get_translation(text)
   
    # Put back markers
    pos = 0
    for mark in markers:
        translated = translated.replace(_get_marker(pos), mark, 1) 
        translated = translated.replace(_get_marker_lastline(pos), mark, 1) 
        pos = pos + 1
    
    print ("Translated:" + translated.encode("utf-8"))
    return translated

def read_parameters():
    parser = OptionParser()

    parser.add_option(
        "-s",
        "--source",
        action="store",
        type="string",
        dest="source_file",
        default="",
        help="Source file in Catalan (not or partially translated)")

    parser.add_option(
        "-t",
        "--translated",
        action="store",
        type="string",
        dest="translated_file",
        default="",
        help="Source file in Spanish (translated)")

    parser.add_option(
        "-o",
        "--output",
        action="store",
        type="string",
        dest="output_file",
        default="",
        help="Output translated file as result of the process")

    (options, args) = parser.parse_args()

    if len(options.source_file) == 0 or len(options.translated_file) == 0 or\
       len(options.output_file) == 0:
        print("Missing inputs file(s)")
        exit(1)

    return (options.source_file, options.translated_file,
            options.output_file)

words = None

def _word_replacement(string):

    global words

    if words is None:
        words = {}
        with open('word-replace.txt') as f:
            print ("Read word-replace.txt")
            lines = f.readlines()
            for line in lines:
                source, target = line.split(',')
                words[unicode(source, "utf-8")] = unicode(target, "utf-8")
               
    for key in words.keys():
        string = string.replace(key, words[key])

    return string

def main():

    print ("Translates using Other languages translations")

    source_file, translated_file, output_file = read_parameters()
    print ("Source file: " + source_file)
    print ("Translated file: " + translated_file)
    print ("Output file: " + output_file)

    # Create a dictionary with translated segments in Spanish
    strings = _load_po_into_dictionary(translated_file)

    input_po = polib.pofile(source_file)
    cnt = 0
    for entry in input_po:

        if len(entry.msgstr) > 0:
            continue
        
        if entry.msgid not in strings:
            continue
        
        cnt = cnt + 1

        sp = _parse_accents(strings[entry.msgid])
        translated = _translate_from_spanish(sp)
        translated = _word_replacement(translated)
        entry.msgstr = translated
        print("{0} [en] -> {1} [es] -> {2} [ca]".format(entry.msgid.encode('utf-8'), 
                                  sp.encode('utf-8'),
                                  translated.encode('utf-8')))

        entry.tcomment = "auto-translated"
        entry.flags.append("fuzzy")

    input_po.save(output_file)
    print ("Auto translated strings" + str(cnt))


if __name__ == "__main__":
    main()
