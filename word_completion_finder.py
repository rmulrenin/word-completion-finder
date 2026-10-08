################################################################################
#
# Computer Project 06
# Description:
# This program uses sets and dictionaries to create a word completion tool.
# It reads words from a file provided by the user, cleans and stores them
# into a set of unique words, and then builds a dictionary where each key is
# a index, letter pair that maps to a list of words containing that character
# at that index.
#
# The user is prompted to enter a prefix, and the program finds all words
# that begin with that prefix by intersecting matching words from the
# dictionary. It continues to prompt for prefixes until the user enters '#'.
#
################################################################################


import string

# --- banner (read-only) ---
banner = (
    "\n==============================================\n"
    "     Welcome to the Word Completion Finder!\n"
    "==============================================\n"
    "This program helps you find words that begin\n"
    "with a given prefix from any text file you choose.\n"
    "Type '#' at any time to quit.\n"
)

# All your functions definition starts here
def open_file():
    '''
    Prompt users for a filename until a valid file exists.
    Returns the opened file pointer
    '''
    while True:
        file_name = input("\n:~Input a file name ~:")
        try:
            fp = open(file_name, encoding="UTF-8")
            return fp
        except FileNotFoundError:
            print("[Error]: no such file")

def read_file(fp):
    '''
    Read lines from a file pointer, strip whitespace,
    and return a set of words.
    '''
    word_set = set()
    for line in fp:
        line = line.strip()
        words = line.split()
        for word in words:
            word = word.strip(string.punctuation).lower()
            if word.isalpha() and len(word) > 1:
                word_set.add(word)
    fp.close()
    return word_set

def auto_dict(word_set):
    '''
    Read words from a set and return a dictionary where
    keys are indices, characters and values are a list
    of words.
    '''
    word_dict = {}
    for word in word_set:
        for i,ch in enumerate(word):
            key = (i, ch)
            if key not in word_dict:
                word_dict[key] = []
            word_dict[key].append(word)
    return word_dict

def check_prefix(word_dict, prefix):
    '''
    Iterates through characters in a prefix and
    returns set of intersected values.
    Values are taken from the word dictionary.
    '''
    search = None

    for i,ch in enumerate(prefix):
        key = (i,ch)
        if key not in word_dict:
            return set()
        if search is None:
            search = set(word_dict[key])
        else:
            search = search & set(word_dict[key])
    return search

def sorted_results(results):
    '''
    Return a sorted list of results from a set of words.

    If the input set is not empty, it returns the words in alphabetical order.
    If the set is empty, it returns an empty list.
    '''
    if results:
        return sorted(results)
    else:
        return []

def main():

    print(banner)
    fp = open_file()
    word_set = read_file(fp)
    print("\nYour vocabulary data file includes {} unique words.".format(len(word_set)))

    word_dict = auto_dict(word_set)
    while True:
        prefix = input("\n:~Enter a prefix to search (# to quit) ~:")
        if prefix == "#":
            print("\nGood Bye")
            break

        results = check_prefix(word_dict, prefix)
        results = sorted_results(results)
        if results:
            print("The words that completes '{}' are: {}".format(prefix, ", ".join(results)))
        else:
            print("There are no completions.")

# These two lines allow this program to be imported into other code
# such as our function_test code allowing other functions to be run
# and tested without 'main' running.  However, when this program is
# run alone, 'main' will execute.
if __name__ == "__main__":
    main()
