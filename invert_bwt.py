''' INVERT BURROWS-WHEELER TRANSFORM
----------------
Global variables
----------------
alphabet
    all the alphanumerical characters and space for now.

----------------------------------------------
Functions for invert_bwt and their description
----------------------------------------------
invert_bwt_via_map
    Takes a bwt string and returns the text it was encoded from.
    This function works by creating a last-first map for the bwt.
    Works in O[n log n] time.
sort_string
    Takes a string astr, sorts its characters lexicographically and
    returns the sorted string.
build_map
    This function takes a string and returns a map of bwt to its true
    index (called the last-first map)
text_using_map
    This function takes bwt, it's last-first map and returns the original
        text the bwt is encoded from (including EOF $).

----------------------------------------
Functions for main and their description
----------------------------------------
print_help()
    Prints help message for the decoding function.
process_file
    Takes a file path (str) and returns a new file with the same name but
    extension of .txt. If not one_word, the B-W invert of each line is placed
    on the same line in the output file.
decode_file_as_word_list
    Takes a path for a file input_file (str) and creates a tuple of decodings
    corresponding to the words in the file at the path.
validate_bwt
    Validates bwt with two tests:
    Checks to see if the string has only one symbol.
        If there are no symbols returns an error message
        If there are more than one symbols returns a different error messsage.
    If there is exactly one symbol, replaces it with end_char and returns
    string.
'''

from collections import deque
import os
from common import (
    all_chars_in_alphabet,
    authenticate,
    check_args_for_help,
    get_file_path,
    get_string,
    validate_file
    )

# GLOBAL VARIABLES
ALPHABET = set()
# add whitespace
ALPHABET.add(chr(32))
# add numbers 0 - 9
for val in range(48, 48+10):
    ALPHABET.add(chr(val))
# add A-Z
for val in range(65, 65+26):
    ALPHABET.add(chr(val))
# add a-z
for val in range(97, 97+26):
    ALPHABET.add(chr(val))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Functions for invert_bwt_via_map #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def sort_string(astr: str) -> str:
    '''Takes a string astr, sorts its characters lexicographically and
    returns the sorted string.

    Examples:
        >>> sort_string('')
        ''
        >>> sort_string('a')
        'a'
        >>> sort_string('ipssm$pissii')
        '$iiiimppssss'
        >>> sort_string('3s$ avrraakd')
        ' $3aaadkrrsv'
        >>> sort_string('annb$aa')
        '$aaabnn'
    '''
    astr_sorted = [i for i in astr]
    astr_sorted.sort()
    astr_sorted = ''.join(astr_sorted)
    return astr_sorted


def build_map(last: str) -> tuple:
    '''This function takes a bwt and returns a bijective L-F map as a tuple.

    Params:
    bwt(str)    the string to be inverted to original text

    Returns:
    tuple       true index stored at the curent index

    Calls:
    sort_string

    Examples
    >>> build_map('$')
    (0,)
    >>> build_map('ipssm$pissii')
    (5, 0, 7, 10, 11, 4, 1, 6, 2, 3, 8, 9)
    >>> build_map('k$avrraad')
    (1, 2, 6, 7, 8, 0, 4, 5, 3)
    >>> build_map('annb$aa')
    (4, 0, 5, 6, 3, 1, 2)
    >>> build_map('3s$ avrraakd')
    (3, 2, 0, 4, 8, 9, 11, 10, 6, 7, 1, 5)
    '''
    # sort last or bwt to get first
    first = sort_string(last)
    # make a map of char to queue of indices of char in last 
    d = dict()
    for i in range(len(last)):
        char = last[i]
        if char not in d:
            d[char] = deque([i])
        else:
            d[char].append(i)
    # lf_map will map the index in first to the index in first that precedes it
    # in the original text
    lf_map = []
    for c in first:
        i = d[c].popleft()
        lf_map.append(i)
    # return a tuple
    lf_map = tuple(lf_map)
    return lf_map


def text_using_map(bwt: str, lf_map: tuple, end_char: str = '$') -> str:
    '''This function takes bwt, it's last-first map and returns the original
    string bwt is encoded from.

    Params:
    bwt (str)       the string to be inverted to original text
    lf_map (list of ints)
                    the last-first map of the bwt
    end_char (str)  EOF character, default value is '$'

    Returns:
    str         the text bwt was encoded from including the $.

    Examples
    >>> text_using_map('$', (0, ))
    '$'
    >>> text_using_map('ipssm$pissii', \
(5, 0, 7, 10, 11, 4, 1, 6, 2, 3, 8, 9))
    'mississippi$'
    >>> text_using_map('k$avrraad', \
(1, 2, 6, 7, 8, 0, 4, 5, 3))
    'aardvark$'
    >>> text_using_map('annb$aa', \
(4, 0, 5, 6, 3, 1, 2))
    'banana$'
    >>> text_using_map('3s$ avrraakd', \
(3, 2, 0, 4, 8, 9, 11, 10, 6, 7, 1, 5))
    '3 aardvarks$'
    '''
    text = ['' for _ in bwt]
    # find the place of the original string in the sorted rotations as
    #   the place of end_char in bwt the last column of rotations.
    x = bwt.index(end_char)
    # create an empty list to be filled with correct order of characters
    text = ['' for _ in bwt]
    # fill text
    for i in range(len(bwt)):
        x = lf_map[x]
        text[i] = bwt[x]
    # return text as a string
    return ''.join(text)


def invert_bwt_via_map(bwt: str, end_char: str = '$') -> str:
    '''
    Takes a bwt string and returns the text it was encoded from.

    This function runs in O(n log n) asymptotically. The rate limiting
    step is sorting the bwt.

    Params:
    bwt        str
    end_char   str, EOF character, default value is '$'

    Returns:
    str       bwt decoded to the original text.

    Calls:
    build_map
    text_from_map

    Examples:
    >>> invert_bwt_via_map('$')
    ''
    >>> invert_bwt_via_map('a$')
    'a'
    >>> invert_bwt_via_map('ipssm$pissii')
    'mississippi'
    >>> invert_bwt_via_map('k$avrraad')
    'aardvark'
    >>> invert_bwt_via_map('3s$ avrraakd')
    '3 aardvarks'
    >>> invert_bwt_via_map('annb$aa')
    'banana'
    '''
    # build a last-first map
    lf_map = build_map(bwt)
    # get text from last-first map, includes end_char at the end
    text = text_using_map(bwt, lf_map)
    return text[:-1]


# ~~~~ #
# Main #
# ~~~~ #


def print_help() -> None:
    '''
    Prints help message for the decoding function.
    '''
    print('')
    print('')
    print("Usage: python3 invert_bwt [-h|--help] \
[-s bwt_string | -f filename]")
    print("")
    print("Options:")
    print("-h | --help")
    print("    Prints this message and exits.")
    print("-f filename")
    print("    * Following -f provide path to the file_name.bwt to decode.")
    print("    * The function expects a file of size 1 MB or smaller.")
    print("    * The function expects only alphanumericals and spaces,")
    print("      other than a single EOF symbol, usually '$'.")
    print("    * Decoded text is always stored at the same path and file name")
    print("      but with an extension of .txt.")
    print("    * If the decoding works function returns True, else None.")
    print("-s 'bwt_text'")
    print("    * Function looks for -f first then -s.")
    print("      If -f is found -s is ignored.")
    print("    * Following -s provide the string to decode.")
    print("    * Please enclose the string in single quotes ('). E.g. 'tex$t'")
    print("    * The function expects only alphanumerical and spaces,")
    print("      other than a single EOF symbol, usually $")
    print("    * If the dencoding works function returns a string, else None")
    print("    * The functions saves nothing.")
    print('')
    print('')


def validate_bwt(string: str, line_no: int = None, end_char: str = '$') -> str:
    '''
    Validates bwt with checks to see if the string has only one symbol.
    If there are no symbols returns an error message.
    If there are more than one symbols returns a different error messsage.
    If there is exactly one symbol, replaces it with `end_char` and returns a
    string.

    Params:
    bwt (str)       the burrows-wheeler transform to be decoded.
    line_no (int)   in case processing file being treated as words
                    separated by '\n'.
    end_char        the special EOF character, default value is '$'.

    Returns:
    bwt (str)       if it passes all validation tests.
    error string        if the bwt has no symbols, or more than one symbols

    Examples:
    >>> validate_bwt('')
    'String has no symbols.'
    >>> validate_bwt(' ')
    'String has no symbols.'
    >>> validate_bwt('$')
    '$'
    >>> validate_bwt('ababs')
    'String has no symbols.'
    >>> validate_bwt('ababs', 10)
    'Line no. 10 has no symbols.'
    >>> validate_bwt('a$bab$s')
    'String has more than one symbols.'
    >>> validate_bwt('a$bab$s', 10)
    'Line no. 10 has more than one symbols.'
    >>> validate_bwt('abab$s')
    'abab$s'
    >>> validate_bwt('abab$s', 10)
    'abab$s'
    '''
    # counting non-space alphanumeric characters and saving their indices
    indices_non = []
    n = len(string)
    for i in range(n):
        if string[i] in ALPHABET:
            continue
        indices_non.append(i)
    if len(indices_non) == 0:
        if line_no:     # being used in a file
            return f'Line no. {line_no} has no symbols.'
        else:           # being used as a string
            return 'String has no symbols.'
        return
    if len(indices_non) > 1:
        if line_no:     # being used in a file
            return f'Line no. {line_no} has more than one symbols.'
        else:           # being used as a string
            return 'String has more than one symbols.'
    # if only one symbol, replace it with end_char
    i = indices_non[0]
    bwt = string[:i] + end_char + string[i+1:]
    return bwt


def decode_file_as_word_list(input_file: str,
                             end_char: str = '$') -> tuple:
    '''
    Takes a path for a file input_file (str) and a user provided EOF `end_str`.
    If any of the words in the file is not processed, prints to the terminal.
    Returns a tuple of strings corresponding to the words in the file
    at the path or a message (str) if the file is not processed.
    '''
    try:       # try and except for some error in reading the file
        output_list = []
        with open(input_file, 'r') as f_in:
            counter = 0
            for raw_bwt in f_in:
                # leading and trailing spaces may be a part of the transform
                # strip only the newline character
                raw_bwt = raw_bwt.strip('\n')
                try:    # try and except for each line
                    bwt = validate_bwt(raw_bwt, counter)
                    if bwt == raw_bwt:
                        temp_text = invert_bwt_via_map(bwt, end_char=end_char)
                        if authenticate(bwt, temp_text, end_char=end_char):
                            text = temp_text
                        else:
                            print(f"Error while processing line no. {counter}:\
unable to encode to BWT.")
                            text = ''
                    else:   # error
                        print(bwt)
                        text = ''
                except Exception as e:
                    print(f"Error in line no. {counter}: {e}")
                    text = ''
                output_list.append(text)
                counter += 1
        return tuple(output_list)
    except Exception as e:
        return e


def process_file(input_file: str,
                 end_char: str = '$',
                 one_word: bool = False) -> bool | str:
    '''
    Takes a file path `input_file`(str), a user provided EOF `end_char`, and
    a boolean `one_word`. Creates a new file with the same name but extension
    of .txt.
    If not `one_word`, the B-W invert of each line is placed on the
    same line in the output file.
    Returns a boolean True if all works well, else a `str` error.

    Params:
    input_file (str)    path to the input file.
    end_char (str)      EOF character, '$'by default.
    one_word (bool)     True, the whole file should be considered one word,
                        rather than the default of False.
                        False, the file should be considered a list of words,
                        separated by '\n' or newline characters.

    Output:
    Write a file in the same folder as the input_file with the same name but
        with extension .txt.
    Prints on the terminal if:
        any line has no symbols.
        any line has more than one symbol.
    '''
    if one_word:    # defunt for now, kept here for the sake of completeness.
                    # signal to deal with the whole file as one word.
        pass
    else:
        try:
            output_tuple = decode_file_as_word_list(
                input_file,
                end_char=end_char)
            if not isinstance(output_tuple, tuple):     # error
                return output_tuple
            output_file = input_file[:-4] + '.txt'
            with open(output_file, 'w') as f:
                for text in output_tuple:
                    f.write(text + '\n')
            return True
        except Exception as e:
            return e


def main(argv: tuple) -> str:
    # help block
    argv = tuple(argv)
    if check_args_for_help(argv):
        print_help()
        return

    # file block
    if '-f' in argv:
        file_path = get_file_path(argv)
        if not file_path:
            print('\n\nNo file provided.')
            print_help()
            return
        input_file = validate_file(file_path, '.bwt')
        if input_file != file_path:     # error
            print('\n\n')
            print(input_file)
            print_help()
            return
        status = process_file(input_file)
        if status is True:
            output_file = input_file[:-4] + '.txt'
            print(f'Output file is saved as {output_file}.')
            return True
        #else:       # status is a string
        print(status)
        return

    # string block
    if '-s' in argv:
        string = get_string(argv)
        if not string:
            print('\n\nNo string provided.')
            print_help()
            return
        bwt = validate_bwt(string)
        if bwt != string:
            print(bwt)
            print_help()
            return
        try:
            temp_text = invert_bwt_via_map(bwt)
            if authenticate(bwt, temp_text):
                text = temp_text
                print(text)
            else:
                print('The string is not a Burrows-Wheeler Transform \
of any text.')
        except Exception as e:
            print('\n\n')
            print(e)
            print_help()
        return

    # catch all
    print_help()


if __name__ == '__main__':
    import sys
    argv = tuple(sys.argv)
    main(argv)
