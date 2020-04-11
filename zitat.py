# -*- coding: utf-8 -*-
# !/usr/bin/env python

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
import re
from hamcrest import assert_that, equal_to, is_in

if sys.version_info < (3, 5):
    print("Zitat requires Python 3.5")
    sys.exit(1)

def kindle_timestamp_to_ISO_8601(timestamp):
    language_function_equivalence = {"Added on":   EN_kindle_timestamp_to_ISO_8601,
                                     "添加于":      ZH_kindle_timestamp_to_ISO_8601}

    for language_signature in language_function_equivalence:
        if re.search(language_signature, timestamp):
            return language_function_equivalence[language_signature](timestamp)


def get_EN_month(day_section):
    months_equivalence = {"January":   "01",
                          "February":  "02",
                          "March":     "03",
                          "April":     "04",
                          "May":       "05",
                          "June":      "06",
                          "July":      "07",
                          "August":    "08",
                          "September": "09",
                          "October":   "10",
                          "November":  "11",
                          "December":  "12"}
    for month in months_equivalence:
        if re.search(month, day_section):
            assert_that(len(months_equivalence[month]), equal_to(2))
            return months_equivalence[month]


def get_EN_day_section(kindle_timestamp):
    return re.search(r'.*?,(.*?),', kindle_timestamp).group(1)


def get_EN_year_time_section(kindle_timestamp):
    return re.search(r'.*?,.*?,(.*?)$', kindle_timestamp).group(1)


def get_EN_day(day_section):
    day = re.search(r'\d{1,2}$', day_section).group(0)
    if int(day) < 10:
        return "0" + day
    return day


def get_EN_year(year_time_section):
    return re.search(r'\s*(\d{4})', year_time_section).group(1)


def get_EN_period(year_time_section):
    return re.search(r'([A-Z]{2})$', year_time_section).group(1)


def get_EN_time(year_time_section):
    return re.search(r'(\d{1,2}:\d{2}:\d{2})\s..$', year_time_section).group(1)


def calculate_ISO_8601_date(year, month, day):
    return str(year) + "-" + str(month) + "-" + str(day)


def calculate_ISO_8601_time(unadjusted_time, period):
    partitioned_time = re.search(r'(\d{1,2}):(\d{2}:\d{2})$', unadjusted_time)
    unadjusted_hour = int(partitioned_time.group(1))
    minutes_and_seconds = partitioned_time.group(2)
    assert_that(len(minutes_and_seconds), equal_to(5))
    assert_that(period, is_in(["AM","PM"]))
    if period == "PM" and unadjusted_hour < 12:
        adjusted_hour = unadjusted_hour + 12
    else:
        adjusted_hour = unadjusted_hour
    return str(adjusted_hour) + ":" + minutes_and_seconds


def EN_kindle_timestamp_to_ISO_8601(EN_kindle_timestamp):
    '''
    Returns an org formatted timestamp
    :param kindletimestamp: the kindle timestamp in whatever language
    '''
    year_time_section = get_EN_year_time_section(EN_kindle_timestamp)
    day_section = get_EN_day_section(EN_kindle_timestamp)

    year = get_EN_year(year_time_section)
    month = get_EN_month(day_section)
    day = get_EN_day(day_section)

    unadjusted_time = get_EN_time(year_time_section)
    period = get_EN_period(year_time_section)

    date = calculate_ISO_8601_date(year, month, day)
    assert_that(len(date), equal_to(10))

    time = calculate_ISO_8601_time(unadjusted_time, period)
    assert_that(len(time), is_in([7, 8]))

    return "[" + date + " " + time + "]"


def get_ZH_month(ZH_kindle_timestamp):
    month = re.search(r'(\d{1,2})月', ZH_kindle_timestamp).group(1)
    if int(month) < 10:
        return "0" + month
    return month


def get_ZH_day(ZH_kindle_timestamp):
    day = re.search(r'(\d{1,2})日', ZH_kindle_timestamp).group(1)
    if int(day) < 10:
        return "0" + day
    return day


def get_ZH_year(ZH_kindle_timestamp):
    return re.search(r'(\d{4})年', ZH_kindle_timestamp).group(1)


def get_ZH_period(ZH_kindle_timestamp):
    if re.search(r'(.)午', ZH_kindle_timestamp).group(1) == "下":
        return "PM"
    return "AM"


def get_ZH_time(ZH_kindle_timestamp):
    return re.search(r'午(\d{1,2}:\d{2}:\d{2})$', ZH_kindle_timestamp).group(1)


def ZH_kindle_timestamp_to_ISO_8601(ZH_kindle_timestamp):
    '''
    Returns sorted list of clippings (same title, same type) by location in
    ascending order. Ignores leading 'Page ' or 'Loc. '. Converts from roman
    numerals (for pages) to numbers (but romans must come before numbers). Also,
    if it is a range, consider only the digits before the dash.
    :param kindletimestamp: the kindle timestamp in whatever language
    '''
    year = get_ZH_year(ZH_kindle_timestamp)
    month = get_ZH_month(ZH_kindle_timestamp)
    day = get_ZH_day(ZH_kindle_timestamp)

    unadjusted_time = get_ZH_time(ZH_kindle_timestamp)
    period = get_ZH_period(ZH_kindle_timestamp)

    date = calculate_ISO_8601_date(year, month, day)
    time = calculate_ISO_8601_time(unadjusted_time, period)

    return "[" + date + " " + time + "]"


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
        with open(filename, mode='r', encoding='utf-8-sig') as in_file:
            file_as_string = in_file.read()
        return file_as_string
    except IOError:
        print('Error reading ' + filename + '.')
        print('Exiting.')
        sys.exit(1)


def get_data(clippings):
    '''
    Return a tuple with author, title, cltype, location, date, and content of a clipping.
    :param c: clipping to process.
    '''

    lines = clippings.split("\n")

# ===============================================================================
#   author is between parentheses at the end of line 0.
# ===============================================================================
# If no closing parenthesis, author is 'Unknown'.
    if lines[0][-1] != ')':
        author = u'Unknown'
    else:
        position = lines[0].rfind('(')
        # If closing but no opening paren (malformed line), author is 'Unknown'.
        if position == -1:
            author = u'Unknown'
        else:
            author = lines[0][position + 1:-1].strip()

# ===============================================================================
#   title is from beginning of line 0 to just before rightmost '('.
# ===============================================================================
# If no closing parenthesis, the whole line is the title.
    if lines[0][-1] != ')':
        title = lines[0].strip()
    else:
        position = lines[0].rfind('(')
        if position == -1:
            position = len(lines[1])
        title = lines[0][:position].strip()

# ===============================================================================
#   Line 1 is a sequence of fields separated by '|'.
#   Field 0 starts with '- ', which we strip (dashes and spaces).
# ===============================================================================
    fields = [s.strip(' -') for s in lines[1].split('|')]

    # cltype is first word of first field.
    words = fields[0].split()

    # location is word 1 or 2. If word 1 is 'on', then word 2 is 'Page'.
    if words[1] == 'on':
        location = ' '.join(words[2:])
    else:
        location = ' '.join(words[1:])

    # date is last field.
    date = kindle_timestamp_to_ISO_8601(fields[-1])

# ===============================================================================
# Line 2 is always blank. Line 3 is the contents.
# ===============================================================================
    content = lines[3].strip()

    return author, title, location, date, content


def process_clipping(authors, clipping):
    '''
    If clipping is of a suitable type, insert it in the dictionary.
    :param authors: the main dictionary.
    :param c: the clipping to process.
    '''

    author, title, location, date, content = get_data(clipping)

    # Move articles to the end of the title. All determiners must be all
    # lowercase and end with a space for this to work.
    determiners = ('the ',  # English
                   'a ',
                   'an ',
                   'el ',   # Spanish
                   'la ',
                   'los ',
                   'las ',
                   'o ',    # Portuguese
                   'os ',
                   'as ',
                   'le ',   # French
                   'les ',
                   'la ',
                   'der ',  # German
                   'die ',
                   'das ')
    if title.lower().startswith(determiners):
        position = title.find(' ')
        title = title[position + 1:] + ', ' + title[:position]

    # Get or create author entry (a dict of titles -> cltypes) in main dictionary.
    author_entry = authors.setdefault(author, {})

    # Get or create title entry (a list of clippings) in that author's dictionary.
    title_list = author_entry.setdefault(title, [])

    # New clipping becomes a tuple.
    new_entry = (location, date, content)

    # Append new tuple to the list.
    title_list.append(new_entry)


def parse_kindle_clippings(clippings_string):
    '''
    Populate dictionary with contents of clippings string. Return dictionary.
    :param filename: input filename.
    '''

    # Split into list of clippings. Discard last, empty clipping.
    clipping_separator = '\n==========\n'
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
    keys = sorted(keys, key=str.lower)
    return [(key, adict[key]) for key in keys]


def format_author_to_org(author):
    """
    Format title heading.
    """
    return u'* {}\n'.format(author)


def format_title_to_org(title):
    """
    Format title heading.
    """
    return u'** {}\n'.format(title)


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


def format_content_to_org(clipping):
    '''
    Format a single clipping to org mode.
    :param c: clipping.
    '''
    location, date, content = clipping

    hd_fill_col = 58
    headline = u'*** {} --\n'.format(snippet(content, hd_fill_col))

    location_and_date = u'\n/{}. {}./\n'. format(location, date)

    return headline + content + location_and_date


def kindle_clippings_to_org(kindle_clippings_string):
    # Sort dictionary by Author | Title | Type | Location
    # The last key is part of the content tuples.
    # Note that sorted dicts become lists of values!!!

    kindle_clippings_string = kindle_clippings_string.replace(u'\ufeff', '')
    org_clippings = str()
    clippings_dict = parse_kindle_clippings(kindle_clippings_string)

    sorted_authors = sorted_dict(clippings_dict)
    for author, author_entry in sorted_authors:
        org_clippings += format_author_to_org(author)
        sorted_titles = sorted_dict(author_entry)
        for title, title_highlights in sorted_titles:
            org_clippings += format_title_to_org(title)
            title_highlights = sort_clipping_list(title_highlights)
            for clipping in title_highlights:
                org_clippings += format_content_to_org(clipping)
    return org_clippings


def roman_to_int(roman_number):
    '''
    Convert roman number to int (from http://code.activestate.com/recipes/81611-roman-numerals/).
    :param n: string containing roman number.
    '''

    numeral_map = zip(
        (1000, 900, 500,  400, 100,   90,  50,   40,  10,    9,   5,    4,   1),
        ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
    )

    roman_number = roman_number.upper()

    i = result = 0
    for integer, numeral in numeral_map:
        while roman_number[i:i + len(numeral)] == numeral:
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


def write_to_org_file(org_clippings_string, out_filename):
    '''
    Export contents of dictionary to org text file.
    :param clippings: main dictionary.
    :param out_filename: output filename.
    '''

    try:
        with codecs.open(out_filename, 'w', encoding='utf-8') as out_file:
            out_file.write(org_clippings_string)
    except IOError:
        print('Error writing ' + out_filename + '.')
        print('Exiting.')
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
        input_filename = input('Enter input filename below:\n>>> ').strip()

    if input_filename == '':
        print('No input filename given. Exiting.')
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
        output_filename = input(
            'Enter output filename below [{}]:\n>>> '.format(output_filename_sugg)).strip()
        if output_filename == '':
            output_filename = output_filename_sugg

    # Read file intro string
    print('Reading', input_filename + '.')
    kindle_clippings_string = open_clippings_file(input_filename)
    # Convert kindle string to org mode string
    org_clippings_string = kindle_clippings_to_org(kindle_clippings_string)

    # Write org mode string to output file.
    print('Writing', output_filename + '.')
    write_to_org_file(org_clippings_string, output_filename)
    print('Done.\n')


if __name__ == '__main__':
    zitat(sys.argv)
