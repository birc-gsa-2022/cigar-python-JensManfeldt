"""A module for translating between edit strings and cigar strings."""

import re


def split_pairs(cigar: str) -> list[tuple[int, str]]:
    """Split a CIGAR string into a list of integer-operation pairs.

    Args:
        cigar (str): A CIGAR string

    Returns:
        list[tuple[int, str]]: A list of pairs, where the first element is
        an integer and the second an edit operation.

    >>> split_pairs("1M1D6M1I4M")
    [(1, 'M'), (1, 'D'), (6, 'M'), (1, 'I'), (4, 'M')]

    """
    # In a more sane language, we could get a faster solution by identifying
    # the part of a block that is all digits and then translate that
    # into an integer, but the relative speed of pure Python and its
    # regular expressions make this a reasonable solution.
    return [(int(i), op) for i, op in re.findall(r"(\d+)([^\d]+)", cigar)]


def cigar_to_edits(cigar: str) -> str:
    """Expand the compressed CIGAR encoding into the full list of edits.

    Args:
        cigar (str): A CIGAR string

    Returns:
        str: The edit operations the CIGAR string describes.

    cigar_to_edits("1M1D6M1I4M")
    'MDMMMMMMIMMMM'

    """

    pairs = split_pairs(cigar)
    print(pairs)
    returnString = ""
    for (x,y) in pairs: 
        for _ in range(int(x)):
            returnString = returnString + y
    
    return returnString


def split_blocks(x: str) -> list[str]:
    """Split a string into blocks of equal character.

    Args:
        x (str): A string, but we sorta think it would be edits.

    Returns:
        list[str]: A list of blocks.

    >>> split_blocks('MDMMMMMMIMMMM')
    ['M', 'D', 'MMMMMM', 'I', 'MMMM']

    """
    # In any other language, this would likely not be the most efficient
    # approach to this, but since re.findall calls into C, it is faster
    # than implementing a more reasonable algorithm in pure Python.
    return [m[0] for m in re.findall(r"((.)\2*)", x)]


def edits_to_cigar(edits: str) -> str:
    """Encode a sequence of edits as a CIGAR.

    Args:
        edits (str): A sequence of edit operations

    Returns:
        str: The CIGAR encoding of edits.

    >>> edits_to_cigar('MDMMMMMMIMMMM')
    '1M1D6M1I4M'

    """
    if edits == "":
        return edits
        
    cigar = ""
    currChar = edits[0]
    count = 1
    for char in edits[1:]:
        if char == currChar:
            count += 1
            continue

        cigar = cigar + str(count) + currChar
        count = 1
        currChar = char
    
    cigar = cigar + str(count) + currChar
        


    return cigar

print(edits_to_cigar("MDIMID"))