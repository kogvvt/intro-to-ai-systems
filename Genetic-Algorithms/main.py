import random
import numpy as np

def encode_binary(x, num_bits):
    binary_string = ""
    integer_part = int(x)
    fract_part = x-integer_part
    
    int_binary = bin(integer_part)[2:]
    fract_binary = ''
    while fract_part > 0 and len(fract_binary) < num_bits:
        fract_part *= 2
        bit = '1' if fract_part >= 1 else '0'
        fract_binary += bit
        fract_part -= int(fract_part)

    
    binary_string = int_binary + '.' + fract_binary
    if len(binary_string) < num_bits+1 :
        binary_string.ljust(len(binary_string),'0')

    return binary_string


def decode_binary(binary_string, num_bits):
    parts = binary_string.split('.')
    integer_binary = parts[0]
    fractional_binary = parts[1]

    
    integer_part = int(integer_binary, 2)

    
    fractional_part = 0
    for i, bit in enumerate(fractional_binary):
        if bit == '1':
            fractional_part += 2 ** -(i + 1)

    decoded_number = integer_part + fractional_part

    return decoded_number

num_bits = 8
x = 7.25
binary_string = encode_binary(x, num_bits)
print(f"Binary representation of x: {binary_string}")


decoded_x = decode_binary(binary_string, num_bits)
print(f"Decoded value of x: {decoded_x}")