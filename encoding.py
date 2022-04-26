"""
Collection of functions for binary encoding to help with
Lempel-Ziv implementation.

@author: Paul Stuiver, Bozhidar Petrov
"""

def int_to_bin(k):
    """
    Converts an integer to its binary value.
    """
    k = format(k,"b")
    return k
def u(k):
    """
    Function u from paper.
    """
    u = "0"*(k-1)+"1"
    return u
    
def e_hat(k):
    """
    Function e_hat from paper.
    """
    ehat = u(len(int_to_bin(k))) + int_to_bin(k)
    return ehat

def e(k):
    """
    Function e from paper.
    """
    e = e_hat(len(int_to_bin(k))) + int_to_bin(k)
    return e

def encode_alphabet(A):
    """
    create encoding for an alphabet A
    input is the alphabet A with type list
    output is a dictionary with key the letter and value its binary expansion
    """
    
    # determine length of the binary expansion
    t = len(int_to_bin(len(A)))
    encoding = {}
    
    # assign letters a,b,c,... in the alphabet to 0,1,2,... with their binary expansion
    count = 0
    for i in A:
        binarytemp = int_to_bin(count)
        # add zeros from the left such that each value has the same length
        val = binarytemp.rjust(t,'0')
        encoding[i]=val
        count = count + 1
    return encoding

def encode_text(source: str) -> str:
    """
    Encode an entire text to a binary string.
    """
    result = ""
    alphabet = set(source)
    alphabet_encoded = encode_alphabet(alphabet)
    for s in source:
        result += alphabet_encoded[s]
    return result

if __name__ == "__main__":
    print(e(15))
    A = ['a','b','c','d','e']
    print(encode_alphabet(A))
    print(encode_text("this is an example text with many letters!"))
