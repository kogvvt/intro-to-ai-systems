import random
import numpy as np

def encode_binary(x, num_bits):
    max = num_bits*num_bits - 1
    step_size = 10 / max
    scaled_x = int(x / step_size)
    binary_string = format(scaled_x, '0' + str(num_bits) + 'b')
    return binary_string

def decode_binary(binary_string, num_bits):
    max = num_bits*num_bits - 1
    step_size = 10 / max
    scaled_x = int(binary_string, 2)
    x = round(scaled_x * step_size,5)
    return x

num_bits = 8
x = 7.25
binary_string = encode_binary(x, num_bits)
print(f"Binary representation of x: {binary_string}")


decoded_x = decode_binary(binary_string, num_bits)
print(f"Decoded value of x: {decoded_x}")