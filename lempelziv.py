"""
Module for performing sliding window Lempel-Ziv on a string.

Does not properly compressed, only used to visualize algorithm.
"""

from typing import List, Tuple, Union

# set parameters
source = "Hello everyone! Hello world!"
# with open('source.txt') as f:
#     source = f.read()
window_size = 50
buffer_size = 10
verbose = True

def encode(input_string: str) -> List[Union[str, Tuple[int]]]:

    result = []
    lookback_size = window_size - buffer_size
    marker = 0 # marks the start of the buffer
    while True:
        if verbose:
            print("---------------------------------------------Current start of buffer", marker)
        if marker == len(input_string):
            # break after string is done
            break

        # get the lookback and buffer strings
        lookback = input_string[max(0, marker - lookback_size):marker]
        buffer = input_string[marker:min(marker + buffer_size, len(input_string))]
        if verbose:
            print(lookback + "|" + buffer)

        offset = 1
        match_length = 0

        current_offset = 1
        for current_offset in range(1, len(lookback) + 1): # stop when beginning of lookback window is reached
            if verbose:
                print("-------------current offset", current_offset)
            current_length = 0
            while True:
                # for this offset, find the longest match
                if verbose:
                    print("current length", current_length)
                if (lookback + buffer)[len(lookback) - current_offset + current_length] == buffer[current_length]:
                    # check if next character matches the next character of the buffer
                    current_length += 1
                else:
                    # if not then stop looking
                    break
                if current_length >= len(buffer):
                    # also stop looking if match is as long as the buffer
                    break
            if current_length > match_length:
                # if this is the longest match so far, record it
                match_length = current_length
                offset = current_offset



        # encode match
        if match_length < 2:
            # no special encoding if match is length 1
            result.append(buffer[0])
            marker += 1
        else:
            # else write encoding and jump forward
            result.append((offset, match_length))
            marker += match_length
    return result


def decode(code: List[Union[str, Tuple[int]]]) -> str:
    result = ""
    for c in code:
        if isinstance(c, str):
            result += c
        else:
            offset, length = c[0], c[1]
            if offset > len(result):
                raise Exception("Invalid code, offset is out of bounds")

            start = len(result) - offset
            for i in range(length):
                result += result[start + i]
    return result


if verbose:
    print("Source:", source)
encoded = encode(source)
if verbose:
    print("Encoded:", encoded)
decoded = decode(encoded)
if verbose:
    print("Decoded:", decoded)

print(source == decoded)