"""
Module for performing sliding window Lempel-Ziv on a string and
compression to binary.

Used to compute compression rate.
"""
import encoding
import math

# set parameters
with open('source_book.txt') as f:
    source = f.read()
multiplier = 1

def lz_encode_binary(X: str, n_w: int) -> str:
    # first record and encode the alphabet
    alphabet = set(X)
    alphabet_encoding = encoding.encode_alphabet(alphabet)
    A = len(alphabet)

    log_n_w = math.log(n_w, 2)
    log_A = math.log(A, 2)

    if n_w > len(X):
        raise Exception("Window is larger than entire source so no compression can be applied.")

    result = ""
    for marker in range(n_w):
        # encode first n_w symbols without compression
        result += alphabet_encoding[X[marker]]

    marker = n_w # marks the start of the buffer
    while True:
        if marker == len(X):
            # break after string is done
            break
        L = 0
        m = None
        for current_m in range(0, n_w): # loop over possible offset values
            current_L = 0 # find maximum phrase length
            while True:
                # for this offset, find the longest match
                if X[marker + current_L] == X[marker - current_m + current_L - 1]:
                    # check if next character in buffer equals next character in window
                    current_L += 1
                else:
                    # if not then stop looking
                    break
                if marker + current_L >= len(X):
                    # also stop looking if end of text is reached
                    break
            if current_L > L:
                # if this is the longest match so far, record it
                L = current_L
                m = current_m
        if m is None:
            # even if no match is found L should be 1
            L = 1

        # first encode L using the e function
        result += encoding.e(L)
        if log_n_w < math.ceil(L * log_A) and m is not None:
            # case with compression
            result += encoding.e(m)
        else:
            for i in range(L):
                result += alphabet_encoding[X[marker + L]]
            # case without compression
        marker += L
    return result


def lz_decode_binary(code: str) -> str:
    # TODO implement decoder
    pass

if __name__ == "__main__":

    import matplotlib.pyplot as plt

    plt.xlabel("Size of window (in $\log_2$ scale)")
    plt.ylabel("Compression rate")
    plt.title("Lempel-Ziv compression rate")

    uncompressed = encoding.encode_text(source)

    upper_bound = 20

    try:
        for i in range(0, upper_bound + 1):
            compressed = lz_encode_binary(source, 2 ** i)
            rate = len(compressed) / len(uncompressed)
            print("Window size (log2)", i, "Compression rate:", rate)
            plt.scatter(i, rate, c='r', marker='x')
    except:
        pass

    plt.hlines(1, 0, upper_bound, colors='k', linestyles='dashed')
    plt.savefig("graph.png")