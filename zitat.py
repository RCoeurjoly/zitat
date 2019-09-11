#!/usr/bin/env python

#   zitat.py: reads and converts Kindle clippings files.
#   Version 1.0
#   Copyright (C) 2012  Sag Alles Ab <sagallesab2@gmail.com>
#
#   URL: http://sagallesab.wordpress.com/zitat
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, visit the URL
#   http://www.gnu.org/licenses/gpl.html

'''
zytat.py: reads and converts Kindle clippings files.
Version 1.0
Created Oct 2012

URL: http://sagallesab.wordpress.com/zitat

@author: sagallesab2 at gmail.com

'''
import codecs
import sys
import time


def open_clippings_file(filename):
    '''
    Try to open file and read it into one unicode string. Return string.
    :param filename: input filename.
    '''

    # Must read the file as utf-8-sig. The reason is explained in
    # http://docs.python.org/library/codecs.html#encodings-and-unicode:
    #
    # "To increase the reliability with which a UTF-8 encoding can be detected,
    #  Microsoft invented a variant of UTF-8 (that Python 2.5 calls "utf-8-sig")
    #  for its Notepad program: Before any of the Unicode characters is written
    #  to the file, a UTF-8 encoded BOM (which looks like this as a byte
    #  sequence: 0xef, 0xbb, 0xbf) is written."
    #
    # This is Amazon following in Microsoft's footsteps... A bad sign.

    try:
        in_file = open(filename)
        file_as_string = unicode(in_file.read(), 'utf-8-sig')
        in_file.close()
        return file_as_string
    except IOError:
        print 'Error reading ' + filename + '.'
        print 'Exiting.'
        sys.exit(1)


def get_data(clippings):
    '''
    Return a tuple with author, title, cltype, location, date, and content of a clipping.
    :param c: clipping to process.
    '''

    lines = clippings.split("\r\n")

#===============================================================================
#   author is between parentheses at the end of line 0.
#===============================================================================
# If no closing parenthesis, author is 'Unknown'.
    if lines[0][-1] != ')':
        author = u'Unknown'
    else:
        position = lines[0].rfind('(')
        # If closing but no opening paren (malformed line), author is 'Unknown'.
        if position == -1:
            author = u'Unknown'
        else:
            author = lines[0][position + 1:-1]

#===============================================================================
#   title is from beginning of line 0 to just before rightmost '('.
#===============================================================================
# If no closing parenthesis, the whole line is the title.
    if lines[0][-1] != ')':
        title = lines[0].strip()
    else:
        position = lines[0].rfind('(')
        if position == -1:
            position = len(lines[1])
        title = lines[0][:position].strip()

#===============================================================================
#   Line 1 is a sequence of fields separated by '|'.
#   Field 0 starts with '- ', which we strip (dashes and spaces).
#===============================================================================
    fields = [s.strip(' -') for s in lines[1].split('|')]

    # cltype is first word of first field.
    words = fields[0].split()
    cltype = words[0]

    # location is word 1 or 2. If word 1 is 'on', then word 2 is 'Page'.
    if words[1] == 'on':
        location = ' '.join(words[2:])
    else:
        location = ' '.join(words[1:])

    # date is last field.
    date = fields[-1]

#===============================================================================
# Line 2 is always blank. Line 3 is the contents.
#===============================================================================
    content = lines[3]
    titulo = title
    return author, titulo, cltype, location, date, content


def process_clipping(authors, clipping):
    '''
    If clipping is of a suitable type, insert it in the dictionary.
    :param authors: the main dictionary.
    :param c: the clipping to process.
    '''

    author, title, cltype, location, date, content = get_data(clipping)

    # We process everything but Bookmarks (which have no text anyway).
    if cltype in ['Bookmark']:
        return

    # Move articles to the end of the title. All determiners must be all
    # lowercase and end with a space for this to work.
    determiners = ('the ',
                   'a ',
                   'an ',
                   'o ',
                   'os ',
                   'as ',
                   'le ',
                   'les ',
                   'la ',
                   'der ',
                   'die ',
                   'das ')
    if title.lower().startswith(determiners):
        position = title.find(' ')
        title = title[position + 1:] + ', ' + title[:position]

    # Get or create author entry (a dict of titles -> cltypes) in main dictionary.
    author_entry = authors.setdefault(author, {})

    # Get or create title entry (a dict of cltypes->lists of clippings) in that author's dictionary.
    title_entry = author_entry.setdefault(title, {})

    # Get or create cltype entry (a list of clippings) in that title's dictionary.
    cltype_list = title_entry.setdefault(cltype, [])

    # New clipping becomes a tuple.
    new_entry = (location, date, content)

    # Append new tuple to the list.
    cltype_list.append(new_entry)


def import_clippings_file(filename):
    '''
    Populate dictionary with contents of input file. Return dictionary.
    :param filename: input filename.
    '''

    # Open and read file into string.
    clippings_string = open_clippings_file(filename)

    # Split into list of clippings. Discard last, empty clipping.
    clipping_separator = '\r\n==========\r\n'
    clipping_list = clippings_string.split(clipping_separator)[:-1]

    # Initialize dictionary and process each clipping.
    authors = {}
    for clipping in clipping_list:
        process_clipping(authors, clipping)

    return authors


def sorted_dict(adict):
    '''
    Return a sorted ***list*** of pairs (k,v) of adict's contents.
    The sort is case-insensitive.
    IMPORTANT: keys must all be strings.
    :param adict:
    '''
    keys = adict.keys()
    keys[:] = sorted(keys, key=unicode.lower)
    return [(key, adict[key]) for key in keys]


def export_author_org(author, out_file):
    """
    Write title heading.
    """
    heading = u'* {}\n\n'.format(author)
    out_file.write(heading)


def export_title_org(title, out_file):
    """
    Write title heading.
    """
    heading = u'** {}\n\n'.format(title)
    out_file.write(heading)


def export_type_org(typ, out_file):
    '''
    Write type heading.
    '''
    heading = u'*** {}\n\n'.format(typ)
    out_file.write(heading)


def snippet(clipping, length):
    '''
    Return prefix of clipping that is at most length chars long.
    '''

    # s shorter than n, return entire s.
    if len(clipping) <= length:
        return clipping

    prefix = clipping.rfind(' ', 0, length + 1)
    if prefix == -1:
        # No spaces in prefix! Truncate at n.
        return clipping[:length]
    else:
        return clipping[:prefix]


def export_content_org(clipping, out_file):
    '''
    Export a single clipping to the output org file.
    :param c: clipping.
    :param f: output file.
    '''

    loc, dat, content = clipping

    hd_fill_col = 58

    headline = u'*** {} --\n\n'.format(snippet(content, hd_fill_col))
    out_file.write(headline)

    out_file.write(content + '\n\n')

    out_file.write(u'/{}. {}./\n\n'. format(loc, dat))

    out_file.flush()


def roman_to_int(number):
    '''
    Convert roman number to int (from http://code.activestate.com/recipes/81611-roman-numerals/).
    :param n: string containing roman number.
    '''

    numeral_map = zip(
        (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
        ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
    )

    number = number.upper()

    i = result = 0
    for integer, numeral in numeral_map:
        while number[i:i + len(numeral)] == numeral:
            result += integer
            i += len(numeral)

    return result


def compute_srt_location(clippings):
    '''
    Convert location to an integer for sorting. Handles ranges (taking only the
    lower bound). Handles roman numerals (which must come before arabic numbers).
    :param c: a tuple of the form (location, date, content)
    '''

    location = clippings[0]

    # Strip leading 'Page ' or 'Loc. '.
    page = location.find(' ')
    location = location[page + 1:]

    # Strip upper bound of range, if there.
    page = location.find('-')
    if page > -1:
        location = location[:page]

    # Convert to int.
    if location.isnumeric():
        ret = int(location)
    else:
        # Treat as roman numeral.
        # Subtract 10000 to make it sort before arabic numbers.
        ret = roman_to_int(location) - 10000

    return ret


def sort_clipping_list(clippings):
    '''
    Returns sorted list of clippings (same title, same type) by location in
    ascending order. Ignores leading 'Page ' or 'Loc. '. Converts from roman
    numerals (for pages) to numbers (but romans must come before numbers). Also,
    if it is a range, consider only the digits before the dash.
    :param clippings: list of tuples of the form (location, date, content)
    '''

    return sorted(clippings, key=compute_srt_location)


def export_to_org(clippings, out_filename, in_filename):
    '''
    Export contents of dictionary to org text file.
    :param clippings: main dictionary.
    :param out_filename: output filename.
    '''

    try:
        out_file = codecs.open(out_filename, 'w', encoding='utf-8')

        # Write a couple of empty lines and info about file.
        out_file.write(u'\n\n')
        out_file.write(u'Generated from clippings in file ' + in_filename + '\n')
        out_file.write(u'on ' + time.strftime('%Y-%m-%d %H:%M:%S %Z') + '\n')
        out_file.write(u'by the zitat script (http://sagallesab.wordpress.com/zitat).')
        out_file.write(u'\n\n\n')

        # Sort dictionary by Author | Title | Type | Location
        # The last key is part of the content tuples.
        # Note that sorted dicts become lists of values!!!
        sorted_authors = sorted_dict(clippings)
        for author, author_entry in sorted_authors:
            export_author_org(author, out_file)
            sorted_titles = sorted_dict(author_entry)
            for title, title_entry in sorted_titles:
                export_title_org(title, out_file)
                sorted_types = sorted_dict(title_entry)
                title_highlights = list()
                for typ, type_entry in sorted_types:
                    # export_type_org(typ, out_file)
                    typ += ''
                    title_highlights += type_entry
                title_highlights = sort_clipping_list(title_highlights)
                for clipping in title_highlights:
                    export_content_org(clipping, out_file)
        out_file.close()
    except IOError:
        print 'Error writing ' + out_filename + '.'
        print 'Exiting.'
        sys.exit(1)


def zitat(argv):
    '''
    Main function: open and read kindle clippings file and import all clippings
    from it, populating a dictionary. Then export dictionary to text file.
    :param argv: command line args.
    '''

    if len(argv) >= 2:
        # If given, first cmdln arg is input filename.
        input_filename = argv[1]
    else:
        # Get from keyboard.
        input_filename = raw_input('Enter input filename below:\n>>> ').strip()

    if input_filename == '':
        print 'No input filename given. Exiting.'
        sys.exit(1)

    # If second arg given, it is output file name.
    if len(argv) > 2:
        output_filename = argv[2]
    else:
        # Compute suggested output filename.
        output_extension = '.org'
        dot_pos = input_filename.rfind('.')
        if dot_pos >= 0:
            output_filename_sugg = input_filename[:dot_pos] + output_extension
        else:
            output_filename_sugg = input_filename + output_extension

        # Get from keyboard, offering suggestion (input file with .org extension).
        output_filename = raw_input(
            'Enter output filename below [{}]:\n>>> '.format(output_filename_sugg)).strip()
        if output_filename == '':
            output_filename = output_filename_sugg

    # Open file and import it to dictionary.
    print 'Reading', input_filename + '.'
    clippings = import_clippings_file(input_filename)

    # Export contents of dictionary to output file.
    print 'Writing', output_filename + '.'
    export_to_org(clippings, output_filename, input_filename)
    print 'Done.\n'


if __name__ == '__main__':
    zitat(sys.argv)