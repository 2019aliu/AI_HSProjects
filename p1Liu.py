# @author ALiu
# @date 2/22-27/18
# Regex HW 1 + 2

import sys
newInput = int(sys.argv[1])

# the dictionary contains my answers
# issues with: 40, 44,

''' 
as of 10:14 03/06/18: problems on:

[39, 40, 43, 44, 47, 50, 52, 54, 55]

complete failures on:
40, 44, 52, 54

lots of failures on:
43, 47, 

some failures on:
39, 50, 55
'''

dict = {
    31: r"/^0$|^100$|^101$/",
    32: r"/^[01]*$/",
    33: r"/^[01]*?0$/m",
    34: r"/\b\w*?[aeiou]\w*?[aeiou]\w*/im",
    35: r"/^1[01]*?0$|^0$/",
    36: r"/^[01]*?110[01]*?$/s",
    37: r"/^.{2,4}$/s",
    38: r"/^\d{3}\s*?-?\s*?\d{2}\s*?-?\s*?\d{4}$/",
    39: r"/^\b\w*d\w*\b/m", # only checks first word
    40: r"/[01*?'01'+?1*?0|10*?'10'+?0*?1|0|1]/",  # this one is wrong
    41: r"/\b[PCKpck]\w*/",
    42: r"/^(..)*.$/s",
    43: r"/^0([01][01])*$|^1([01][01])*0$/m",
    44: r"/^[01][^(110)]$/m",  # this one is wrong, solution with look-ahead: /^(?!110)[01]+$/
    45: r"/^[.XOxo]{64}$/",
    46: r"/^[XOxo]*?[.]{1}[XOxo]*?$/",
    47: r"/^X*?O+?[.].*?$|^.*?[.]O+?X*?$/i",
    48: r"/^\b[bc]*?a?[bc]*?$/m",
    49: r"/^\b([bc]*a+[bc]*a+[bc]*)*$|^[bc]+$/i",
    50: r"/^([02]*?1[02]*?1[02]*?)+$|^2[02]+$|^0$/",
    51: r"/^.*?(.)\1{9}.*$/s",
    52: r"/\b\w*?(\w)\w*?\1\w*?\b/i",
    53: r"/\b\w*(\w)\1\w*/",
    54: r"/\b\w*?(\w)\w*\1\w*?/",
    55: r"/^([01])[01]*\1$/m",
    56: r"/\b(?=cat)\w{6}\b/",
    57: r"/^([01])[01]+(?<=.)\1$/",
    58: r"/^([01])[01]*(?=\1).$/",
    59: r"/\b([aeiou])\w*(?!\1)[aeiou]\b/",
    60: r"/^([01](?<!011))*$/m"
}

print("The regular expression for exercise {} is {}".format(newInput, dict[newInput]))

# { Program written by: 2019aliu }

'''
Assignment:

Determine a regular expression which will match only on the indicated strings, or else will find the indicated
matches. The form for the submission will be a command line script that takes a single integer as input from 31
to 40, inclusive, and outputs the corresponding regular expression pattern, as it was done in class: the pattern is
to be delimited by forward slashes and any options should immediately follow the final slash.

31. Determine whether a string is either 0, 100, or 101.

32. Determine whether a given string is a binary string (ie. composed only of 0 and 1 characters).

33. An integer (sub)string refers to a non-empty (sub)string that will convert to an integer but has no leading 0.
Zero is represented as the single digit 0. Given a binary integer string, what regular expression determines
whether it is even?

34. What is a regular expression to determine (ie. match) those words in a text that have at least two vowels?

35. Given a string, determine whether it is an even binary integer string.

36. Determine whether a given string is a binary string containing 110 as a substring.

37. Match on all strings of length at least two, but at most four.

38. Validate a social security number entered into a field (ie. recognize ddd-dd-dddd where the d represents
digits and where the dash indicates an arbitrary number of spaces with at most one dash). For example,
542786363, 542 786363, and 542 – 78-6263 are all considered valid.

39. Determine a regular expression to help you find the first word of each line of text with a d in it.

40. Determine whether a string is a binary string that has the same number of 01 substrings as 10 substrings.
'''
