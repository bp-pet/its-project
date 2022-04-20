input_string = "Hello everyone! Hello world!"

code_string = ""

window_size = 25
buffer_size = 8
lookback_size = window_size - buffer_size


i = 0 # can't use for loop because we want to skip multiple iterations sometimes
while True:
    if i == len(input_string):
        # break after string is done
        break

    # get the lookback and buffer strings
    lookback = input_string[max(0, i - lookback_size):i]
    buffer = input_string[i:min(i + buffer_size, len(input_string))]

    # find a match for the first character in the buffer
    starting_index = None
    for ind, j in enumerate(lookback):
        # find first instance of first buffer item in lookback window
        if buffer[0] == j:
            starting_index = ind
            break
    if starting_index is None:
        # if no matches found then encode string as itself and continue
        code_string += buffer[0]
        i += 1
        continue

    # find the end of the match
    match_length = 1
    for ind, j in enumerate(buffer[1:]):
        # check how far in the buffer we can go before match ends
        if starting_index + ind + 1 > len(lookback) - 1:
            # reached end of lookback window
            break
        if j == lookback[starting_index + ind + 1]:
            # if next character is match, keep looking
            match_length += 1
        else:
            # if not match, we stop looking
            break

    # encode match
    if match_length == 1:
        # no special encoding if match is length 1
        code_string += buffer[0]
        i += 1
    else:
        # else write encoding and jump forward
        code_string += f"<{lookback_size - starting_index - 1}, {match_length}>"
        i += match_length


print(code_string)

# TODO change search technique: first maximize L, then minimize m (take rightmost longest match)
# TODO change it so that match can overlap with buffer

# Paul will look into how to actually encode (look into paper)

# Dimitri will write out exercises

# research questions:
# prove that if window size becomes large we approach the entropy