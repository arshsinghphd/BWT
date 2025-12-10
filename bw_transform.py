''' BURROWS WHEELER TRANSFORM
----------------
Global variables
----------------
alphabet
    all the alphanumerical characters and space for now.

-------------------------------
Functions and their Description
-------------------------------
bw_transform
    This function takes a string and returns its Burrow-Wheeler Transform.
make_rotations
    Takes a string with with a string ending character at the end.
    Returns a tuple of rotations of the text.
sort_rotations
    This function takes a tuple of rotations of some text, and
    returns a sorted rotations as a tuple.
sorted_rotations_to_bwt
    This function takes a tuple of rotations sorted in a lexicographical
    order and returns a string made of the last characters of the sorted
    rotations as the burrows-wheeler transform.

----------------------------------------
Functions for main and their description
----------------------------------------
process_file
    Takes a file path (str) and returns a new file with the same name but
    extension of .bwt. If not one_word, the BWT of each line is placed on
    the same line in the output file.
encode_file_as_word_list
    Takes a file path (str) and creates a tuple of encodings, corresponding
    to the words in the file at the path.
validate_text
    Validates text with the following test:
    Checks to see if the text has any characters that are not in ALPHABET.
    If there are returns an error message.
    Else returns the text.
print_help
    Prints help message for the encoding function.

-------------------------------
About Burrows-Wheeler Transform
-------------------------------
    * Attributed to two computer scientists Michael Burrows and David Wheeler.
    * Quoting an example from The Burrows-Wheeler Transform: Data Compression,
    Suffix Arrays, and Pattern Matching. Adjeroh, D., Tim Bell, and Amar
    Mukharjee. 2008. Springer Science+Business Media LLC.
    * Steps to BWT:
        1. Say text is 'aardvark', we first add a string end character, '$'
        2. Find all the rotations.
        'aardvark$'
        'ardvark$a'
        'rdvark$aa'
        'dvark$aar'
        'vark$aard'
        'ark$aardv'
        'rk$aardva'
        'k$aardvar'
        '$aardvark'

        3. Sort the rotations
        '$aardvark'
        'aardvark$'
        'ardvark$a'
        'ark$aardv'
        'dvark$aar'
        'k$aardvar'
        'rdvark$aa'
        'rk$aardva'
        'vark$aard'

        4. Gather the character at the end of all the sorted rotations and
        return this as the BWT:
        'k$avrraad'
'''

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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Functions for bw_transform #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def sorted_rotations_to_bwt(sorted_rotations: tuple) -> str:
    '''
    This function takes a tuple of rotations sorted in a lexicographical
    order and returns a string made of the last characters of these sorted
    rotations as the burrows-wheeler transform of the source text.

    Params:
        list(str)   sorted_rotations a sorted list of rotations of some source
                    string.

    Returns:
        str         a string made of the last characters of the sorted
                    rotations, also called the burrow-wheeler transform.

    Examples:
    >>> sorted_rotations_to_bwt((''))
    ''
    >>> sorted_rotations_to_bwt(('$'))
    '$'
    >>> sorted_rotations_to_bwt(('$a', 'a$'))
    'a$'
    >>> sorted_rotations_to_bwt(('$mississippi', 'i$mississipp', \
'ippi$mississ', 'issippi$miss', 'ississippi$m', 'mississippi$', \
'pi$mississip', 'ppi$mississi', 'sippi$missis', 'sissippi$mis', \
'ssippi$missi', 'ssissippi$mi'))
    'ipssm$pissii'
    >>> sorted_rotations_to_bwt(('$aardvark', 'aardvark$', 'ardvark$a', \
'ark$aardv', 'dvark$aar', 'k$aardvar', 'rdvark$aa', 'rk$aardva', 'vark$aard'))
    'k$avrraad'
    >>> sorted_rotations_to_bwt((' aardvarks$3', '$3 aardvarks', \
'3 aardvarks$', 'aardvarks$3 ', 'ardvarks$3 a', 'arks$3 aardv', \
'dvarks$3 aar', 'ks$3 aardvar', 'rdvarks$3 aa', 'rks$3 aardva', \
's$3 aardvark', 'varks$3 aard'))
    '3s$ avrraakd'
    '''
    bwt = ''    # initiate bwt
    # add last characater of each rotation in sorted_rotations to bwt
    for rotation in sorted_rotations:
        bwt += rotation[-1]
    return bwt


def sort_rotations(rotations: tuple) -> tuple:
    '''
    This function takes a tuple of rotations of some text, and
    returns a sorted tuple.

    Params:
        tuple(str)   rotations, a tuple  of rotations of some string.

    Returns:
        tuple(str)   rotations, stable-sorted in a lexicographical order.

    Examples:
    >>> sort_rotations((''))
    ()
    >>> sort_rotations(('$'))
    ('$',)
    >>> sort_rotations(('a$', '$a'))
    ('$a', 'a$')
    >>> sort_rotations(('mississippi$', 'ississippi$m', 'ssissippi$mi', \
'sissippi$mis', 'issippi$miss', 'ssippi$missi', 'sippi$missis', \
'ippi$mississ', 'ppi$mississi', 'pi$mississip', 'i$mississipp', \
'$mississippi'))
    ('$mississippi', 'i$mississipp', 'ippi$mississ', 'issippi$miss', \
'ississippi$m', 'mississippi$', 'pi$mississip', 'ppi$mississi', \
'sippi$missis', 'sissippi$mis', 'ssippi$missi', 'ssissippi$mi')
    >>> sort_rotations(('aardvark$', 'ardvark$a', 'rdvark$aa', 'dvark$aar', \
'vark$aard', 'ark$aardv', 'rk$aardva', 'k$aardvar', '$aardvark'))
    ('$aardvark', 'aardvark$', 'ardvark$a', 'ark$aardv', 'dvark$aar', \
'k$aardvar', 'rdvark$aa', 'rk$aardva', 'vark$aard')
    >>> sort_rotations(('3 aardvarks$', ' aardvarks$3', 'aardvarks$3 ', \
'ardvarks$3 a', 'rdvarks$3 aa', 'dvarks$3 aar', 'varks$3 aard', \
'arks$3 aardv', 'rks$3 aardva', 'ks$3 aardvar', 's$3 aardvark', \
'$3 aardvarks'))
    (' aardvarks$3', '$3 aardvarks', '3 aardvarks$', 'aardvarks$3 ', \
'ardvarks$3 a', 'arks$3 aardv', 'dvarks$3 aar', 'ks$3 aardvar', \
'rdvarks$3 aa', 'rks$3 aardva', 's$3 aardvark', 'varks$3 aard')
    '''
    rotations = list(rotations)
    rotations.sort()    # python's in-built sort is a stable sort
    rotations = tuple(rotations)
    return rotations


def make_rotations(text: str) -> tuple:
    '''
    Takes a string with with a string ending character at the end.
    Returns a list rotations of the text.

    Params:
        text str, a string with a '$' at the end

    Returns:
        list(str)   a list of rotations of text.

    Examples:
    >>> make_rotations('')
    ()
    >>> make_rotations('$')
    ('$',)
    >>> make_rotations('a$')
    ('a$', '$a')
    >>> make_rotations('mississippi$')
    ('mississippi$', 'ississippi$m', 'ssissippi$mi', 'sissippi$mis', \
'issippi$miss', 'ssippi$missi', 'sippi$missis', 'ippi$mississ', \
'ppi$mississi', 'pi$mississip', 'i$mississipp', '$mississippi')
    >>> make_rotations('aardvark$')
    ('aardvark$', 'ardvark$a', 'rdvark$aa', 'dvark$aar', 'vark$aard', \
'ark$aardv', 'rk$aardva', 'k$aardvar', '$aardvark')
    >>> make_rotations('3 aardvarks$')
    ('3 aardvarks$', ' aardvarks$3', 'aardvarks$3 ', 'ardvarks$3 a', \
'rdvarks$3 aa', 'dvarks$3 aar', 'varks$3 aard', 'arks$3 aardv', \
'rks$3 aardva', 'ks$3 aardvar', 's$3 aardvark', '$3 aardvarks')
    '''
    n = len(text)
    text2 = text + text
    rotations = []
    for i in range(n):  # find rotations and fill the list
        rotations.append(text2[i:i+n])
    return tuple(rotations)


def bw_transform(text: str, end_char: str = '$') -> str:
    '''
    This function takes a string and returns its Burrow-Wheeler Transform.

    Params:
    str     text, assume for the first run that the text is only alphanumeric.
    end_char EOF character, default value is '$'.

    Returns:
    str     the burrows wheeler transform of text provided

    Examples:
    >>> bw_transform('')
    '$'
    >>> bw_transform('a')
    'a$'
    >>> bw_transform('mississippi')
    'ipssm$pissii'
    >>> bw_transform('aardvark')
    'k$avrraad'
    >>> bw_transform('3 aardvarks')
    '3s$ avrraakd'
    '''
    text = text + end_char   # add end_char to the end of the string
    rotations = make_rotations(text)    # initiate and fill list of rotations
    # sort rotations in lexicographical order
    sorted_rotations = sort_rotations(rotations)
    # create and return bwt from the sorted_rotations
    bwt = sorted_rotations_to_bwt(sorted_rotations)
    return bwt

# ~~~~ #
# Main #
# ~~~~ #


def print_help() -> None:
    '''
    Prints help message for the encoding function.
    '''
    print('')
    print('')
    print("Usage: python3 bw_transform [-h|--help] [-f filename | -s string]")
    print("")
    print("Options:")
    print("-h | --help")
    print("    Prints this message and exits.")
    print("-f filename")
    print("    * Following -f provide path to the file_name.txt to encode.")
    print("    * The function expects a file of size 1 MB or smaller.")
    print("    * The function expects only alphanumericals and spaces in the")
    print("      file.")
    print("    * Encoded text is always stored at the same path and file name")
    print("      but with an extension of .bwt.")
    print("    * Encoded text will have $ as EOF character.")
    print("    * If the encoding works function returns True, else None.")
    print("-s 'text'")
    print("    * Function looks for -f first then -s.")
    print("      If -f is found -s is ignored.")
    print("    * Following -s provide the string to be encode.")
    print("    * Please enclose the string in single quotes ('). E.g. 'text'")
    print("    * The function expects only alphanumericals and spaces.")
    print("    * If the encoding works function returns a string, else None")
    print("    * The functions saves nothing.")
    print('')
    print('')


def validate_text(text: str, line_no: int = None) -> str:
    '''
    Validates text with the following test:
    Checks to see if the text has any characters that are not in ALPHABET.
    If there are returns an error message.
    Else returns the text.

    Params:
    text (str)  the text to be burrows-wheeler transformed.

    Returns:
    text (str)  if it passes all validation tests.
    error_message  if the text has any special characters.

    Examples:
    >>> validate_text('')
    ''
    >>> validate_text('ababs')
    'ababs'
    >>> validate_text('     ')
    '     '
    >>> validate_text('ababs', 10)
    'ababs'
    >>> validate_text('a$bab$s')
    'String has characters other than spaces and alphanumeric.'
    >>> validate_text('a$bab$s', 10)
    'Line no. 10 has characters other than spaces and alphanumeric.'
    '''
    # counting characters not in ALPHABET
    count_non = 0
    n = len(text)
    for i in range(n):
        if text[i] in ALPHABET:
            continue
        # else
        count_non += 1
    if count_non > 0:
        if line_no:     # being used in a file
            return f'Line no. {line_no} has characters other than spaces \
and alphanumeric.'
        else:           # being used for a string
            return 'String has characters other than spaces and \
alphanumeric.'
        return
    return text


def encode_file_as_word_list(input_file: str,
                             end_char: str = '$') -> tuple | str:
    '''
    Takes a file path (str) and creates a tuple of encodings, corresponding
    to the words in the file at the path.
    '''
    # try and except for some unexpected error in reading the file
    try:
        output_list = []
        with open(input_file, 'r') as f_in:
            counter = 0
            for raw_text in f_in:
                raw_text = raw_text.strip()
                try:       # try and except for each line
                    text = validate_text(raw_text, counter)
                    if text == raw_text:
                        temp_bwt = bw_transform(text, end_char=end_char)
                        if authenticate(temp_bwt, text, end_char=end_char):
                            bwt = temp_bwt
                        else:
                            print(f"Error while processing line no. {counter}:\
 unable to encode to BWT.")
                            bwt = ''
                    else:  # error
                        print(text)
                        bwt = ''
                except Exception as e:
                    print(f"Error while processing line no. {counter}: {e}")
                    bwt = ''
                output_list.append(bwt)
                counter += 1
        return tuple(output_list)
    except Exception as e:
        return e


def process_file(input_file: str,
                 end_char: str = '$',
                 one_word: bool = False) -> bool | str:
    '''
    Takes a file path (str) and returns a new file with the same name but
    extension of .bwt. If not one_word, the BWT of each line is placed on
    the same line in the output file.

    Params:
    input_file (str)    path to the input file
    end_char (str)      EOF character, default value is '$'
    one_word (bool)     True, the whole file should be considered a word,
                        rather than the default of False
                        False, the file should be considered a list of words,
                        separated by '\n' or newline characters.
    Output:
    Write a file in the same folder as the input_file with the same name but
        with extension .bwt.
    Prints message on the terminal if:
        any line has characters other than space or alphanumeric.
    '''
    if one_word:    # defunt for now, kept here for the sake of completeness.
                    # signal to deal with the whole file as one word.
        pass
    else:
        try:
            output_tuple = encode_file_as_word_list(input_file,
                                                    end_char=end_char)
            if not isinstance(output_tuple, tuple):    # error
                return output_tuple

            # else write output file
            output_file = input_file[:-4] + '.bwt'
            with open(output_file, 'w') as f:
                for bwt in output_tuple:
                    f.write(bwt + '\n')

            return True
        except Exception as e:
            return e


def main(argv: tuple) -> str:
    # help block
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
        input_file = validate_file(file_path, '.txt')
        if input_file != file_path:    # returned an error message
            print(input_file)
            print_help()
            return
        # else
        status = process_file(input_file)
        if status is True:
            output_file = input_file[:-4] + '.bwt'
            print(f'Output file is saved as {output_file}.')
            return True
        #else: status is a string
        print(status)
        return

    # string block
    if '-s' in argv:
        string = get_string(argv)
        if not string:
            print('\n\nNo string provided.')
            print_help()
            return
        string = string.strip()
        text = validate_text(string)
        if text != string:
            print(text)
            print_help()
            return
        # else try decoding bwt, except unknow errors
        try:
            print(bw_transform(text))
            return
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
